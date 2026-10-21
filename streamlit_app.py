from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Ganti nama file ini kalau nanti kamu mengunggah versi HTML yang baru.
HTML_FILE = "UV-1700_Virtual_Lab_v29_animasi_kuvet.html"

st.set_page_config(
    page_title="UV-1700 Virtual Laboratory",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Rapatkan margin Streamlit supaya area lab selebar mungkin.
st.markdown(
    """
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      .block-container {padding: 0.5rem 0.5rem 0 0.5rem; max-width: 100%;}
    </style>
    """,
    unsafe_allow_html=True,
)

html_path = Path(__file__).parent / HTML_FILE

if not html_path.exists():
    st.error(f"File {HTML_FILE} tidak ditemukan. Pastikan berada satu folder dengan app.py.")
    st.stop()


@st.cache_data(show_spinner=False)
def load_html(path: str, mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


html = load_html(str(html_path), html_path.stat().st_mtime)

# Tinggi tampilan (px). Tambah kalau panel kanan terpotong di layarmu.
components.html(html, height=920, scrolling=True)
