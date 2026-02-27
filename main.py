# Imports
import streamlit as st
from helpers import hide_sidebar
# Main
hide_sidebar()

if not st.user.is_logged_in:
    st.header("This app is private.")
    st.subheader("Please log in.")
    if st.button("Log in with Microsoft"):
        st.login()
else:
    st.switch_page("pages/landing.py")