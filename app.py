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
    # Membagi layout menjadi 2 kolom
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📈 Data Pasar")
        # Mengambil data harga dari CoinGecko
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum,solana&x_cg_demo_api_key={gecko_key}"
        try:
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data).T
            st.table(df)
        except Exception as e:
            st.error(f"Gagal tarik data harga: {e}")

    with col2:
        st.subheader("🧠 Analisis AI")
        if st.button("Jalankan Analisis Mendalam"):
            with st.spinner("Sedang meriset pasar..."):
                try:
                    # 1. Pencarian Berita via Tavily
                    tavily = TavilyClient(api_key=tavily_key)
                    news = tavily.search(query="crypto market analysis May 2026")
                    
                    # 2. Inisialisasi Claude
                    client = anthropic.Anthropic(
                        api_key=claude_key, 
                        base_url="https://api.tokies.lol/anthropic"
                    )
                    
                    # 3. Analisis oleh Claude
                    # Menggunakan model dari setting.json kamu
                    prompt = f"Data Harga: {data}. Berita: {news}. Berikan analisis teknikal & fundamental mendalam untuk portofolio crypto."
                    msg = client.messages.create(
                        model="claude-opus-4-7", 
                        max_tokens=1000, 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.write(msg.content[0].text)
                except Exception as e:
                    st.error(f"Error AI: {e}")
else:
    st.info("Terminal belum aktif. Silakan masukkan semua kunci API di sidebar.")
