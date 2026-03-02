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
        return st.session_state["user"]

    msal_app = get_msal_app()
    state = str(uuid.uuid4())

    # Save state in query params so it survives redirect
    st.query_params["expected_state"] = state

    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"],
        state=state,
        response_mode="query"
    )

    st.markdown(f"[Click here to sign in]({auth_url})")


def complete_login():
    params = st.query_params

    if "code" not in params:
        return

    expected_state = params.get("expected_state")
    returned_state = params.get("state")

    if not expected_state or returned_state != expected_state:
        st.error("Invalid auth state")
        st.stop()

    msal_app = get_msal_app()

    result = msal_app.acquire_token_by_authorization_code(
        params["code"],
        scopes=["User.Read"],
        redirect_uri=st.secrets["auth"]["redirect_uri"]
    )

    if "id_token_claims" in result:
        st.session_state["user"] = result["id_token_claims"]

        # Clear query params
        st.query_params.clear()

        st.rerun()
    else:
        st.error("Login failed")

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