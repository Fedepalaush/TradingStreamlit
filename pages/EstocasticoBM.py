import pandas as pd
import yfinance as yf
import seaborn as sns
import streamlit as st
import pandas_ta as ta
from dataBM import tickersBM

tickers = tickersBM
for ticker in tickers:
    data = yf.Ticker(ticker).history('1y')
    try:
        data.drop(columns=['Dividends','Stock Splits'], inplace=True)
        data['RSI'] = ta.rsi(data['Close'], length = 14)

        data['Ema200'] =  ta.ema(data["Close"], length=200)
      
        k_period = 14
        d_period = 3
        # Adds a "n_high" column with max value of previous 14 periods
        data['n_high'] = data['High'].rolling(k_period).max()
        # Adds an "n_low" column with min value of previous 14 periods
        data['n_low'] = data['Low'].rolling(k_period).min()
        # Uses the min/max values to calculate the %k (as a percentage)
        data['%K'] = (data['Close'] - data['n_low']) * 100 / (data['n_high'] - data['n_low'])
        # Uses the %k to calculates a SMA over the past 3 values of %k
        data['%D'] = data['%K'].rolling(d_period).mean()
        data.dropna(inplace=True)

        data['SALIDA'] = 0  # Default value
        data.loc[(data['%D'] > data['%K']) & (data['%D'].shift() < data['%K'].shift()), 'SALIDA'] = 1
        data.loc[(data['%D'] < data['%K']) & (data['%D'].shift() > data['%K'].shift()), 'SALIDA'] = 2

        if ((data.tail(1)['SALIDA']==1).values[0]) & (data.tail(1)['Ema200'].values[0]<data.tail(1)['Close'].values[0]) & ((data.tail(3)['%K'].tail(3)> 78).any()):
            st.text(ticker)
            st.text(data.tail(1)['Ema200'].values[0])
            st.text(data.tail(1)['Close'].values[0])
            st.text('Superior') 

        if ((data.tail(1)['SALIDA']==2).values[0]) & (data.tail(1)['Ema200'].values[0]>data.tail(1)['Close'].values[0]) & ((data.tail(3)['%K'].tail(3)< 22).any()):
            st.text(ticker)
            st.text('Inferior') 
            
    except:
        pass