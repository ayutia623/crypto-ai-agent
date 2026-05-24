import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Command Center", layout="wide")
st.title("🚀 Crypto Command Center v3.0")

# Ambil dari Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

@st.cache_data(ttl=60)
def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    response = requests.get(url).json()
    df = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Layout Utama
coin = st.sidebar.selectbox("Pilih Aset:", ['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple'])
df = get_data(coin)

# Statistik Cepat (Cards)
col1, col2, col3 = st.columns(3)
current_price = df['price'].iloc[-1]
change = ((current_price - df['price'].iloc[0]) / df['price'].iloc[0]) * 100
col1.metric("Harga Saat Ini", f"${current_price:,.2f}", f"{change:.2f}%")
col2.metric("Harga Tertinggi (24h)", f"${df['price'].max():,.2f}")
col3.metric("Harga Terendah (24h)", f"${df['price'].min():,.2f}")

# Grafik Utama
fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], line=dict(color='#00ffcc'))])
fig.update_layout(template="plotly_dark", height=300)
st.plotly_chart(fig, use_container_width=True)

# Monitoring Kerja AI (Real-time Simulation)
if st.button("Jalankan Analisis Komprehensif"):
    with st.status("Memulai simulasi analisis...", expanded=True) as status:
        st.write("Mengecek data pasar global...")
        tavily = TavilyClient(api_key=tavily_key)
        
        st.write("Mencari sentimen berita terkini...")
        news = tavily.search(query=f"market sentiment {coin} May 2026")
        
        st.write("Mengirim data ke Claude (Opus)...")
        headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": f"Aset: {coin}. Harga: {current_price}. Berita: {news}. Analisis mendalam?"}]
        }
        response = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
        
        status.update(label="Analisis Selesai!", state="complete")
        
    st.markdown("### 🧠 Hasil Analisis AI")
    st.write(response['content'][0]['text'])
