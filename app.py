import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Master Command Center", layout="wide")
st.title("🚀 Crypto Master Command Center")

# Konfigurasi API
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

@st.cache_data(ttl=60)
def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1&x_cg_demo_api_key={gecko_key}"
    data = requests.get(url).json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# TAB 1: Dashboard & Analisis
tab1, tab2 = st.tabs(["📊 Dashboard & Prediksi", "💬 AI Crypto Chat"])

with tab1:
    coin = st.selectbox("Pilih Aset:", ['bitcoin', 'ethereum', 'solana'])
    df = get_data(coin)
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['price'], line=dict(color='#00ffcc'))])
    fig.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Jalankan Analisis Komprehensif"):
        with st.status("AI sedang bekerja...", expanded=True):
            tavily = TavilyClient(api_key=tavily_key)
            news = tavily.search(query=f"market analysis {coin} May 2026")
            headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
            payload = {"model": model_name, "messages": [{"role": "user", "content": f"Aset: {coin}. Berita: {news}. Analisis & prediksi 3 jam?"}]}
            res = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers).json()
            st.write(res['content'][0]['text'])

# TAB 2: Chat Assistant
with tab2:
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
    if prompt := st.chat_input("Tanya AI tentang strategi trading..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            payload = {"model": model_name, "messages": st.session_state.messages}
            res = requests.post(f"{base_url}/v1/messages", json={"x-api-key": auth_token, **payload}, headers={"x-api-key": auth_token, "Content-Type": "application/json"}).json()
            answer = res['content'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
