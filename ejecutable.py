import streamlit as st
import pandas as pd
import yfinance as yf


# Using "with" notation
with st.sidebar:
    add_radio = st.selectbox(
        "Seleccione plazo en años",
        range (1,31),
        index=29)
    
    add_combo = st.selectbox(
        "Seleccione una opción",
        ['AAPL', 'MSFT', 'KO', 'BA'],
        index=0 
)

data = yf.Ticker(add_combo).history(period=f'{add_radio}y')

st.dataframe(data.tail(40))

latest_day_data = data.iloc[-1].Close
st.text(f"Price: ${latest_day_data:.2f}")

st.subheader("Historical Data")
st.line_chart(data["Close"])
