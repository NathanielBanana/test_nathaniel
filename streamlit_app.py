import streamlit as st
from datetime import date

if "db" not in st.session_state:
    st.session_state["db"] = {
        "users" : {
            "student_123" : {
                "onboarding_complete: False"
                "name" : "bobby",
                "age" : 1000,
                "email" : "bobby@school.edu",
                "total points" : 0,
                "days" : {
                    str(date.today()) : {
                        "fixed_blocks": [],
                        "floating_tasks": [],
                        "ai_schedule": None
                    }
                }
            }
        }
    }

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"

if not st.session_state["logged_in"]:    
    if st.session_state["auth_mode"] == "login":
        st.title("Log In")
        st.write("Log in to continue")
        with st.form("log_in_form"):
            log_in_email =  st.text_input("Enter your email:")
            log_in_password = st.text_input("Enter your account password:")

            if st.form_submit_button("Log In"):
                # Validate email / password
                st.session_state["logged_in"] = True
                st.rerun()




        if st.button("Don't have an account? Sign Up"):
            st.session_state["auth_mode"] = "signup"
            st.rerun()
    else:
        st.title("Sign Up")
        with st.form("Sign Up"):
            sign_up_email = st.text_input("Enter your email:")
            sign_up_password = st.text_input("Make a password:")
            sign_up_password_confirm = st.text_input("Confirm your password:")

            if st.form_submit_button("Creat an Account"):
                # Validate email / password
                st.success("Account created! Please log in")
                st.session_state["auth_mode"] = "login"
                st.rerun()
        if st.button("Already have an account? Log In"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
else:
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
            st.session_state["auth_mode"] = "homepage"
            st.rerun()
            st.title("Home Page")
            if st.button("Log Out"):
                st.session_state["logged_in"] = False
                st.rerun()
            if st.button("Settings"):
                st.session_state["auth_mode"] = "settings"
                st.rerun()
                st.title("settings")
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.rerun()

