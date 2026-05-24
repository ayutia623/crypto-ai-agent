import streamlit as st
from pycoingecko import CoinGeckoAPI
import anthropic

st.set_page_config(page_title="Crypto AI Agent", layout="wide")

st.title("🚀 Crypto AI Agent - Live Analysis")

with st.sidebar:
    # Kita tetap minta user input, tapi nanti bisa kita pindahkan ke Secrets
    api_key = st.text_input("Tokies/Claude API Key", type="password")
    
if api_key:
    # Konfigurasi Client Anthropic dengan URL kustom
    client = anthropic.Anthropic(
        api_key=api_key,
        base_url="https://api.tokies.lol/anthropic" # URL kustom kamu
    )
    
    # Inisialisasi CoinGecko (tambahkan pengecekan jika kamu butuh kunci geckonya)
    cg = CoinGeckoAPI() # Pakai mode publik jika tidak ada kunci
    
    price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')
    btc_price = price_data['bitcoin']['usd']

    st.success(f"Harga Bitcoin saat ini: ${btc_price:,.2f}")

    if st.button("Analisis Pasar"):
        with st.spinner("Claude sedang menganalisis..."):
            prompt = f"Harga Bitcoin saat ini adalah ${btc_price}. Berikan analisis teknikal singkat."
            
            # Sesuaikan dengan model yang ada di setting.json kamu
            message = client.messages.create(
                model="claude-opus-4-7", 
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(message.content[0].text)
else:
    st.info("Silakan masukkan API Key Anda di sidebar.")
