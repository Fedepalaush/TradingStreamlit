import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time 

chrome_options = Options()
chrome_service = Service("path")

st.title("Web Scraping with Selenium and Streamlit")


def scrape_website():
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    url = "https://quicktrade.com.ar/Bursatil/Cotizacion/Cedears/"
    driver.get(url)
    time.sleep(3)
    #Todas las acciones del Cedears
    acciones = driver.find_elements(By.CLASS_NAME, 'Simbolo')
    driver.quit()
    for accion in acciones:
        print(accion.get_attribute("value"))

st.title("Web Scraping with Selenium and Streamlit")

if st.button("Scrape Website"):
    scrape_website()
    st.success("Scraping completed successfully!")    