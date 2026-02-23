import streamlit as st
from pathlib import Path
from streamlit_js_eval import get_geolocation
from db import insert_feedback, DeviceID
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

smiley = ASSETS_DIR / "smiley.png"

# ---------- APP STATE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"   # default

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

location = get_geolocation()

if location and "location" not in st.session_state:
    coords = location.get("coords", {})

    st.session_state["location"] = location
    st.session_state["accuracy"] = coords.get("accuracy")
    st.session_state["lat"] = coords.get("latitude")
    st.session_state["lon"] = coords.get("longitude")

    timestamp = location.get("timestamp", {})
    st.session_state["timestamp"] = timestamp


    st.rerun()


# ---------- THEME CSS ----------
LIGHT_MODE = """
<style>
:root {
    --bg: #F2F2F2;
    --text: #000000;
    --card: #FFFFFF;
    --accent: #5E2CED;
}
body {
    background-color: var(--bg);
    color: var(--text);
}
h1 {
    text-align: center;
    color: var(--text);
    font-weight: 800;
    margin-bottom: 1.3rem;
}
.feedback-btn {
    height: 220px !important;
    width: 220px !important;
    border-radius: 110px !important;
    font-size: 120px !important;
    padding: 0 !important;
    border: none !important;
    background-color: var(--card) !important;
    color: var(--text) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.18) !important;
    transition: 0.15s ease-in-out;
}
.feedback-btn:hover {
    transform: scale(1.06);
    background-color: var(--accent) !important;
    color: white !important;
}
</style>
"""

DARK_MODE = """
<style>
:root {
    --bg: #0D0D0D;
    --text: #FFFFFF;
    --card: #1A1A1A;
    --accent: #A58BFF;
}
body {
    background-color: var(--bg);
    color: var(--text);
}
h1 {
    text-align: center;
    color: var(--text);
    font-weight: 800;
    margin-bottom: 1.3rem;
}
.feedback-btn {
    height: 220px !important;
    width: 220px !important;
    border-radius: 110px !important;
    font-size: 120px !important;
    padding: 0 !important;
    border: none !important;
    background-color: var(--card) !important;
    color: var(--text) !important;
    box-shadow: 0 6px 16px rgba(255,255,255,0.12) !important;
    transition: 0.15s ease-in-out;
}
.feedback-btn:hover {
    transform: scale(1.06);
    background-color: var(--accent) !important;
    color: black !important;
}
</style>
"""

# Apply theme
if st.session_state.theme == "light":
    st.markdown(LIGHT_MODE, unsafe_allow_html=True)
else:
    st.markdown(DARK_MODE, unsafe_allow_html=True)


# ---------- UI ----------
# DXC LOGO
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/DXC_Technology_logo.svg/400px-DXC_Technology_logo.svg.png",
    width=180
)

# Theme toggle
theme_label = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
st.button(theme_label, on_click=toggle_theme)

st.title("How was your experience?")

# Emoji layout
col1, col2, col3, col4, col5 = st.columns(5)

emojis = ["😡", "🙁", "😐", "🙂", "😁"]  # larger-face friendly variations
values = [1, 2, 3, 4, 5]

for col, emoji, val in zip([col1, col2, col3, col4, col5], emojis, values):

    if col.button(emoji, key=f"btn_{val}", help="Tap to give feedback", type="primary"):

        utc_time = datetime.now()

        if "lat" in st.session_state and "lon" in st.session_state:
            #st.success(f"Latitude: {st.session_state['lat']}, Longitude: {st.session_state['lon']}")
            print(st.session_state["lat"])
            print(st.session_state["lon"])
            print(st.session_state["accuracy"])
        feedback_data = {
            "device_id": DeviceID.data[0]["device_id"],
            "feedback_value": val,
            "timestamp_utc": datetime.fromtimestamp(st.session_state.get("location", {}).get("timestamp", 0) / 1000).isoformat(),
            "timezone_offset_minutes": 0,
            "latitude": st.session_state.get("lat"),
            "longitude": st.session_state.get("lon"),
            "location_accuracy": st.session_state.get("accuracy"),
        }
        print("Feedback data to insert:", feedback_data)
        try:
            insert_feedback(feedback_data)
            print(utc_time)
            st.success(f"Thank you! Your feedback rating was: {val}")
        except Exception as e:
            st.error(f"Error saving feedback: {e}")