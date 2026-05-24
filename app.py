import streamlit as st

# Pengaturan Tampilan Layar Luas
st.set_page_config(page_title="Crypto AI Agent", layout="wide")

st.title("🚀 Crypto AI Agent - Personal Dashboard")
st.markdown("---")

# Sidebar untuk API Key (Agar rapi)
with st.sidebar:
    st.header("🔑 Pengaturan API")
    claude_key = st.text_input("Claude API Key", type="password")
    gecko_key = st.text_input("CoinGecko API Key", type="password")
    st.markdown("---")
    st.info("Status: Siap untuk konfigurasi")

# Kolom Utama
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Analisis Data")
    st.write("Belum ada data. Silakan masukkan API Key untuk memulai.")

with col2:
    st.subheader("🤖 Pesan Agen")
    st.write("Agen sedang menunggu perintah...")
