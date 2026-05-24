import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient
import ccxt

st.set_page_config(page_title="Pro Crypto Command Center", layout="wide")
st.title("🚀 Paper Trading & Command Center v5.0")

# Ambil Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

# Fungsi Data
@st.cache_data(ttl=60)
def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

coin = st.sidebar.selectbox("Pilih Aset:", ['bitcoin', 'ethereum', 'solana'])
df = get_data(coin)
current_price = df['price'].iloc[-1]

# Panel Simulasi
st.sidebar.subheader("💰 Simulasi Paper Trading")
if "balance" not in st.session_state: st.session_state.balance = 10000.0 # Modal awal $10.000
st.sidebar.write(f"Modal Virtual: ${st.session_state.balance:,.2f}")

if st.sidebar.button("Simulasi Beli (Buy)"):
    st.session_state.entry_price = current_price
    st.sidebar.success(f"Beli di ${current_price:,.2f}")

# Analisis AI
if st.button("Jalankan Analisis & Strategi Trading"):
    with st.status("AI sedang menghitung strategi...", expanded=True):
        tavily = TavilyClient(api_key=tavily_key)
        news = tavily.search(query=f"market analysis {coin} May 2026")
        
        headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": f"Aset: {coin}. Harga: {current_price}. Berita: {news}. Berikan rekomendasi Buy/Hold/Sell dan alasan teknikal."}]
        }
        res = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
        st.write(res['content'][0]['text'])

# Visualisasi
fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], line=dict(color='#00ffcc'))])
fig.update_layout(template="plotly_dark", height=300)
st.plotly_chart(fig, use_container_width=True)
