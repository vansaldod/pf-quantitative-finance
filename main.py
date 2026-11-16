import pandas as pd
import numpy as np
import yfinance as yf

# Descargar precios desde yahoo finance
tickers = ["IVV", "ILF", "SOXX"] # SP500, LATAM, Semiconductores
vector_w = [0.5, 0.3, 0.2] # Lista de pesos del portafolio
vector_w = np.array(vector_w).reshape(-1,1) # Vector de pesos
df_prices = yf.download(tickers, start="2024-01-01", end="2026-09-30")["Close"]
df_prices = df_prices[tickers]

# Calcular retornos diarios
df_ret = df_prices.pct_change().dropna()

# Calcular matriz de varianza covarianza
df_cov = df_ret.cov()
# print(df_cov) # Con este print podemos visualizar en la consola nuestra matriz de varianza-covarianza de nuestro portafolio.

# Calcular varianza del portafolio 
w = vector_w
w_t = w.T
sigma = df_cov.values

# print("w", w.shape) # Con este print se puede visualizar el tamaño de la matriz "w".
# print("w", w_t.shape) # En el caso de este print, se visualiza el tamaño de la matriz "w" traspuesta.
# print("sigma", sigma.shape) # En este último se ve el tamaño de la matriz de los sigmas, que es de 3x3.

varianza = np.dot(sigma, w)
varianza = np.dot(w_t, varianza)
varianza = varianza[0][0]

# Calcular desviación estándar 
desv = varianza**(1/2)
volatilidad_anual = desv * 252**(1/2)
print(f"La volatilidad del portafolio es: {volatilidad_anual*100:.04}%")

# Calcular la media del portafolio
vector_ret = df_ret.mean()
vector_ret = vector_ret.values
vector_ret = vector_ret.reshape(-1,1)
mu = np.dot(w_t, vector_ret)[0][0]
mu_anual = mu * 252
# print(f"La media anual del portafolio es: {mu_anual*100:.04}%") # Con este print se obtiene el resultado de la media anualizada de nuestro portafolio.

# Calcular Value at Risk (VaR) al 95% de confianza
var_95 = mu_anual - 1.64 * volatilidad_anual
print(f"La VaR anual del portafolio es: {var_95*100:.04}%")

# FIRMA: ag2FuyTVRz1F2LjmTT9rqeq2BWKxuGhzCl_SS5A4FUxQPUW5JuyFgv4LC49VucTX_FjjlAeFv7J_NV2voFsFADIeYgcnQYJmvA==
