import streamlit as st
import requests
import pandas as pd
import anthropic
from tavily import TavilyClient

st.set_page_config(page_title="Pro Crypto Terminal", layout="wide")

# Styling agar terlihat seperti terminal profesional
st.markdown("""<style>.main {background-color: #0e1117;}</style>""", unsafe_allow_html=True)

st.title("📊 Pro Crypto Terminal")

# Sidebar
with st.sidebar:
    st.header("🔑 Kredensial")
    claude_key = st.text_input("Claude Key", type="password")
    gecko_key = st.text_input("Gecko Key", type="password")
    tavily_key = st.text_input("Tavily Key", type="password")

if claude_key and gecko_key and tavily_key:
    # 1. Layout Kolom untuk Tampilan Kompleks
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📈 Data Pasar")
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum,solana&x_cg_demo_api_key={gecko_key}"
        data = requests.get(url).json()
        df = pd.DataFrame(data).T # Mengubah data menjadi tabel rapi
        st.table(df)

    with col2:
        st.subheader("🧠 Analisis AI")
        if st.button("Jalankan Analisis Mendalam"):
            with st.spinner("Mereset pasar & menganalisis data..."):
                # Pencarian Tavily
                tavily = TavilyClient(api_key=tavily_key)
                news = tavily.search(query="crypto market analysis May 2026")
                
                # Analisis Claude
                client = anthropic.Anthropic(api_key=claude_key, base_url="https://api.tokies.lol/anthropic", default_headers={"x-api-key": claude_key})
                prompt = f"Data Harga: {data}. Berita: {news}. Analisis teknikal & fundamental mendalam."
                msg = client.messages.create(model="claude-opus-4-7", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
                st.write(msg.content[0].text)
else:
    st.info("Terminal belum aktif. Silakan masukkan kunci API.")
