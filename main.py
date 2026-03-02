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
    # If already logged in
    if "user" in st.session_state:
        return st.session_state["user"]

    # Build auth URL
    msal_app = get_msal_app()
    state = str(uuid.uuid4())
    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"],
        state=state,
        response_mode="query"
    )

    st.session_state["auth_state"] = state
    st.markdown(f"[Click here to sign in with Microsoft]({auth_url})")

def complete_login():
    # Parse URL params
    params = st.experimental_get_query_params()
    if "code" not in params:
        return

    if params.get("state", [""])[0] != st.session_state.get("auth_state"):
        st.error("Invalid auth state")
        return

    msal_app = get_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        params["code"][0],
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"]
    )

    if "id_token_claims" in result:
        st.session_state["user"] = result["id_token_claims"]
        st.experimental_set_query_params()  # Clear query params
        st.experimental_rerun()
    else:
        st.error("Login failed")
# Main
hide_sidebar()
complete_login()

if "user" not in st.session_state:
    st.header("Sign in to continue")
    login()
    st.stop()
else:
    st.switch_page("pages/landing.py")