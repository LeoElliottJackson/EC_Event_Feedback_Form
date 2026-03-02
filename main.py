# Imports
import streamlit as st
from helpers import complete_login, login
from helpers import hide_sidebar 
# Functions
def remove_st_branding():
    st.markdown(
        """
        <script>
        window.addEventListener('load', () => {
            window.top.document.querySelectorAll(`[href*="streamlit.io"]`)
                .forEach(e => e.style.display = 'none');
        });
        </script>
        """,
        unsafe_allow_html=True
    )
remove_st_branding()
# Main
complete_login()

st.set_page_config(page_title="Login")

hide_sidebar()

if "user" not in st.session_state:
    st.header("Sign in to continue")
    login()
    st.stop()

st.success(f"Logged in as: {st.session_state['user']['name']}")
st.switch_page("pages/landing.py")