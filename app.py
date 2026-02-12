import streamlit as st
import yfinance as yf
import feedparser

st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("📊 Market Intelligence Dashboard")

# --- 1. 指標データの取得と表示 ---
# 前日比を計算するため2日分取得
tickers = {
    "ドル円": "JPY=X", "日経平均": "^N225", "NYダウ": "^DJI",
    "NASDAQ": "^IXIC", "米10年債": "^TNX", "日10年債": "GJGB10Y.SG"
}

cols = st.columns(4)

# 基本指数の表示
for i, (name, sym) in enumerate(tickers.items()):
    with cols[i % 4]:
        data = yf.Ticker(sym).history(period="2d")
        if len(data) >= 2:
            current = data['Close'].iloc[-1]
            delta = current - data['Close'].iloc[-2]
            fmt = ".2f" if "10年" in name or "ドル円" in name else ",.0f"
            st.metric(name, f"{current:{fmt}}", f"{delta:{fmt}}")

# --- 2. 金価格（円建て/g）の計算と表示 ---
with cols[2]: # 空いている3列目に配置
    try:
        gold_data = yf.Ticker("GC=F").history(period="2d")
        fx_data = yf.Ticker("JPY=X").history(period="2d")
        
        # 現在と前日の価格を計算
        g_now = (gold_data['Close'].iloc[-1] * fx_data['Close'].iloc[-1]) / 31.1035
        g_prev = (gold_data['Close'].iloc[-2] * fx_data['Close'].iloc[-2]) / 31.1035
        st.metric("金 (円建て/g)", f"{g_now:,.0f}円", f"{g_now - g_prev:,.0f}円")
    except:
        st.caption("金価格計算エラー")

st.divider()

# --- 3. 投資に役立つニュースの絞り込み ---
col_n1, col_n2 = st.columns(2)

def show_news(url, title):
    st.subheader(title)
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        st.write(f"・ [{entry.title}]({entry.link})")

with col_n1:
    # 市場全体を動かすマクロ要因（FOMCや日銀など）
    show_news("https://news.google.com/rss/search?q=FOMC+OR+日銀+OR+雇用統計+OR+CPI&hl=ja&gl=JP&ceid=JP:ja", "⚖️ 市場変動・マクロ要因")

with col_n2:
    # 成長の源泉となるテック・AIトレンド
    show_news("https://news.google.com/rss/search?q=NVIDIA+OR+OpenAI+OR+半導体+OR+Generative+AI&hl=ja&gl=JP&ceid=JP:ja", "🤖 テック・AIトレンド")
