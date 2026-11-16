import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# ==================
# APP
# ==================
# Título de la app
st.title("Calculadora Riesgo Mercado")

# Selección tickers
st.multiselect(label = "tickers", options = ["IVV", "ILF", "SOXX"], key= "tickers", default= "SOXX")
tickers = st.session_state["tickers"]

# Seleccionar pesos
st.multiselect(label = "pesos", options = [0.5, 0.3, 0.2], key= "pesos")
vector_w = st.session_state["pesos"]
vector_w = np.array(vector_w).reshape(-1,1) # Vector de pesos

# Descargar desde Yahoo finance
if len(tickers) > 0: 
    df_prices = yf.download(tickers, start="2024-01-01", end="2026-09-30")["Close"]
    df_prices = df_prices[tickers]
    # st.dataframe(df_prices)

# Calcular retornos diarios
df_ret = df_prices.pct_change().dropna()

# Calcular matriz de varianza covarianza
df_cov = df_ret.cov()
# print(df_cov) # Con este print podemos visualizar en la consola nuestra matriz de varianza-covarianza de nuestro portafolio.

# Calcular varianza del portafolio 
w = vector_w
w_t = w.T
sigma = df_cov.values
varianza = np.dot(sigma, w)
varianza = np.dot(w_t, varianza)[0][0]
desv = varianza**(1/2)
volatilidad_anual = desv * 252**(1/2)
report_volatilidad = f"La volatilidad del portafolio es: {volatilidad_anual*100:.04}%"

st.write(report_volatilidad)

