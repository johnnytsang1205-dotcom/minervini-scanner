import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Mark Minervini 趨勢模板篩選器")
st.write("今日掃描名單：AAPL, MSFT, NVDA, TSLA, META (示範測試)")

tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "META"]
results = []

st.write("⏳ 正在讀取數據，請稍候...")

for ticker in tickers:
    try:
        df = yf.Ticker(ticker).history(period="1y")
        if len(df) < 200: 
            continue
            
        close = df['Close'].iloc[-1]
        sma50 = df['Close'].rolling(50).mean().iloc[-1]
        sma150 = df['Close'].rolling(150).mean().iloc[-1]
        sma200 = df['Close'].rolling(200).mean().iloc[-1]
        low_52w = df['Low'].rolling(252, min_periods=200).min().iloc[-1]
        high_52w = df['High'].rolling(252, min_periods=200).max().iloc[-1]
        sma200_20d = df['Close'].rolling(200).mean().iloc[-20]
        
        c1 = close > sma150 and close > sma200
        c2 = sma150 > sma200
        c3 = sma200 > sma200_20d
        c4 = sma50 > sma150 and sma50 > sma200
        c5 = close > sma50
        c6 = close >= (low_52w * 1.3)
        c7 = close >= (high_52w * 0.75)
        
        if c1 and c2 and c3 and c4 and c5 and c6 and c7:
            results.append({
                "股票代號": ticker, 
                "最新收盤價": round(close, 2), 
                "距離52週高位(%)": round((close - high_52w) / high_52w * 100, 2)
            })
    except:
        pass

if results:
    st.success("✅ 今日篩選完成！以下股票符合條件：")
    st.dataframe(pd.DataFrame(results))
else:
    st.warning("今日名單中沒有股票符合所有條件。")

