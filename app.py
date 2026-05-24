import streamlit as st
from pycoingecko import CoinGeckoAPI
import anthropic

st.set_page_config(page_title="Crypto AI Agent", layout="wide")

st.title("🚀 Crypto AI Agent - Live Analysis")

# Sidebar untuk API Key
with st.sidebar:
    claude_key = st.text_input("Claude API Key", type="password")
    gecko_key = st.text_input("CoinGecko API Key", type="password")

if claude_key and gecko_key:
    cg = CoinGeckoAPI(api_key=gecko_key)
    client = anthropic.Anthropic(api_key=claude_key)

    # Menarik harga Bitcoin
    price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')
    btc_price = price_data['bitcoin']['usd']

    st.success(f"Harga Bitcoin saat ini: ${btc_price:,.2f}")

    if st.button("Analisis Pasar"):
        with st.spinner("Claude sedang menganalisis..."):
            prompt = f"Harga Bitcoin saat ini adalah ${btc_price}. Berikan analisis singkat apakah ini saat yang baik untuk menahan aset."
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(message.content[0].text)
else:
    st.info("Silakan masukkan API Key di sidebar untuk memulai.")
