import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="DEMA Scanner")

st.title("NIFTY50 DEMA Scanner")

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

results = []

for stock in stocks:

    try:
        df = yf.download(
            stock,
            period="5d",
            interval="15m",
            progress=False
        )

        if df.empty:
            continue

        close = df["Close"]

        ema1 = close.ewm(span=100, adjust=False).mean()
        ema2 = ema1.ewm(span=100, adjust=False).mean()

        dema = 2 * ema1 - ema2

        latest_price = float(close.iloc[-1])
        latest_dema = float(dema.iloc[-1])

        signal = "BUY" if latest_price > latest_dema else "SELL"

        results.append({
            "Stock": stock,
            "Price": round(latest_price, 2),
            "DEMA100": round(latest_dema, 2),
            "Signal": signal
        })

    except Exception as e:
        st.write(f"Error in {stock}: {e}")

table = pd.DataFrame(results)

st.dataframe(table, use_container_width=True)