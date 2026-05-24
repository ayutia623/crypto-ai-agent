import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")
st.title("📊 Pro Crypto Terminal: Advanced Analysis")

# Pengaturan API dari Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

# Fungsi Ambil Data Historis (Agar Grafik Terbentuk)
@st.cache_data(ttl=60) # Cache data agar cepat
def get_market_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    response = requests.get(url).json()
    prices = response['prices']
    return pd.DataFrame(prices, columns=['timestamp', 'price'])

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Real-time Price Chart")
    selected_coin = st.selectbox("Pilih Aset:", ['bitcoin', 'ethereum', 'solana'])
    df = get_market_data(selected_coin)
    
    # Membuat Grafik Plotly Profesional
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], line=dict(color='#00ffcc', width=2))])
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=30, b=20), height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🧠 AI Insights")
    if st.button("Jalankan Analisis Pro"):
        with st.spinner("Mereset pasar..."):
            # 1. Berita
            tavily = TavilyClient(api_key=tavily_key)
            news = tavily.search(query=f"market analysis {selected_coin} May 2026")
            
            # 2. Analisis
            headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": f"Aset: {selected_coin}. Data Harga: {df.tail(5).to_string()}. Berita: {news}. Analisis teknikal & arah tren?"}]
            }
            response = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
            st.write(response['content'][0]['text'])
