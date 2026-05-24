import streamlit as st
import requests
import pandas as pd
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")
st.title("📊 Pro Crypto Terminal")

# Ambil dari Secrets
auth_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

if auth_token and gecko_key and tavily_key:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📈 Data Pasar")
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum,solana&x_cg_demo_api_key={gecko_key}"
        data = requests.get(url).json()
        st.table(pd.DataFrame(data).T)

    with col2:
        st.subheader("🧠 Analisis AI")
        if st.button("Jalankan Analisis Mendalam"):
            with st.spinner("Menghubungkan ke AI..."):
                try:
                    # 1. Tavily
                    tavily = TavilyClient(api_key=tavily_key)
                    news = tavily.search(query="crypto market analysis May 2026")
                    
                    # 2. Kirim ke Claude (Bypass library, pakai request manual agar tidak diblokir)
                    headers = {"x-api-key": auth_token, "Content-Type": "application/json"}
                    payload = {
                        "model": model_name,
                        "max_tokens": 1000,
                        "messages": [{"role": "user", "content": f"Data: {data}. Berita: {news}. Analisis?"}]
                    }
                    response = requests.post(f"{base_url}/v1/messages", json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        st.write(res_json['content'][0]['text'])
                    else:
                        st.error(f"Status {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.error("Secrets tidak terbaca!")
