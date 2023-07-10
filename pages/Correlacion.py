import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()

from dataBM import tickersBM

tickers = st.multiselect('Seleccione el Ticker:', sorted(tickersBM))
colnames = []
combined = pd.DataFrame()

if tickers:
    for ticker in tickers:
        data = yf.Ticker(ticker).history(start=start, end=end)
        if combined.empty:
            combined = pd.DataFrame(data['Close'])
        else:
            combined = pd.concat([combined, pd.DataFrame(data['Close'])], axis=1)
        colnames.append(ticker)

    combined.columns = colnames
    print(combined)

    fig = plt.figure(figsize=(10, 4))
    corr_data = combined.pct_change().corr(method="pearson")
    sns.heatmap(corr_data, annot=True, cmap="coolwarm")

    st.pyplot(fig)