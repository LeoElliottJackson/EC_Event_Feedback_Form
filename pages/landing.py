import streamlit as st
from helpers import hide_sidebar

if "user" not in st.session_state:
    st.switch_page("main.py")
else:
    hide_sidebar()

    st.header("Please select the event type")
    option = st.selectbox("Event type:", ("Onboarding", "STEM Event", "Assessment Centre", "Other"), placeholder="Select an event type")

    if option:
        st.session_state["event_type"] = option
        if st.button("Save and submit", key="next_btn", type="primary", width=750):
            st.switch_page("pages/buttonPage.py")