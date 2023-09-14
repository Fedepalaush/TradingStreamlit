import streamlit as st
import pandas as pd
import yfinance as yf
import os
from Principal import infoAccion

from streamlit import session_state as state

# Define the path to the CSV file
CSV_FILE_PATH = 'data.csv'
CSV_FILE_PATH_RATIOS = 'ratios.csv'

# Check if the DataFrame is stored in session state
if 'df' not in state:
    # Load the DataFrame from the CSV file if it exists
    if os.path.isfile(CSV_FILE_PATH):
        state.df = pd.read_csv(CSV_FILE_PATH)
    else:
        # Create an empty DataFrame if it doesn't exist
        state.df = pd.DataFrame(columns=['Ticker', 'Cantidad', 'PrecioCompra', 'PrecioActual', 'PCT', 'Ratio', 'Total', 'TotalIndividual' ])

if 'ratios' not in state:
    # Load the DataFrame from the CSV file if it exists
    if os.path.isfile(CSV_FILE_PATH_RATIOS):
        state.ratios = pd.read_csv(CSV_FILE_PATH_RATIOS)



# Function to add a new row
def add_row(ticker_value, cantidad_value, precio_compra):
    ticker_value = ticker
    cantidad_value = int(cantidad)
    precio_compra = float(precio_compra)
    precio_actual = yf.Ticker(ticker_value).history(period='1d')['Close'].values[0]
    pct = "{:.2f}%".format(((precio_actual / precio_compra) - 1) * 100)
    ratio = st.session_state.ratios[st.session_state.ratios['ticker']==ticker]['Ratio Cedear']
    total = float((precio_actual /ratio.values[0] ) * cantidad_value)
    totalIndividual = (((total)/(float((precio_compra /ratio.values[0] ) * cantidad_value))-1)*100)
    

    new_row = {
        'Ticker': ticker_value,
        'Cantidad': cantidad_value,
        'PrecioCompra': precio_compra,
        'PrecioActual': yf.Ticker(ticker_value).history(period='1d')['Close'].values[0],
        'PCT':  pct,
        'Ratio' : ratio.values[0],
        'Total' : total,
        'TotalIndividual' : totalIndividual

    }
    state.df.loc[len(state.df)] = new_row
    st.success("Acción Agregada")
    st.experimental_rerun()


# Function to recalculate 'PrecioActual' and 'Diferencia' for all rows
def recalculate_precio_actual():

    for i, row in state.df.iterrows():
        ticker_value = row['Ticker']
        precio_actual = yf.Ticker(ticker_value).history(period='1d')['Close'].values[0]
        state.df.at[i, 'PrecioActual'] = precio_actual
        state.df.at[i, 'PCT'] = "{:.2f}%".format((precio_actual / state.df.at[i, 'PrecioCompra'] - 1) * 100)
        state.df.at[i, 'Total'] = float((precio_actual /state.df.at[i, 'Ratio'] ) * state.df.at[i, 'Cantidad'])
        state.df.at[i, 'TotalIndividual'] =((precio_actual /state.df.at[i, 'Ratio'] ) * state.df.at[i, 'Cantidad']) /  ((state.df.at[i, 'PrecioCompra'] /state.df.at[i, 'Ratio']) * state.df.at[i, 'Cantidad']) 

    st.success("Precio Actual and Diferencia recalculated successfully.")

col1, col2, col3 = st.columns(3)
with col1:
     st.text('Acciones postivas')
     count = (state.df['PCT'] > '0%').sum()
     st.text(count)
with col2:
     st.text('Acciones negativas')
     count = (state.df['PCT'] < '0%').sum()
     st.text(count)
with col3:
     st.text('Rendimiento Dolares($)')

    

col1, col2, col3 = st.columns(3)
with col1:
     st.text('Total Invertido')
     #count = state.df['Total'].sum() - state.df['Diferencia'].sum()
     count=0
     formatted_total = f"${count:.2f}"
     st.write(formatted_total)
with col2:
     st.text('Rendimiento Pesos($)')
     #total = state.df['Diferencia'].sum()
     #formatted_total = f"${total:.2f}"
     formatted_total = 0
     st.write(formatted_total)
with col3:
     st.text('Total Actual ($)')
     total = state.df['Total'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)

# Display the DataFrame
st.divider()
st.dataframe(state.df)
recalculate_button = st.button('Recalcular')
st.divider()


for i, row in state.df.iterrows():
    ticker_value = row['Ticker']
    data = infoAccion(ticker_value)
    data.dropna(inplace=True)

    # Add the first text value in the center
    st.subheader(ticker_value)

    # Use Streamlit's columns to create three equal-width columns
    col1, col2, col3 = st.columns(3)

    # Add the remaining three text values in the three columns
    col1.text('EMA200')
    if data.iloc[i]['Close'] > data.iloc[i]['Ema200']:
        arrow = '↑'  # Up arrow symbol
    else:
        arrow = '↓'  # Down arrow symbol
    col1.text(arrow)
    col2.text('DIF EMA')
    col2.text(str(data.iloc[-1]['RSI']))
    col3.text('RSI')
    col3.text( str(data.iloc[-1]['RSI']))


st.divider()

# Create two columns
col1, col2 = st.columns(2)


# Create text input widgets in the first column
with col1:
    st.text('Agregar Accion')
    ticker = st.text_input('Ticker')
    cantidad = st.text_input('Cantidad')
    precio_compra = st.text_input('Precio Compra Dolar')

    col11, col12 = st.columns(2)
    with col11:
     button = st.button('Agregar')

# Create text input widgets in the second column
with col2:
    st.text('Vender Accion')
    tickerVenta = st.text_input('Ticker Venta')
    cantidad = st.text_input('Cantidad Venta')

    col11, col12 = st.columns(2)
    with col11:
     buttonVender = st.button('Venta')
   

# Check if the button is clicked
if button:
    add_row(ticker, cantidad, precio_compra)

# Check if the button is clicked
if buttonVender:
    add_row(tickerVenta, cantidad, precio_compra)

# Check if the recalculate button is clicked
if recalculate_button:
    recalculate_precio_actual()

state.df['Total'] = (state.df['PrecioActual'] /state.df['Ratio'] ) * state.df['Cantidad']
# Save the DataFrame to a CSV file
state.df.to_csv(CSV_FILE_PATH, index=False)

#Change value
#state.df.at[0, 'PrecioCompra'] = 37.88