import yfinance as yf
import pandas_ta as ta
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dataBM import tickersBM

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

tickers = tickersBM
for ticker in tickers:
    data = yf.Ticker(ticker).history('5y')
    try:
        data.drop(columns=['Dividends','Stock Splits'], inplace=True)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['Ema200'] = ta.ema(data["Close"], length=200)
        data['EmaMediana'] = ta.ema(data["Close"], length=20)

        # Calcular el indicador estocástico
        data['LowestLow'] = data['Low'].rolling(window=14).min()
        data['HighestHigh'] = data['High'].rolling(window=14).max()
        data['Stochastic'] = 100 * ((data['Close'] - data['LowestLow']) / (data['HighestHigh'] - data['LowestLow']))

        if abs(data['Close'].iloc[-1] - data['Ema200'].iloc[-1]) < 0.1 and data['Stochastic'].iloc[-1] < 20:
            st.write('CONDICIÓN CUMPLIDA para', ticker)
            graficoVelas(data)

    except:
        pass