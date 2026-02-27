import streamlit as st
from pathlib import Path
from streamlit_js_eval import get_geolocation
from db import insert_feedback, DeviceID
from datetime import datetime
from db import insert_feedback
from helpers import hide_sidebar, dxc_logo

if not st.user.is_logged_in:
    st.switch_page("main.py")
else:
    hide_sidebar()
    event_type = st.session_state.get("event_type")


    # -------------- PAGE SCALING ----------------

    SCALE = 1.25

    st.markdown(
        f"""
        <style>
        html {{
            zoom: {SCALE};
        }}

        /* Button scaling */
        div.stButton > button {{
            height: {100 * SCALE}px !important;
            width: {100 * SCALE}px !important;
            font-size: {2.5 * SCALE}rem !important;
            border-radius: {20 * SCALE}px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    #-------------------- SUPABASE REPSONSE ---------------

    # def insert_feedback(feedback_data):
    #     response = supabase.table("feedback_event").insert(feedback_data).execute()

    #     if response.error:
    #         raise Exception(response.error.message)

    #     return response.data

    # ---------------- GET LOCATION ----------------
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

    # --------------- BUTTONS ---------------

    st.markdown(
        f"""
        <h1 style="
            text-align: center;
            transform: translateX({0.6 * SCALE}rem);
        ">
            How was your experience?
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Emoji layout
    col_left, col1, col2, col3, col4, col5, col_right = st.columns([1,1,1,1,1,1,1])

    emojis = ["😡", "🙁", "😐", "🙂", "😁"] 
    values = [1, 2, 3, 4, 5]

    for col, emoji, val in zip([col1, col2, col3, col4, col5], emojis, values):

        if col.button(emoji, key=f"btn_{val}", help="Tap to give feedback", type="primary", width=75):
            st.session_state["clicked_value"] = val

            utc_time = datetime.now()

            if "lat" in st.session_state and "lon" in st.session_state:

                # debug statements
                print(st.session_state["lat"])
                print(st.session_state["lon"])
                print(st.session_state["accuracy"])

            if "clicked_value" in st.session_state:
                val = st.session_state["clicked_value"]

                feedback_data = {
                    "device_id": DeviceID.data[0]["device_id"],
                    "feedback_value": val,
                    "timestamp_utc": datetime.fromtimestamp(st.session_state.get("location", {}).get("timestamp", 0) / 1000).isoformat(),
                    "timezone_offset_minutes": 0,
                    "latitude": st.session_state.get("lat"),
                    "longitude": st.session_state.get("lon"),
                    "location_accuracy": st.session_state.get("accuracy"),
                    "event": event_type
                }

                print("Feedback data to insert:", feedback_data)

                try:
                    insert_feedback(feedback_data)
                    #st.toast(f"Thank you! Your feedback rating was: {val}")
                    st.markdown(
                            f"""
                            <div style="
                                position: fixed;
                                bottom: 2rem;
                                left: 50%;
                                transform: translateX(-50%);
                                background: #4CAF50;
                                color: white;
                                padding: 0.75rem 1.25rem;
                                border-radius: 8px;
                                font-weight: 600;
                                z-index: 9999;
                                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                            ">
                                Thank you! Your feedback rating was: {val}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"Error saving feedback: {e}")

                del st.session_state["clicked_value"]

        
    # ---------- UI ----------
    # DXC LOGO
    #st.image(dxc_logo)
    col_left, col_centre, col_right = st.columns([1, 2, 1])  # center column is wider
    with col_centre:
        st.image(dxc_logo)