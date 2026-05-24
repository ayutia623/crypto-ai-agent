import streamlit as st
import requests
import pandas as pd
import anthropic
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")
st.title("📊 Pro Crypto Terminal")

# Mengambil rahasia dengan nama variabel yang tepat
claude_token = st.secrets.get("ANTHROPIC_AUTH_TOKEN")
gecko_key = st.secrets.get("GECKO_API_KEY")
tavily_key = st.secrets.get("TAVILY_API_KEY")
base_url = st.secrets.get("ANTHROPIC_BASE_URL")
model_name = st.secrets.get("ANTHROPIC_MODEL")

if claude_token and gecko_key and tavily_key:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📈 Data Pasar")
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum,solana&x_cg_demo_api_key={gecko_key}"
        response = requests.get(url)
        data = response.json()
        st.table(pd.DataFrame(data).T)

    with col2:
        st.subheader("🧠 Analisis AI")
        if st.button("Jalankan Analisis Mendalam"):
            with st.spinner("Sedang memproses..."):
                try:
                    tavily = TavilyClient(api_key=tavily_key)
                    news = tavily.search(query="crypto market analysis May 2026")
                    
                    # Inisialisasi client dengan AUTH_TOKEN yang benar
                    client = anthropic.Anthropic(api_key=claude_token, base_url=base_url)
                    
                    msg = client.messages.create(
                        model=model_name, 
                        max_tokens=1000, 
                        messages=[{"role": "user", "content": f"Data: {data}. Berita: {news}. Analisis?"}]
                    )
                    st.write(msg.content[0].text)
                except Exception as e:
                    st.error(f"Error AI: {e}")
else:
    st.error("Secrets belum terkonfigurasi dengan nama yang benar di Streamlit!")
