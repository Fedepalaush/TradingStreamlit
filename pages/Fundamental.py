import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from dataBM import tickersBM

with st.sidebar:
    add_combo = st.selectbox(
        "Seleccione una Acción",
        tickersBM,
        index=0 
)

# Define the ticker symbol
ticker = add_combo

# Get the cashflow data using yfinance
data_cashflow = yf.Ticker(ticker).get_cashflow()
data_balance = yf.Ticker(ticker).get_balance_sheet()
data_income = yf.Ticker(ticker).get_incomestmt()

st.dataframe(data_income)

col1, col2 = st.columns(2)

with col1:
    # Select only the 'FreeCashFlow' row
    flujoCaja = data_cashflow.iloc[:1]

    # Extract the year and free cash flow values
    years = [str(col.year) for col in flujoCaja.columns]
    cashflows = flujoCaja.loc['FreeCashFlow'].tolist()

    # Reverse the lists to change the order
    years = years[::-1]
    cashflows = cashflows[::-1]
    # Create the bar plot
    fig, ax = plt.subplots()
    plt.bar(years, cashflows)
    plt.xlabel('Año')
    plt.ylabel('Flujo de Caja')
    plt.title('Flujo de Caja en Años')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar plot using Streamlit
    st.pyplot(fig)

with col2:
    # Select only the 'TotalRevenue' row
    totalRevenue = data_income.loc['TotalRevenue']

    # Extract the year and revenue values
    years = [str(col.year) for col in totalRevenue.index]
    revenues = totalRevenue.values

    # Reverse the lists to change the order
    years = years[::-1]
    revenues = revenues[::-1]

    # Create the bar plot
    fig, ax = plt.subplots()
    plt.bar(years, revenues)
    plt.xlabel('Año')
    plt.ylabel('Ganancia')
    plt.title('Ganancia Total')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar plot using Streamlit
    st.pyplot(fig)


col3, col4 = st.columns(2)

with col3: 
        # Select only the 'TotalRevenue' row
    netIncome = data_income.loc['NetIncome']

    # Extract the year and revenue values
    years = [str(col.year) for col in netIncome.index]
    incomes = netIncome.values

    # Reverse the lists to change the order
    years = years[::-1]
    revenues = incomes[::-1]

    # Create the bar plot
    fig, ax = plt.subplots()
    plt.bar(years, incomes)
    plt.xlabel('Año')
    plt.ylabel('Ingresos')
    plt.title('Ingresos Netos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar plot using Streamlit
    st.pyplot(fig)