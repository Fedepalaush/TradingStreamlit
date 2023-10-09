import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

data = yf.Ticker('AAPL').history('5y')

train = data.iloc[:-20]
st.dataframe(train)

test = data.iloc[-20:]
st.dataframe(test)

real_stock_price = test.iloc[:, 1:2].values
st.dataframe(real_stock_price)

# Obtener las columnas 'Open', 'Close' y 'Volume' para el conjunto de entrenamiento
training_set = train.iloc[:, 1:2].values
st.dataframe(training_set)
st.text(training_set.shape)

# Escalado de Características
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

# Crear una estructura de datos con 60 Timesteps y 1 salida
X_train = []
y_train = []
for i in range(60, 1237):
    X_train.append(training_set_scaled[i-60:i, :])
    y_train.append(training_set_scaled[i, 0])  # Usar el precio de cierre
X_train, y_train = np.array(X_train), np.array(y_train)    

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))  # 3 características: Open, Close, Volume


# Construcción de la RNR
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
# Inicialización del modelo
regressor = Sequential()

# Añadir Capa LSTM
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam', loss='mean_squared_error')

regressor.fit(X_train, y_train, epochs=100, batch_size=32)



# Preparar los datos de prueba
data = data.iloc[:,1:2]
real_stock_price = test.iloc[:, 1:2].values 
inputs = data[len(data) - len(test) - 60: ].values
inputs.reshape(-1,1)
inputs = sc.transform(inputs)



X_test = []


for i in range(60, 80):
    X_test.append(inputs[i-60:i, :])  # Utilizar las tres características
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))  # 3 características: Open, Close, Volume

print('XTEST')
print(X_test)
print(X_test.shape)
# Obtener los precios predichos
predicted_stock_price = regressor.predict(X_test)


predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Visualizar
plt.plot(real_stock_price, color='red', label='Precio Real de la Accion')
plt.plot(predicted_stock_price, color='blue', label='Precio Predicho de la Accion')
plt.title('Prediccion de una RNR')
plt.xlabel('Fecha')
plt.ylabel('Precio de la Accion')
plt.legend()

st.pyplot()