import yfinance as yf
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas_ta as ta
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        ['AAPL', 'MSFT', 'KO', 'BA', 'SPY'],
        index=0 )

    
tickers = [add_combo, '^VIX']
data = yf.download(tickers, period='15y')

df = data['Close'].pct_change()
df['ATR'] = ta.atr(data['High'][add_combo], data['Low'][add_combo],data['Close'][add_combo], length=14)
df['Relative_Volume'] = data['Volume'][add_combo]/data['Volume'][add_combo].rolling(40).mean()
df['std'] = data['Close'][add_combo].rolling(40).std()
df['H-L'] = data['High'][add_combo]/data['Low'][add_combo]-1
df['O-C'] = data['Open'][add_combo]/data['Close'][add_combo]-1
df['DD'] = data['Close']['^VIX']/data['Close']['^VIX'].cummax()-1
df['Avrg_dd'] = (data['Close']['^VIX']/data['Close']['^VIX'].cummax()-1).rolling(20).mean()
df.dropna(inplace=True)

st.dataframe(df)
kmeans = KMeans(4)

df['regime'] = kmeans.fit_predict(df)
col = []
for i in range (0,len(df)):
    if df['regime'].iloc[i]==0:
        col.append('blue')
    elif df['regime'].iloc[i]==1: 
        col.append('red')
    elif df['regime'].iloc[i]==2: 
        col.append('orange')
    else:
        col.append('brown')

fig, ax = plt.subplots()
ax.scatter(data.index[39:], data['Close'][add_combo][39:], c=col, s=4)
ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.set_title('Scatter Plot')

# Display scatter plot in Streamlit
st.pyplot(fig)

st.dataframe(data)