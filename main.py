# Imports
import streamlit as st
from helpers import hide_sidebar
import streamlit as st
import msal
import uuid
# Login
def get_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=st.secrets["auth"]["client_id"],
        client_credential=st.secrets["auth"]["client_secret"],
        authority=st.secrets["auth"]["authority"]
    )

def login():
    if "user" in st.session_state:
        return st.session_state["user"]

    msal_app = get_msal_app()
    state = str(uuid.uuid4())

    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"],
        state=state,
        response_mode="query"
    )

    st.session_state["auth_state"] = state
    st.markdown(f"[Click here to sign in]({auth_url})")

def complete_login():
    # Read URL query parameters
    params = st.query_params

    # If no "code" param, user isn't returning from Azure yet
    if "code" not in params:
        return

    # Validate state parameter
    if params.get("state", "") != st.session_state.get("auth_state"):
        st.error("Invalid auth state")
        return

    msal_app = get_msal_app()

    # Redeem authorization code for tokens
    result = msal_app.acquire_token_by_authorization_code(
        params["code"],
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"]
    )

    if "id_token_claims" in result:
        st.session_state["user"] = result["id_token_claims"]

        # 🔥 Clear query params to remove ?code=... from the URL
        st.query_params = {}

        st.experimental_rerun()
    else:
        st.error("Login failed")

# Main
hide_sidebar()

st.set_page_config(page_title="Login")

# 1️⃣ Handle callback FIRST before any other logic
complete_login()

# 2️⃣ If user is not logged in, show login button ONLY
if "user" not in st.session_state:
    st.header("Sign in to continue")
    login()
    st.stop()

# 3️⃣ If logged in, proceed to app
st.success(f"Logged in as: {st.session_state['user']['name']}")
st.switch_page("pages/landing.py")