import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas_ta as ta
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go



tickers = ['HL', 'SONY', 'ETSY', 'BABA', 'SID', 'UL', 'KEP', 'LMT', 'MELI', 'MSFT', 'CX', 'AMX', 'HOG', 'PBI', 'TSM', 'MA', 'VALE', 'MMM', 'BCS', 'BBD', 'DESP', 'WBAD', 'TWTR', 'XD', 'RTX', 'CAAP', 'VZD', 'BAD', 'NEM', 'ABEV', 'BIIB', 'HAL', 'ERIC', 'VIV', 'AAPL', 'IP', 'GOOGL', 'HMY', 'AVY', 'SBS', 'BP', 'NGG', 'ITUB', 'TD', 'JNJ', 'ING', 'XOM', 'HSBC', 'UNP', 'AAPLD', 'PAAS', 'TIMB', 'PEP', 'CL', 'NVS', 'MOD', 'BHP', 'HMC', 'PSX', 'HON', 'V', 'AUY', 'BIDU', 'MCD', 'USB', 'IFF', 'SNA', 'MDT', 'AEG', 'PCAR', 'JD', 'TSLA', 'GPRK', 'ANF', 'SLB', 'PG', 'EBAY', 'TM', 'SQ', 'IBM', 'CRMD', 'FSLR', 'FDX', 'GE', 'AZN', 'VOD', 'DEO', 'AEM', 'BB', 'ARCO', 'ADI', 'GSK', 'T', 'SNOW', 'ERJ', 'CAT', 'GILD', 'NMR', 'BIOX', 'KGC', 'GRMN', 'WFCD', 'VRSN', 'JPM', 'GGB', 'DE', 'CRM', 'WBA', 'ADBE', 'ZM', 'SAN', 'TMO', 'AMD', 'GOLD', 'BMY', 'BA', 'NFLX', 'MO', 'NTES', 'KB', 'QCOM', 'MRK', 'X', 'PGD', 'EFX', 'MUFG', 'AVGO', 'COST', 'MFG', 'WBK', 'UGP', 'ROST', 'VZ', 'ADGO', 'XROX', 'DOCU', 'XOMD', 'AXP', 'NKE', 'YELP', 'FCX', 'PFE', 'AMZN', 'INTC', 'CS', 'WMTD', 'GS', 'C', 'HD', 'MSI', 'KOD', 'CDE', 'LYG', 'RIO', 'SCCO', 'E', 'DD', 'SBUX', 'CVX', 'IBN', 'ORAN', 'CAR', 'KO', 'YY', 'WFC', 'AMAT', 'PBR', 'SAP', 'HWM', 'ABBV', 'SHOP', 'INFY', 'BRFS', 'LVS', 'TTM', 'GFI', 'FMX', 'VISTD', 'URBN', 'AIG', 'BK', 'HPQ', 'AMGN', 'NUE', 'VD', 'GLW', 'KMB', 'EBR', 'TRIP', 'GSD', 'SUZ', 'TXN', 'PHG', 'NTCO', 'WMT', 'SPOT', 'CSCO', 'WBO', 'HSY', 'ORCL', 'ZMD', 'SNAP', 'LLY', 'MMC', 'CAH', 'UNH', 'ABT', 'BSBR', 'NVDA', 'ADP', 'TGT', 'VIST', 'PYPL']


for ticker in tickers:
    data = yf.Ticker(ticker).history('5y')
    try:
        data.drop(columns=['Dividends','Stock Splits'], inplace=True)
        data['RSI'] = ta.rsi(data['Close'], length = 14)

        data['Ema200'] =  ta.ema(data["Close"], length=200)
        data['EmaLenta'] =  ta.ema(data["Close"], length=50)
        data['EmaMediana'] =  ta.ema(data["Close"], length=21)
        data['EmaRapida'] =  ta.ema(data["Close"], length=8)

        backrollingN = 5
        data['TENDENCIA_RAPIDA']=data['EmaRapida'].diff(periods=1)
        data['TENDENCIA_RAPIDA']=data['TENDENCIA_RAPIDA'].rolling(window=backrollingN).mean()

        data['TENDENCIA_MEDIANA']=data['EmaMediana'].diff(periods=1)
        data['TENDENCIA_MEDIANA']=data['TENDENCIA_MEDIANA'].rolling(window=backrollingN).mean()

        data['TENDENCIA_LENTA']=data['EmaLenta'].diff(periods=1)
        data['TENDENCIA_LENTA']=data['TENDENCIA_LENTA'].rolling(window=backrollingN).mean()

        # Check the conditions and assign values
        data['SALIDACORTO'] = 0  # Default value
        data.loc[(data['EmaRapida'] > data['EmaMediana']) & (data['EmaRapida'].shift() < data['EmaMediana'].shift()), 'SALIDACORTO'] = 1
        data.loc[(data['EmaRapida'] < data['EmaMediana']) & (data['EmaRapida'].shift() > data['EmaMediana'].shift()), 'SALIDACORTO'] = 2

        data['SALIDALARGO'] = 0  # Default value
        data.loc[(data['EmaLenta'] > data['Ema200']) & (data['EmaLenta'].shift() < data['Ema200'].shift()), 'SALIDALARGO'] = 1
        data.loc[(data['EmaLenta'] < data['Ema200']) & (data['EmaLenta'].shift() > data['Ema200'].shift()), 'SALIDALARGO'] = 2


       



        if data['SALIDACORTO'].tail(3).any():
            if (data['SALIDACORTO'].tail(3) == 1).any():
                st.write('LONG')
            if (data['SALIDACORTO'].tail(3) == 2).any():
                st.write('SHORT')
            st.write(ticker)
        #Grafico de Velas
            st.subheader("Grafico de Velas")
            # Create a subplot with shared x-axis
            fig = make_subplots(shared_xaxes=True)
            # Add the candlestick trace
            candlestick_trace = go.Candlestick(x=data.index,
                                            open=data['Open'],
                                            high=data['High'],
                                            low=data['Low'],
                                            close=data['Close'])
            fig.add_trace(candlestick_trace)
            # Add range breaks to the x-axis
            rangebreaks = [
                dict(bounds=["sat", "mon"]),  # Range break from Saturday to Monday
            ]
            fig.update_layout(xaxis_rangeslider_visible=False,  # Disable the rangeslider
                            xaxis=dict(rangebreaks=rangebreaks))  # Add the range breaks
            # Display the chart
            st.plotly_chart(fig)
    
    except:
        pass