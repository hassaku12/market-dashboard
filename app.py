import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd

st.set_page_config(page_title="Intelligence Dashboard", layout="wide")

st.title("📊 Intelligence Dashboard")

# --- 1. マーケット指標の定義 ---
# 日本国債10年はデータソースによりシンボルが不安定なため、
# yfinanceで安定している代表的なシンボルをセットしています
tickers = {
    "ドル円": "JPY=X",
    "日経平均": "^N225",
    "NYダウ": "^DJI",
    "NASDAQ": "^IXIC",
    "米国債10年": "^TNX",
    "日本国債10年": "GJGB10Y.SG", # または ^JGB10Y-SG
    "金先物": "GC=F"
}

# 4列レイアウトで指標を表示
cols = st.columns(4)

for i, (name, sym) in enumerate(tickers.items()):
    with cols[i % 4]:
        try:
            # 前日差を計算するために2日分取得
            data = yf.Ticker(sym).history(period="2d")
            if not data.empty and len(data) >= 2:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2]
                delta = current - prev
                
                # 表示形式の調整（金利やドル円は小数点2桁、株価はカンマ区切り）
                if "10年" in name or "ドル円" in name:
                    val_str = f"{current:.2f}"
                    delta_str = f"{delta:.2f}"
                else:
                    val_str = f"{current:,.0f}"
                    delta_str = f"{delta:,.0f}"
                
                st.metric(label=name, value=val_str, delta=delta_str)
        except:
            st.caption(f"{name}: 取得エラー")

st.divider()

# --- 2. ニュース・トレンドセクション ---
col_news1, col_news2 = st.columns(2)

def display_rss(url, title, count=5):
    st.subheader(title)
    feed = feedparser.parse(url)
    for entry in feed.entries[:count]:
        st.markdown(f"・ [{entry.title}]({entry.link})")

with col_news1:
    # Googleニュースの「ビジネス」カテゴリ
    display_rss("https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ja&gl=JP&ceid=JP:ja", "🏦 マーケット変動要因")
    
    # AI関連（キーワード検索RSS）
    display_rss("https://news.google.com/rss/search?q=Generative+AI+OR+LLM+OR+NVIDIA&hl=ja&gl=JP&ceid=JP:ja", "🤖 AI関連ニュース")

with col_news2:
    # Googleニュースの「テクノロジー」カテゴリ（社会トレンドの代替）
    display_rss("https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja", "📈 社会・ITトレンド")
