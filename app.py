# Required imports
import yfinance as yf
import pandas as pd
from scipy.signal import find_peaks
import plotly.graph_objects as go
import streamlit as st

# Streamlit UI - Introduction and How to Use the App
st.markdown("""
# Stock Analysis Tool

Welcome to our stock analysis application, lovingly crafted to provide traders and investors with key insights into market trends, moving averages, and Fibonacci retracement levels.

### What It Does
This tool allows you to:
- View a stock's price movement over time.
- Analyze moving averages (20, 50, 200 periods) to identify trends.
- Utilize Fibonacci retracement levels to spot potential support and resistance areas.

### How to Use
1. Enter a stock symbol in the sidebar.
2. Choose your desired analysis period.
3. Review the plotted stock data and moving averages.
4. Use the Fibonacci levels to identify support and resistance areas.

**Pro Tip from a Seasoned Trader**: *Buy at support levels, and sell at resistance levels.* This strategy leverages the concept that prices tend to bounce off these key levels, offering opportunities for entry and exit.

Let's dive into the analysis!
""")

# User Inputs
sidebar = st.sidebar
symbol = sidebar.text_input("Enter stock symbol:", "AAPL")
period = sidebar.selectbox("Select period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

# Download stock data
data = yf.download(symbol, period=period)

# Calculate Moving Averages
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()
data['MA20'] = data['Close'].rolling(window=20).mean()

# Detecting significant peaks and troughs
peaks, _ = find_peaks(data['Close'], prominence=1)  # Adjust prominence as needed
troughs, _ = find_peaks(-data['Close'], prominence=1)  # Finding troughs by inverting the data

# Plot setup
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='black')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='50-Period MA', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], name='200-Period MA', line=dict(color='red')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='20-Period MA', line=dict(color='green')))

# Handling Fibonacci Levels
if len(peaks) == 0 or len(troughs) == 0:
    fig.add_annotation(xref='paper', yref='paper', x=0.5, y=0.5, text="No significant peaks or troughs detected for Fibonacci analysis", showarrow=False, font=dict(size=20, color="red"))
else:
    high_price = data.iloc[peaks]['Close'].max()
    low_price = data.iloc[troughs]['Close'].min()

    # Fibonacci Levels
    fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    price_diff = high_price - low_price
    for i, level in enumerate(fib_levels):
        data[f'Fib_Level_{i}'] = high_price - price_diff * level

    # Add Fibonacci Levels to the plot
    for i in range(7):
        fig.add_trace(go.Scatter(x=data.index, y=[data[f'Fib_Level_{i}'][0]]*len(data), name=f'Fib Level {fib_levels[i]*100}%', line=dict(dash='dot')))

# Display the chart
st.plotly_chart(fig)
