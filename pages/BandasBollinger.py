import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas_ta as ta
from dataBM import tickersBM

for ticker in tickersBM:
    try:
        data = yf.Ticker(ticker).history(period='max')

        # Calculate Bollinger Bands
        bollinger_bands = ta.bbands(data['Close'], length=20, std=2)
        rsi = ta.rsi(data['Close'], length=13)
 
        # Print the DataFrame with Bollinger Bands
        precio_actual = data['Close'].tail(1).values[0]
        banda_inferior = bollinger_bands.tail(3)['BBL_20_2.0'].values
        banda_superior = bollinger_bands.tail(3)['BBU_20_2.0'].values
        rsi_values = rsi.tail(3).values
          
        if (precio_actual < banda_inferior).any() and (rsi_values < 35).any():
            st.text(ticker + " Compra")
        else:
            pass        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        pass    