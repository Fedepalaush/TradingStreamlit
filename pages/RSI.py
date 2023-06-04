from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from datetime import timedelta

with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        ['AAPL', 'MSFT', 'KO', 'BA'],
        index=0 
)

    fechaInicio = st.date_input(
        "Seleccione Fecha Inicio",
        datetime.date.today() - timedelta(days=365))


data = yf. download (add_combo, fechaInicio)
class Rsi(Strategy):
    upper_bound = 66
    lower_bound = 38
    rsi_window = 16
    def init(self):
          self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)
    def next(self):
        if crossover (self.rsi, self .upper_bound):
          self.position.close()
          self.sell(tp=0.9*self.data.Close, sl=1.10*self.data.Close)
        elif crossover (self.lower_bound , self.rsi):
          self.position.close ()
          self.buy (tp=1.5*self.data.Close, sl=0.90*self.data.Close)

bt = Backtest(data, Rsi, cash=1000, commission=.002)        
bt.run()
  
stats, heatmap = bt.optimize(
    upper_bound = range(40,70,2),
    lower_bound = range(30,45,2),
    rsi_window = range (10,20,2),
    maximize= 'Equity Final [$]',
    return_heatmap=True
)

heatmap.unstack()

st.text('ARRIBA ' + str(stats["_strategy"].upper_bound))
st.text('ABAJO ' + str(stats["_strategy"].lower_bound))
st.text('RSI ' + str(stats["_strategy"].rsi_window))
