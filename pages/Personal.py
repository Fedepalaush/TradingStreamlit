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
        state.df = pd.DataFrame(columns=['Ticker', 'Cantidad', 'PrecioCompraD','PrecioActualD', 'PrecioCompraP','PrecioActualP', 'DiferenciaP', 'TotalPesos','PCTP' ])



def getIOLData():
    IOLData = pd.read_html('https://iol.invertironline.com/mercado/cotizaciones/argentina/cedears/todos')
    df = IOLData[0]

    # Define a function to split the string and update the DataFrame
    def split_symbol_description(row):
        symbol, description = row['Símbolo'].split(maxsplit=1)
        row['Symbol'] = symbol
        row['Description'] = description
        return row

    # Apply the function to each row of the DataFrame
    df = df.apply(split_symbol_description, axis=1)

    selected_columns = ['Symbol', 'Description', 'Variación Diaria', 'Último Operado']
    subset_df = df[selected_columns]

    return subset_df

# Function to add a new row
def add_row():
    IOLData = getIOLData()
    ticker_value = ticker
    cantidad_value = int(cantidad)
    precio_compra_d_value = float(precio_compra_d)
    precio_compra_p_value = float(precio_compra_p)
    precio_actual = precioActual(IOLData, ticker)
    pct = "{:.2f}%".format(((precio_actual / precio_compra_p_value) - 1) * 100)
    print(precio_actual)

    new_row = {
        'Ticker': ticker_value,
        'Cantidad': cantidad_value,
        'PrecioCompraD': precio_compra_d_value,
        'PrecioCompraP': precio_compra_p_value,
        'PrecioActualD': yf.Ticker(ticker_value).history(period='1d')['Close'].values[0],
        'PrecioActualP': precio_actual,
        'DiferenciaP': precio_actual - precio_compra_p_value ,
        'TotalPesos':cantidad_value * precio_compra_p_value,
        'PCTP':  pct
    }
    state.df.loc[len(state.df)] = new_row
    st.success("New row added successfully.")

def precioActual(df, Ticker):
    for index, row in df.iterrows():
        if row['Symbol'] == Ticker:
            ultimo_operado = row['Último Operado']
            value = ultimo_operado.replace('.', '').replace(',', '.')
            return float(value)

# Function to recalculate 'PrecioActual' and 'Diferencia' for all rows
def recalculate_precio_actual():
    IOLData = getIOLData()
    for i, row in state.df.iterrows():
        ticker_value = row['Ticker']
        precio_actualD = yf.Ticker(ticker_value).history(period='1d')['Close'].values[0]
        precio_actualP = precioActual(IOLData, ticker_value)
        state.df.at[i, 'PrecioActualD'] = precio_actualD
        state.df.at[i, 'PrecioActualP'] = precio_actualP
        state.df.at[i, 'DiferenciaP'] = (precio_actualP * state.df.at[i, 'Cantidad']) - state.df.at[i, 'PrecioCompraP'] * state.df.at[i, 'Cantidad']
        state.df.at[i, 'PCTP'] = "{:.2f}%".format((precio_actualP / state.df.at[i, 'PrecioCompraP'] - 1) * 100)

    st.success("PrecioActual and Diferencia recalculated successfully.")

col1, col2, col3 = st.columns(3)
with col1:
     st.text('Acciones postivas')
     count = (state.df['PCTP'] > '0%').sum()
     st.text(count)
with col2:
     st.text('Acciones negativas')
     count = (state.df['PCTP'] < '0%').sum()
     st.text(count)
with col3:
     st.text('Rendimiento Dolares($)')
    

col1, col2, col3 = st.columns(3)
with col1:
     st.text('Total Invertido')
     count = state.df['TotalPesos'].sum() - state.df['DiferenciaP'].sum()
     formatted_total = f"${count:.2f}"
     st.write(formatted_total)
with col2:
     st.text('Rendimiento Pesos($)')
     total = state.df['DiferenciaP'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)
with col3:
     st.text('Total Actual ($)')
     total = state.df['TotalPesos'].sum()
     formatted_total = f"${total:.2f}"
     st.write(formatted_total)

# Display the DataFrame
st.divider()
st.dataframe(state.df)
recalculate_button = st.button('Recalcular')
st.divider()

for i, row in state.df.iterrows():
    ticker_value = row['Ticker']
    st.text(ticker_value)

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

state.df['TotalPesos'] = state.df['Cantidad'] * state.df['PrecioActualP']
# Save the DataFrame to a CSV file
state.df.to_csv(CSV_FILE_PATH, index=False)

#Change value
#state.df.at[0, 'PrecioCompra'] = 37.88