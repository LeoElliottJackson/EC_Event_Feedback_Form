from pathlib import Path
from PIL import Image
import streamlit as st
import msal
import uuid

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

smiley = ASSETS_DIR / "smiley.png"
dxc_logo = ASSETS_DIR / "DXC_Logo.png"
# -------------------------------------------------------------------
# MSAL HELPERS
# -------------------------------------------------------------------
def get_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=st.secrets["auth"]["client_id"],
        client_credential=st.secrets["auth"]["client_secret"],
        authority=st.secrets["auth"]["authority"]
    )

def login():
    if "user" in st.session_state:
        return

    msal_app = get_msal_app()

    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"]
    )

    st.markdown(f"[Click here to sign in]({auth_url})")

def complete_login():
    params = st.query_params

    if "code" not in params:
        return

    msal_app = get_msal_app()

    result = msal_app.acquire_token_by_authorization_code(
        params["code"],
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"]
    )

    if "id_token_claims" in result:
        st.session_state["user"] = result["id_token_claims"]
        st.query_params.clear()
        st.rerun()
    else:
        st.error(result)
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