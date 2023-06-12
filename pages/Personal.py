import streamlit as st
import pandas as pd
import yfinance as yf
import os


from streamlit import session_state as state

# Define the path to the CSV file
CSV_FILE_PATH = 'data.csv'

# Check if the DataFrame is stored in session state
if 'df' not in state:
    # Load the DataFrame from the CSV file if it exists
    if os.path.isfile(CSV_FILE_PATH):
        state.df = pd.read_csv(CSV_FILE_PATH)
    else:
        # Create an empty DataFrame if it doesn't exist
        state.df = pd.DataFrame(columns=['Ticker', 'Cantidad', 'PrecioCompraD','PrecioCompraP', 'PrecioActual', 'Diferencia', 'PCT'])

# Function to add a new row
def add_row():
    ticker_value = ticker
    cantidad_value = int(cantidad)
    precio_compra_d_value = float(precio_compra_d)
    precio_compra_p_value = float(precio_compra_d)

    new_row = {
        'Ticker': ticker_value,
        'Cantidad': cantidad_value,
        'PrecioCompraD': precio_compra_d_value,
        'PrecioCompraP': precio_compra_p_value,
        'PrecioActual': yf.Ticker(ticker_value).history(period='1d')['Close'].values[0],
        'Diferencia': None,
        'PCT': None
    }
    state.df.loc[len(state.df)] = new_row
    st.success("New row added successfully.")

# Function to recalculate 'PrecioActual' and 'Diferencia' for all rows
def recalculate_precio_actual():
    for i, row in state.df.iterrows():
        ticker_value = row['Ticker']
        precio_actual = yf.Ticker(ticker_value).history(period='1d')['Close'].values[0]
        state.df.at[i, 'PrecioActual'] = precio_actual
        state.df.at[i, 'Diferencia'] = precio_actual - state.df.at[i, 'PrecioCompra']
        state.df.at[i, 'PCT'] = "{:.2f}%".format((precio_actual / state.df.at[i, 'PrecioCompra'] - 1) * 100)
    st.success("PrecioActual and Diferencia recalculated successfully.")

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
     total = state.df['Diferencia'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)

col1, col2, col3 = st.columns(3)
with col1:
     st.text('Total Invertido')
     count = state.df['TotalPesos'].sum()
     formatted_total = f"${count:.2f}"
     st.write(formatted_total)
with col2:
     st.text('Rendimiento Pesos($)')
     total = state.df['Diferencia'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)
with col3:
     st.text('Rendimiento Actual ($)')
     total = state.df['Diferencia'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)

# Display the DataFrame
st.divider()
st.dataframe(state.df)
recalculate_button = st.button('Recalcular')
st.divider()
# Create two columns
col1, col2 = st.columns(2)

# Create text input widgets in the first column
with col1:
    st.text('Agregar Accion')
    ticker = st.text_input('Ticker')
    cantidad = st.text_input('Cantidad')
    precio_compra_d = st.text_input('Precio Compra Dolar')
    precio_compra_p = st.text_input('Precio Compra Pesos')

    col11, col12 = st.columns(2)
    with col11:
     button = st.button('Agregar')
   

# Check if the button is clicked
if button:
    add_row()

# Check if the recalculate button is clicked
if recalculate_button:
    recalculate_precio_actual()

state.df['TotalPesos'] = state.df['Cantidad'] * state.df['PrecioCompraP']
# Save the DataFrame to a CSV file
state.df.to_csv(CSV_FILE_PATH, index=False)

#Change value
#state.df.at[0, 'PrecioCompra'] = 37.88