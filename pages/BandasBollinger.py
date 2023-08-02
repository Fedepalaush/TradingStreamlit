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
        print(data)

        # Calculate Bollinger Bands
        bollinger_bands = ta.bbands(data['Close'], length=20, std=2)

        # Print the DataFrame with Bollinger Bands
        precio_actual = data['Close'].tail(1).values[0]
        banda_inferior = bollinger_bands.tail(3)['BBL_20_2.0'].values
        banda_superior = bollinger_bands.tail(3)['BBU_20_2.0'].values[0]

          
        if ((precio_actual<banda_inferior)).any():
            st.text(ticker + " Compra")
        else:
            pass        
    except:
        pass    