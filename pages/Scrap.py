import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from streamlit import session_state as state
import os

# Define the path to the CSV file
CSV_FILE_PATH = 'ratios.csv'

# Check if the DataFrame is stored in session state
if 'ratios' not in state:
    # Load the DataFrame from the CSV file if it exists
    if os.path.isfile(CSV_FILE_PATH):
        state.ratios = pd.read_csv(CSV_FILE_PATH)
    else:
        # Create an empty DataFrame if it doesn't exist
        state.ratios = pd.DataFrame()

st.title("Web Scraping with Selenium and Streamlit")

def scrape_website():
    url = 'https://www.comafi.com.ar/custodiaglobal/2483-Programas-Cedear.note.aspx'
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table on the page (use 'Inspect Element' in your browser to identify the table tag)
    table = soup.find('table')

    # Read the table into a Pandas DataFrame
    df = pd.read_html(str(table))[0]
    df.dropna(how='all', inplace=True)
    print(df.columns)
    df = df[['Id  de  mercado','Ratio  Cedear  /  valor  sub-yacente']]
    df.rename(columns={'Id  de  mercado': 'ticker', 'Ratio  Cedear  /  valor  sub-yacente': 'ratio'}, inplace=True)

    # Separate the values in the 'Ratio Cedear / valor sub-yacente' column into two columns
    df[['Ratio Cedear', 'Valor sub-yacente']] = df['ratio'].str.split(':', expand=True)

    # Convert the new columns to integers
    df['Ratio Cedear'] = df['Ratio Cedear'].astype(int)
    df['Valor sub-yacente'] = df['Valor sub-yacente'].astype(int)

    # Drop the original 'Ratio Cedear / valor sub-yacente' column
    df.drop('ratio', axis=1, inplace=True)

    # Now, you have the data in the 'df' DataFrame with the values separated into different columns
    print(df)
    st.dataframe(df)
    st.session_state.ratios = df

if st.button("Scrape Website"):
    scrape_website()
    st.success("Scraping completed successfully!")

state.ratios.to_csv(CSV_FILE_PATH, index=False)