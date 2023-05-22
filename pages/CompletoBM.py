import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas_ta as ta
import streamlit as st

tickers = ['HL', 'SONY', 'ETSY', 'BABA', 'SID', 'UL', 'KEP', 'LMT', 'MELI', 'MSFT', 'CX', 'AMX', 'HOG', 'PBI', 'TSM', 'MA', 'VALE', 'MMM', 'BCS', 'BBD', 'DESP', 'WBAD', 'TWTR', 'XD', 'RTX', 'CAAP', 'VZD', 'BAD', 'NEM', 'ABEV', 'BIIB', 'HAL', 'ERIC', 'VIV', 'AAPL', 'IP', 'GOOGL', 'HMY', 'AVY', 'SBS', 'BP', 'NGG', 'ITUB', 'TD', 'JNJ', 'ING', 'XOM', 'HSBC', 'UNP', 'AAPLD', 'PAAS', 'TIMB', 'PEP', 'CL', 'NVS', 'MOD', 'BHP', 'HMC', 'PSX', 'HON', 'V', 'AUY', 'BIDU', 'MCD', 'USB', 'IFF', 'SNA', 'MDT', 'AEG', 'PCAR', 'JD', 'TSLA', 'GPRK', 'ANF', 'SLB', 'PG', 'EBAY', 'TM', 'SQ', 'IBM', 'CRMD', 'FSLR', 'FDX', 'GE', 'AZN', 'VOD', 'DEO', 'AEM', 'BB', 'ARCO', 'ADI', 'GSK', 'T', 'SNOW', 'ERJ', 'CAT', 'GILD', 'NMR', 'BIOX', 'KGC', 'GRMN', 'WFCD', 'VRSN', 'JPM', 'GGB', 'DE', 'CRM', 'WBA', 'ADBE', 'ZM', 'SAN', 'TMO', 'AMD', 'GOLD', 'BMY', 'BA', 'NFLX', 'MO', 'NTES', 'KB', 'QCOM', 'MRK', 'X', 'PGD', 'EFX', 'MUFG', 'AVGO', 'COST', 'MFG', 'WBK', 'UGP', 'ROST', 'VZ', 'ADGO', 'XROX', 'DOCU', 'XOMD', 'AXP', 'NKE', 'YELP', 'FCX', 'PFE', 'AMZN', 'INTC', 'CS', 'WMTD', 'GS', 'C', 'HD', 'MSI', 'KOD', 'CDE', 'LYG', 'RIO', 'SCCO', 'E', 'DD', 'SBUX', 'CVX', 'IBN', 'ORAN', 'CAR', 'KO', 'YY', 'WFC', 'AMAT', 'PBR', 'SAP', 'HWM', 'ABBV', 'SHOP', 'INFY', 'BRFS', 'LVS', 'TTM', 'GFI', 'FMX', 'VISTD', 'URBN', 'AIG', 'BK', 'HPQ', 'AMGN', 'NUE', 'VD', 'GLW', 'KMB', 'EBR', 'TRIP', 'GSD', 'SUZ', 'TXN', 'PHG', 'NTCO', 'WMT', 'SPOT', 'CSCO', 'WBO', 'HSY', 'ORCL', 'ZMD', 'SNAP', 'LLY', 'MMC', 'CAH', 'UNH', 'ABT', 'BSBR', 'NVDA', 'ADP', 'TGT', 'VIST', 'PYPL']


for ticker in tickers[-50:]:
    data = yf.Ticker(ticker).history('5y')
    try:
        data.drop(columns=['Dividends', 'Stock Splits'], inplace=True)

        data['RSI'] = ta.rsi(data['Close'], length = 14)

        data['EMA_RAPIDA'] = ta.ema(data["Close"], length=8)
        data['EMA_MEDIANA'] = ta.ema(data["Close"], length=21)
        data['EMA_LENTA'] = ta.ema(data["Close"], length=50)

        backrollingN = 5
        data['TENDENCIA_RAPIDA']=data['EMA_RAPIDA'].diff(periods=1)
        data['TENDENCIA_RAPIDA']=data['TENDENCIA_RAPIDA'].rolling(window=backrollingN).mean()

        data['TENDENCIA_MEDIANA']=data['EMA_MEDIANA'].diff(periods=1)
        data['TENDENCIA_MEDIANA']=data['TENDENCIA_MEDIANA'].rolling(window=backrollingN).mean()

        data['TENDENCIA_LENTA']=data['EMA_LENTA'].diff(periods=1)
        data['TENDENCIA_LENTA']=data['TENDENCIA_LENTA'].rolling(window=backrollingN).mean()

        data['SALIDA'] = (data.EMA_RAPIDA < data.EMA_MEDIANA) & (data.EMA_MEDIANA < data.EMA_LENTA) & (data.TENDENCIA_RAPIDA>0.1) & (data.TENDENCIA_RAPIDA<0.3)
        print(data)
        if data['SALIDA'].tail(3).any():
            print(ticker)   
            st.write(ticker)
            st.subheader("Historical Data")
                # Filter the data for the last 6 months
            last_six_months_data = data.tail(3*30)  # Assuming each month has 30 days

    # Create a line chart for the last 6 months of data
            st.line_chart(last_six_months_data["Close"])        
    except:
        pass