from math import sqrt
import pandas as pd 
from sklearn.cluster import KMeans
import yfinance as yf
import matplotlib.pyplot as plt
from dataBM import tickersBM 

plt.rc('font', size=10)

tickers = tickersBM[:25]

print(tickers)

data = yf.Ticker('AAPL').history(period='max')
data=data.tolist()
print(data)

moments = (
    data
    .pct_change()
    .describe()
    .T[{"mean", "std"}]
    .rename(columns={'mean':'returns', "std":"vol"})
)  * [252,sqrt(252)]


print(moments)

