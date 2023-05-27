import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta
import numpy as np

# Set wide mode
st.set_page_config(layout="wide")
options_date = ['1h','1d','5d','1wk','1mo','3mo']
# Barra lateral con Seleccion de Accion, Inicio, Fin y Timeframe
with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        ['AAPL', 'MSFT', 'KO', 'BA'],
        index=0 
)
    fechaInicio = st.date_input(
        "Seleccione Fecha Inicio",
        datetime.date.today() - timedelta(days=365))
    fechaFin = st.date_input(
        "Seleccione Fecha Fin",
        datetime.date.today())
    
    timeframe = st.selectbox(
        "Seleccione timeframe",
        options_date,
        index=options_date.index('1d'))
    

data = yf.Ticker(add_combo).history(start=fechaInicio, end=fechaFin, interval=timeframe)


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


st.dataframe(data)

#Precio del último cierre
latest_day_data = data.iloc[-1].Close
st.text(f"Precio Actual: ${latest_day_data:.2f}")


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
