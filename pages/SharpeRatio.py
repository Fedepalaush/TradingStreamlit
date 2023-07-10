import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0][['Symbol', 'GICS Sector', 'GICS Sub-Industry']]

with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Industria",
        ['Industrials', 'Consumer Discretionary', 'Information Technology', 'Financials', 'Health Care', 'Communication Services', 'Materials','Utilities', 'Energy', 'Consumer Staples', 'Real Estate', 'Consumer Staples'],
        index=0 
)


#Agrupado por Sector 
sector_tickers, industry_tickers = {},{}
sectors, industries = tickers.groupby('GICS Sector'), tickers.groupby('GICS Sub-Industry')

for sector, group in sectors:
    sector_tickers[sector] = list(group['Symbol'])
    for industry, industry_group in industries:
        industry_tickers[industry] = list(industry_group['Symbol'])

financials = [ticker.replace(".", "-") for ticker in sector_tickers['Financials']]        
tech = [ticker.replace(".", "-") for ticker in sector_tickers['Information Technology']]
info = [ticker.replace(".", "-") for ticker in sector_tickers[add_combo]] 
#Precios de Cierre
start = '2015-01-01'
end = '2023-07-01'
sp500_fin = pd.DataFrame(yf.download(info + ['^GSPC'], start, end)['Close']).dropna(axis=1)
returns = sp500_fin.pct_change()[1:]


#Sharpe

sharpe_1y = (returns.iloc[-252:,:].mean()/returns.iloc[-252,:].std())
sharpe_2y = (returns.iloc[-252*2:,:].mean()/returns.iloc[-252*2,:].std())
sharpe_5y = (returns.iloc[-252*5:,:].mean()/returns.iloc[-252*5,:].std())

sharpe_df = pd.DataFrame({'Sharpe 1Y': sharpe_1y,
                          'Sharpe 2Y': sharpe_2y,
                          'Sharpe 5Y': sharpe_5y})

#Grafico

fig, ax = plt.subplots(figsize=(16,10))
sns.regplot(x='Sharpe 5Y', y='Sharpe 2Y', data=sharpe_df, color='b', marker='o')
plt.scatter(sharpe_df.loc['^GSPC', 'Sharpe 5Y'], sharpe_df.loc['^GSPC', 'Sharpe 2Y'], s=100, facecolors='r', edgecolors='r')
plt.axvline(sharpe_df.loc['^GSPC', 'Sharpe 5Y'], linestyle='--', lw=1.8, color='r')
plt.axhline(sharpe_df.loc['^GSPC', 'Sharpe 2Y'], linestyle='--', lw=1.8, color='r')
plt.title('Sharpe ratio 2y v 5y: ' + str(add_combo) + ' SP500. From ' + str(start) + ' to ' + str(end), fontweight='bold')
plt.xlabel('Sharpe Ratio (5 Years)')
plt.ylabel('Sharpe Ratio (2 Years)')
plt.grid()

for i in range(len(sharpe_df)):
    if sharpe_df.index[i] != '^GSPC':
        plt.annotate(sharpe_df.index[i], (sharpe_df.iloc[i,2], sharpe_df.iloc[i,1]), xytext=(5,-5), textcoords='offset points', fontsize=9)
    else:
        plt.annotate(sharpe_df.index[i], (sharpe_df.iloc[i,2], sharpe_df.iloc[i,1]), xytext=(5,-5), textcoords='offset points', fontsize=9, color='r')
st.pyplot(fig)