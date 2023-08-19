import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import yfinance as yf
import pandas_ta as ta


tickers = 'SPY QQQ'

data = yf.download(
    tickers= tickers,
    period= 'max',
    interval= '1d',
    ignore_tz=True,
    auto_adjust=True,
)

data = data['Close']
data = data['20050101':]


def get_signal(data, ticker, fast_ma, slow_ma):

    close_adj = data[[ticker]].copy()
    close_adj.columns = ['close']

    close_adj['R'] = close_adj.close.pct_change().fillna(0)

    #Define indicators
    close_adj['slow_ma'] = ta.ema(close_adj["close"], length=slow_ma)
    close_adj['fast_ma'] = ta.ema(close_adj["close"], length=fast_ma)

    #Compute Signals
    close_adj = close_adj[~close_adj.slow_ma.isnull()]

    close_adj = close_adj.assign(
        signal = lambda x : np.where(x.fast_ma > x.slow_ma,1,0)
    )
    close_adj['signal'] = close_adj['signal'].shift(1, fill_value=0)
    close_adj['R_strategy'] = close_adj.R * close_adj.signal

    return close_adj

ticker = "SPY"
df_signal = get_signal(data, ticker, fast_ma=10, slow_ma=65)

#Retorno total
print(100 * (1+df_signal[['R', 'R_strategy']]).prod()-1)

cumulative_returns = 100 * (1 + df_signal[['R', 'R_strategy']]).cumprod()

# Create a Plotly line chart for cumulative returns
st.write("Cumulative Returns")
fig_cum_returns = px.line(cumulative_returns, title='Total Returns')
st.plotly_chart(fig_cum_returns)


def performance(df_signal, ticker, freq='M', risk_free_rate=0.02):

    rets = df_signal[['R', 'R_strategy']].copy()
    rets.columns = ['Buy and Hold', 'Estrategia']

    if freq == 'D':
        scale = 252
    elif freq == 'M':
        scale = 12
        rets = rets.resample(freq).agg(lambda x: (1 + x).prod() - 1 )
    else:
        return None        
    
    #Compute Results
    ret_cumulative = (1+rets).cumprod()
    previous_peaks = ret_cumulative.cummax()
    drawdown = (ret_cumulative - previous_peaks) / previous_peaks

    #Compute annualizd returns and risk
    annualized_returns = (1 + rets.mean())**scale-1
    annualized_std_deviation = rets.std() *np.sqrt(scale)
    max_drawdown = drawdown.min() * -1

    df_risk_return = pd.DataFrame(
        dict(
        ticker = ticker,
        annualized_returns=annualized_returns,
        annualized_std_deviation=annualized_std_deviation,
        )
    )

    df_risk_return['Max Drawdown'] = drawdown.min() * -1

    #Compute Sharpe Ratio
    df_risk_return = df_risk_return.assign(
        sharpe_ratio = lambda x: (x.annualized_returns-risk_free_rate)/x.annualized_std_deviation,
        calmar_ratio=lambda x: (x.annualized_returns)/x['Max Drawdown'],
    )
    return df_risk_return


results = []
for fast_ma in range (5,50,5):
    for slow_ma in range (30,200,5):
        if fast_ma >= slow_ma:
            continue
        else:
            #Compute Signal
            df_signal = get_signal(data,ticker,fast_ma,slow_ma)

            #Compute Performance
            perf = performance(df_signal, ticker, freq='D', risk_free_rate=0.02)

            perf['fast_ma'] = fast_ma
            perf['slow_ma'] = slow_ma
            results.append(perf.tail(1))

df_res = pd.concat(results)
df_res.sort_values('calmar_ratio', ascending=False).head()

st.dataframe(df_res)

#eval_metric ='annualized_returns'
eval_metric = 'calmar_ratio'
#eval_metric = 'sharpe_ratio'

df_mat = df_res.pivot(index='fast_ma', columns='slow_ma', values = eval_metric)

fig = px.imshow(df_mat,
                color_continuous_scale='RdYlGn',
                aspect='auto')
fig.update_layout(
    title = eval_metric,
    xaxis_title='Slow EMA',
    yaxis_title = 'Fast EMA'
)
st.plotly_chart(fig)
