import streamlit as st
import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

data = yf.Ticker('AAPL').history(period='1y')

class RsiOscillator(Strategy):
    
    upper_bound = 42
    lower_bound = 40
    rsi_window = 10

    def init(self):
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_window)

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):    
            self.buy()

class EmaCross(Strategy):
    rapida = 12
    lenta = 22

    def init(self):
        self.ema_rapida = self.I(ta.ema, data.Close, self.rapida)
        self.ema_lenta = self.I(ta.ema, data.Close, self.lenta)
        print(self.ema_lenta)

    def next(self):
        if crossover(self.ema_lenta, self.ema_rapida):
            self.position.close()
        elif crossover(self.ema_rapida, self.ema_lenta):    
            self.buy()

bt = Backtest(data, EmaCross, cash=1000)

""" stats, heatmap = bt.optimize(
    upper_bound = range(55,75,2),
    lower_bound = range(15,35,2),
    rsi_window = range (10,20,2),
    maximize= 'Return [%]',
    return_heatmap=True
) """

stats, heatmap = bt.optimize(
    rapida = range(6,13,1),
    lenta = range(18,24,2),
    maximize= 'Return [%]',
    return_heatmap=True
) 


st.text(str(stats["_strategy"].rapida))         
st.text(str(stats["_strategy"].lenta))         
st.text(stats)         