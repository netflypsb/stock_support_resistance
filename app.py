import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# Place input fields in the sidebar
sidebar = st.sidebar
symbol = sidebar.text_input("Enter stock symbol:", "AAPL")
period = sidebar.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

# Download stock data
data = yf.download(symbol, period=period)

# Calculate Moving Averages
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()
data['MA20'] = data['Close'].rolling(window=20).mean()

# Finding highest and lowest price for the Fibonacci Retracement Levels
high_price = data['High'].max()
low_price = data['Low'].min()

# Calculate Fibonacci Levels
fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
price_diff = high_price - low_price
data['Fib_Level_0'] = high_price
data['Fib_Level_1'] = high_price - price_diff * fib_levels[1]
data['Fib_Level_2'] = high_price - price_diff * fib_levels[2]
data['Fib_Level_3'] = high_price - price_diff * fib_levels[3]
data['Fib_Level_4'] = high_price - price_diff * fib_levels[4]
data['Fib_Level_5'] = high_price - price_diff * fib_levels[5]
data['Fib_Level_6'] = low_price

# Plotting
fig = go.Figure()

# Add traces for Close price and MAs
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='black')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='50-Period MA', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], name='200-Period MA', line=dict(color='red')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='20-Period MA', line=dict(color='green')))

# Add traces for Fibonacci Levels
for i in range(7):
    fig.add_trace(go.Scatter(x=data.index, y=[data[f'Fib_Level_{i}'][0]]*len(data), name=f'Fib Level {fib_levels[i]*100}%', line=dict(dash='dot')))

# Display the chart
st.plotly_chart(fig)

# Note: This implementation assumes a simplistic approach to finding the high and low points for Fibonacci retracement levels. 
# In practice, these should be determined based on significant peaks and troughs within a specific period of interest.
