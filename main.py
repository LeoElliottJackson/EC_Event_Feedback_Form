# Imports
import streamlit as st
import msal
import uuid
from helpers import hide_sidebar  # can only be called AFTER callback handled!!

# -------------------------
# MSAL HELPERS
# -------------------------
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
# ---------------------------------------------------------
# MAIN APP — ORDER MATTERS!
# ---------------------------------------------------------

# 1️⃣ CALLBACK MUST RUN FIRST — BEFORE ANY UI!
complete_login()

# 2️⃣ NOW set page config (AFTER callback)
st.set_page_config(page_title="Login")

# 3️⃣ NOW hide sidebar safely
hide_sidebar()

# 4️⃣ If not logged in, show login only
if "user" not in st.session_state:
    st.header("Sign in to continue")
    login()
    st.stop()

# 5️⃣ Logged in → redirect
st.success(f"Logged in as: {st.session_state['user']['name']}")
st.switch_page("pages/landing.py")