import streamlit as st

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