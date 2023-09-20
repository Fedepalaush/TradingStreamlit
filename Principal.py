import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit import session_state as state
import os 

CSV_FILE_PATH = 'ratios.csv'
# Set wide mode
st.set_page_config(layout="wide")
options_date = ['1h','1d','5d','1wk','1mo','3mo']
# Barra lateral con Seleccion de Accion, Inicio, Fin y Timeframe
with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        ['AAPL', 'MSFT', 'KO', 'BA', 'TD'],
        index=0 
)
    fechaInicio = st.date_input(
        "Seleccione Fecha Inicio",
        datetime.date.today() - timedelta(days=1825))
    
    timeframe = st.selectbox(
        "Seleccione timeframe",
        options_date,
        index=options_date.index('1d'))
    
if 'ratios' not in state:
    # Load the DataFrame from the CSV file if it exists
    if os.path.isfile(CSV_FILE_PATH):
        state.ratios = pd.read_csv(CSV_FILE_PATH)
    else:
        # Create an empty DataFrame if it doesn't exist
        state.ratios = pd.DataFrame()


def infoAccion (ticker):
    data = yf.Ticker(ticker).history(start=fechaInicio, end=datetime.date.today(), interval=timeframe)
    st.dataframe(data)
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
    return data

def calculaMeses(data):
    df = pd.DataFrame(data)
    df['Fecha'] = df.index
    df['Fecha'] = pd.to_datetime(df['Fecha'])  # Convertir la columna 'Fecha' a tipo de dato datetime

    # Crear una nueva columna 'Year' y 'Month' para separar el año y el mes
    df['Year'] = df['Fecha'].dt.year
    df['Month'] = df['Fecha'].dt.month

    # Agrupar los datos por año y mes, y seleccionar el primer y último valor
    agg_funcs = {'Open': 'first', 'Close': 'last'}
    result = df.groupby(['Year', 'Month']).agg(agg_funcs)

    # Resetear el índice para que los años y meses sean columnas en el nuevo DataFrame
    result.reset_index(inplace=True)
    result['PCT'] = (((result['Close']/result['Open'])-1)*100)
    
        # Pivot the DataFrame to create a matrix suitable for a heatmap
    pivot_result = result.pivot(index='Month', columns='Year', values='PCT')

    # Create the heatmap
    fig = plt.figure(figsize=(7, 3))  # Adjust the figure size as needed
    sns.heatmap(pivot_result, annot=True, fmt=".2f", cmap="RdYlGn", linewidths=.5)

    # Establecer etiquetas y título
    plt.xlabel('Año')
    plt.ylabel('Mes')
    plt.title('Variación por Año y Mes')
    st.pyplot(fig)
    

data = infoAccion(add_combo)

# Check the conditions and assign values
data['SALIDACORTO'] = 0  # Default value
data.loc[(data['EmaRapida'] > data['EmaMediana']) & (data['EmaRapida'].shift() < data['EmaMediana'].shift()), 'SALIDACORTO'] = 1
data.loc[(data['EmaRapida'] < data['EmaMediana']) & (data['EmaRapida'].shift() > data['EmaMediana'].shift()), 'SALIDACORTO'] = 2

data['SALIDALARGO'] = 0  # Default value
data.loc[(data['EmaLenta'] > data['Ema200']) & (data['EmaLenta'].shift() < data['Ema200'].shift()), 'SALIDALARGO'] = 1
data.loc[(data['EmaLenta'] < data['Ema200']) & (data['EmaLenta'].shift() > data['Ema200'].shift()), 'SALIDALARGO'] = 2

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
st.dataframe(data.tail(10))

#Tendencias en Porcentajes
tendencias = data.iloc[:,-5:-2]
tendencias.dropna(inplace=True)
st.dataframe(tendencias)
fig = plt.figure(figsize=(18,9))
sns.boxplot(tendencias)
st.pyplot(fig)

anual = data
anual['AÑO'] = anual.index.year
anual['MES'] = anual.index.month
anual.dropna(inplace=True)
anual['DIFERENCIA'] = anual['Close'].pct_change()*100
st.dataframe(anual)

col1, col2 = st.columns (2)

with col1:
    calculaMeses(data)