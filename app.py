import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")
st.title("🚀 Pro Crypto Terminal v2.0")

# Ambil dari Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

# Fungsi Data Historis
@st.cache_data(ttl=60)
def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Layout Dashbord
col1, col2 = st.columns([2, 1])

with col1:
    coin = st.selectbox("Pilih Aset untuk Analisis:", ['bitcoin', 'ethereum', 'solana'])
    df = get_data(coin)
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], mode='lines', line=dict(color='#00ffcc'))])
    fig.update_layout(template="plotly_dark", title=f"Pergerakan {coin.upper()} 24 Jam Terakhir")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🤖 Agensi AI")
    if st.button("Jalankan Analisis Lengkap"):
        with st.spinner("Menggabungkan data teknikal, berita, dan sentimen..."):
            # 1. Riset
            tavily = TavilyClient(api_key=tavily_key)
            news = tavily.search(query=f"latest news and market sentiment for {coin} May 2026")
            
            # 2. Analisis Claude
            headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
            prompt = f"""
            Aset: {coin}. Harga saat ini: {df['price'].iloc[-1]}. 
            Data 24 jam terakhir: {df.tail(10).to_string()}. 
            Berita terbaru: {news}. 
            Tugas: Berikan analisis komprehensif, hitung volatilitas, dan berikan rekomendasi (Beli/Hold/Jual) dengan alasan yang logis.
            """
            payload = {"model": model_name, "messages": [{"role": "user", "content": prompt}]}
            response = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
            st.write(response['content'][0]['text'])

st.info("Fitur Baru: Sekarang AI memantau data historis 24 jam terakhir untuk memberikan rekomendasi yang lebih presisi.")
