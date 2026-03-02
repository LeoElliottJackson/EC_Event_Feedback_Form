from pathlib import Path
from PIL import Image
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

smiley = ASSETS_DIR / "smiley.png"
dxc_logo = ASSETS_DIR / "DXC_Logo.png"


# -------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------
def init_page(page_title: str, layout: str = "wide", logo_link: str = "https://dxc.com/uk/en"):
    st.set_page_config(
        page_title=page_title,
        page_icon=Image.open(dxc_logo),
        layout=layout
    )

# -------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------
def hide_sidebar():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)