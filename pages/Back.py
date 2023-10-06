import streamlit as st
import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import datetime, timedelta

tickers= ['AAPL', 'MSFT', 'BABA', 'BA']
estrategias = ['Cruce EMA', 'RSI']

#Variables Usadas
upper = 70
lower = 30
ventana = 14

ema_rapida = 9
ema_lenta = 21

# Sidebar
st.sidebar.header("Indicadores")
estrategia = st.sidebar.selectbox("Seleccione una Estrategia",estrategias )
ticker = st.sidebar.selectbox("Seleccione una Accion", tickers)
# Fecha de inicio
fechaInicio = st.sidebar.date_input(
        "Seleccione Fecha Inicio",
        datetime.today() - timedelta(days=365))


fechaFin = st.sidebar.date_input(
        "Seleccione Fecha de Fin",
        datetime.today())


# Retrieve historical data using yfinance with specified start and end dates
data = yf.Ticker(ticker).history(start=fechaInicio, end=fechaFin)

if estrategia == 'Cruce EMA':
    ema_rapida = st.sidebar.slider("Rapida", 6, 13, 9)
    ema_lenta = st.sidebar.slider("Lenta", 18, 24, 21)
elif estrategia == 'RSI':
    upper = st.sidebar.slider("Upper", 60,80,70)
    lower = st.sidebar.slider("Lower", 20,40,30)
    ventana = st.sidebar.slider("Ventana", 10, 16, 14)
    
execute_button = st.sidebar.button("Ejecutar")


class RsiOscillator(Strategy):
    
    upper_bound = upper
    lower_bound = lower
    rsi_window = ventana

    def init(self):
        self.rsi = self.I(ta.rsi, data.Close, self.rsi_window)

    def next(self):
        if crossover(self.upper_bound,self.rsi):
            self.position.close()
        if crossover(self.rsi, self.lower_bound):
            self.buy()

class EmaCross(Strategy):
    rapida = ema_rapida
    lenta = ema_lenta

    def init(self):
        self.ema_rapida = self.I(ta.ema, data.Close, self.rapida)
        self.ema_lenta = self.I(ta.ema, data.Close, self.lenta)
        print(self.ema_lenta)

    def next(self):
        if crossover(self.ema_lenta, self.ema_rapida):
            self.position.close()
        elif crossover(self.ema_rapida, self.ema_lenta):    
            self.buy()

if execute_button:
    if estrategia == 'Cruce EMA': 
        bt = Backtest(data, EmaCross, cash=1000)
        stats, heatmap = bt.optimize(
        rapida = range(6,13,1),
        lenta = range(18,24,2),
        maximize= 'Return [%]',
        return_heatmap=True
        ) 
    elif estrategia == 'RSI':
        bt = Backtest(data, RsiOscillator, cash=1000)
        stats, heatmap = bt.optimize(
        upper_bound = range(60,80,1),
        lower_bound = range(20,30,1),
        rsi_window= range(10,16,1),
        maximize= 'Return [%]',
        return_heatmap=True
        ) 





   # st.text(str(stats["_strategy"].rapida))         
   # st.text(str(stats["_strategy"].lenta))         
    st.text(stats)         