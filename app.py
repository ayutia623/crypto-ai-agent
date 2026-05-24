import streamlit as st
from pycoingecko import CoinGeckoAPI
import anthropic
from tavily import TavilyClient

st.set_page_config(page_title="Crypto AI Agent Pro", layout="wide")
st.title("🚀 Crypto AI Agent - Intelligence Mode")

with st.sidebar:
    st.header("🔑 Kunci Akses")
    claude_key = st.text_input("Claude API Key", type="password")
    gecko_key = st.text_input("CoinGecko API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")

if claude_key and gecko_key and tavily_key:
    cg = CoinGeckoAPI(api_key=gecko_key)
    client = anthropic.Anthropic(
        api_key=claude_key,
        base_url="https://api.tokies.lol/anthropic",
        default_headers={"x-api-key": claude_key}
    )
    tavily = TavilyClient(api_key=tavily_key)
    
    coins = ['bitcoin', 'ethereum', 'solana']
    
    if st.button("Analisis Komprehensif (Data + Berita)"):
        with st.spinner("Sedang meriset pasar..."):
            # 1. Tarik Data Harga
            data = cg.get_price(ids=','.join(coins), vs_currencies='usd')
            market_summary = "\n".join([f"{c.capitalize()}: ${data[c]['usd']:,}" for c in coins])
            
            # 2. Cari Berita Terkini via Tavily
            news = tavily.search(query="crypto market trends news analysis May 2026", search_depth="advanced")
            news_summary = "\n".join([f"- {r['title']}: {r['content']}" for r in news['results'][:3]])
            
            # 3. Analisis oleh Claude
            prompt = f"Data Harga:\n{market_summary}\n\nBerita Terkini:\n{news_summary}\n\nBerikan analisis mendalam dan strategi trading untuk hari ini."
            
            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(message.content[0].text)
else:
    st.info("Masukkan ketiga API Key di sidebar untuk mengaktifkan agen cerdas.")
