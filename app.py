import streamlit as st
import yfinance as yf

st.title("NIFTY50 DEMA Scanner")

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

results = []

for s in stocks:
    df = yf.download(s, period="5d", interval="15m")

    close = df['Close']

    ema = close.ewm(span=100).mean()
    dema = 2 * ema - ema.ewm(span=100).mean()

    signal = "BUY" if close.iloc[-1] > dema.iloc[-1] else "SELL"

    results.append({
        "Stock": s,
        "Signal": signal
    })

st.table(results)