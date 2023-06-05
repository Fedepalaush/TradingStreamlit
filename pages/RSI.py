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
from dataBM import tickersBM

with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        tickersBM,
        index=0 
)

    fechaInicio = st.date_input(
        "Seleccione Fecha Inicio",
        datetime.date.today() - timedelta(days=365))


    # Add a slider with two values
    min_max = st.slider("Seleccione niveles minimos y máximos", 20, 70, (40, 50), 2)
    ventana = st.slider("Ventana RSI", min_value=7, max_value=21, value=14, step=1)

    

data = yf. download (add_combo, fechaInicio)
class Rsi(Strategy):
    upper_bound = min_max[1]
    lower_bound = min_max[0]
    rsi_window = ventana
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
retorno_final = "{:.2f}%".format(round(stats['Return [%]'], 2))
heatmap.unstack()

st.text('Arriba ' + str(stats["_strategy"].upper_bound))
st.text('Abajo ' + str(stats["_strategy"].lower_bound))
st.text('Ventana ' + str(stats["_strategy"].rsi_window))
st.text('Retorno ' + str(retorno_final))

st.button('Graficar', on_click=bt.plot)

print(stats)