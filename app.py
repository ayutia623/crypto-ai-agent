import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient

# Konfigurasi Halaman
st.set_page_config(page_title="Pro Crypto Master Command Center", layout="wide")
st.title("🚀 Crypto Master Command Center")

# Ambil data dari Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

# Fungsi Data dengan Cache
@st.cache_data(ttl=60)
def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Logika System Prompt untuk Claude
system_logic = """
Kamu adalah Crypto Analyst AI kelas dunia. 
Tugasmu:
1. Lakukan analisis mendalam terhadap data pasar.
2. Pertimbangkan sisi fundamental dan teknikal secara objektif.
3. Berpikir logis, terstruktur, dan transparan dalam memberikan rekomendasi.
4. Jika menganalisis pergerakan harga, berikan simulasi prediksi dalam format tabel.
"""

# Tab Utama
tab1, tab2 = st.tabs(["📊 Dashboard & Prediksi", "💬 AI Crypto Chat"])

with tab1:
    coin = st.selectbox("Pilih Aset:", ['bitcoin', 'ethereum', 'solana'])
    df = get_data(coin)
    current_price = df['price'].iloc[-1]
    
    # Metrik
    col1, col2, col3 = st.columns(3)
    col1.metric("Harga Saat Ini", f"${current_price:,.2f}")
    col2.metric("Perubahan 24h", f"{((current_price - df['price'].iloc[0]) / df['price'].iloc[0]) * 100:.2f}%")
    col3.metric("Volatilitas", f"{df['price'].pct_change().std() * 100:.4f}%")

    # Grafik
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], line=dict(color='#00ffcc'))])
    fig.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Jalankan Analisis & Prediksi"):
        with st.status("AI sedang menganalisis pasar...", expanded=True):
            tavily = TavilyClient(api_key=tavily_key)
            news = tavily.search(query=f"technical and sentiment analysis for {coin} May 2026")
            
            headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
            payload = {
                "model": model_name,
                "system": system_logic,
                "messages": [{"role": "user", "content": f"Aset: {coin}. Harga: {current_price}. Berita: {news}. Berikan analisis dan tabel prediksi 3 jam ke depan."}]
            }
            res = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
            st.write(res['content'][0]['text'])

with tab2:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
    if prompt := st.chat_input("Tanya AI tentang strategi trading..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            payload = {"model": model_name, "system": system_logic, "messages": st.session_state.messages}
            res = requests.post(f"{base_url}/v1/messages", json={"x-api-key": auth_token, **payload}, headers={"x-api-key": auth_token, "Content-Type": "application/json"}).json()
            answer = res['content'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar Paper Trading
st.sidebar.subheader("💰 Paper Trading")
if st.sidebar.button("Simulasi Beli"):
    st.sidebar.success(f"Posisi dibuka di ${current_price:,.2f}")
