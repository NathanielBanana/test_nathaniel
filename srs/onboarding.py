import streamlit as st
from firebase_utils import db, auth

def onboarding(): 
    with st.form("onboarding"):
        name = st.text_input("What is your name?")
        age = st.text_input("How old are you?")
        favorite_color = st.select_slider(
            "Choose your favorite color",
            options=[
                "Red",
                "Orange",
                "Yellow",
                "Green",
                "Blue",
                "Indigo",
                "Violet",
            ],
        ) 
        reason_for_use = st.radio(
            "What are you using this website for?",
            ["Personal Reasons", "School/Education", "Professional/Team Work"],
        )

        onboarding_submit = st.form_submit_button("Finish")

        if onboarding_submit:
            uid = st.session_state['user_session']['uid']
            db.collection('users').document(uid).update({
                "name": name,
                "age": age,
                "favorite_color": favorite_color,
                "reason_for_use": reason_for_use,
                "completed_onboarding": True
            })

            if "user" in st.session_state:
                st.session_state["user"]["completed_onboarding"] = True
            st.session_state["current_view"] = "main"
            st.rerun()