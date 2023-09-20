import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas_ta as ta
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dataBM import tickersBM

tickers = tickersBM

def graficoVelas(data):
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


# Agregar barra lateral
st.sidebar.subheader("Configuraciones")

# Intervalo de tiempo
intervalo_tiempo = st.sidebar.selectbox("Intervalo de Tiempo", ['1d', '1h', '4h', '1s'], index=1)

longitud_ema_lenta = st.sidebar.slider("Longitud de EMA Lenta", 1, 252, 200)
longitud_ema_rapida = st.sidebar.slider("Longitud de EMA Rápida", 1, 200, 50)

# Add an "Ejecutar" button
ejecutar_button = st.sidebar.button("Ejecutar")

if ejecutar_button:
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(interval=intervalo_tiempo)
            print(data)
            
            # Filter out 'Dividends' and 'Stock Splits' events
            data = data.drop(['Dividends', 'Stock Splits'], axis=1)

            data['RSI'] = ta.rsi(data['Close'], length = 14)
            data['EmaLenta'] =  ta.ema(data["Close"], length=longitud_ema_lenta)
            data['EmaRapida'] =  ta.ema(data["Close"], length=longitud_ema_rapida)

            data['SALIDALARGO'] = 0  # Default value
            data.loc[(data['EmaRapida'] > data['EmaLenta']) & (data['EmaRapida'].shift() < data['EmaLenta'].shift()) , 'SALIDALARGO'] = 1
            data.loc[(data['EmaRapida'] < data['EmaLenta']) & (data['EmaRapida'].shift() > data['EmaLenta'].shift()) , 'SALIDALARGO'] = 2

            if data['SALIDALARGO'].tail(3).any():
                if (data['SALIDALARGO'].tail(3) == 1).any():
                    st.write('LONG')
                    st.write(ticker)    
                    graficoVelas(data)
        except Exception as e:
            continue

        except:
            pass
