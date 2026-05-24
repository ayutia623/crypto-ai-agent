import streamlit as st
import requests
import pandas as pd
import anthropic
from tavily import TavilyClient

# Konfigurasi Halaman
st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")
st.title("📊 Pro Crypto Terminal")

# Sidebar untuk Input API Key
with st.sidebar:
    st.header("🔑 Kredensial API")
    claude_key = st.text_input("Claude API Key", type="password")
    gecko_key = st.text_input("Gecko API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")

if claude_key and gecko_key and tavily_key:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📈 Data Pasar")
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum,solana&x_cg_demo_api_key={gecko_key}"
        try:
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data).T
            st.table(df)
        except Exception as e:
            st.error(f"Gagal tarik data: {e}")

    with col2:
        st.subheader("🧠 Analisis AI")
        if st.button("Jalankan Analisis Mendalam"):
            with st.spinner("Sedang memproses..."):
                try:
                    # 1. Riset Tavily
                    tavily = TavilyClient(api_key=tavily_key)
                    news = tavily.search(query="crypto market analysis May 2026")
                    
                    # 2. Inisialisasi Claude
                    # Menggunakan base_url sesuai proxy kamu
                    client = anthropic.Anthropic(
                        api_key=claude_key, 
                        base_url="https://api.tokies.lol/anthropic"
                    )
                    
                    # 3. Analisis dengan model yang ada di setting.json
                    prompt = f"Data Harga: {data}. Berita: {news}. Analisis mendalam untuk portofolio crypto."
                    msg = client.messages.create(
                        model="opus", # Kita coba pakai 'opus' sesuai setting.json kamu
                        max_tokens=1000, 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.write(msg.content[0].text)
                except Exception as e:
                    st.error(f"Error pada AI: {e}")
                    st.info("Coba ganti model ke 'sonnet' atau 'opus' di kode jika error ini muncul.")
else:
    st.info("Terminal belum aktif. Silakan masukkan semua kunci API di sidebar.")
