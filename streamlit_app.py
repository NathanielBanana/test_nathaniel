import streamlit as st
from datetime import date
from pages.onboarding import onboarding
from pages.homepage import homepage
from pages.activityform import activity_form
from pages.calender_gen import calender_gen

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

if "user_info" not in st.session_state:
    st.session_state["user_info"] = None


if not st.session_state["logged_in"]:    
    if st.session_state["auth_mode"] == "login":
        st.title("Log In")
        st.write("Log in to continue")
        with st.form("log_in_form"):
            log_in_email =  st.text_input("Enter your email:")
            log_in_password = st.text_input("Enter your account password:")

            if st.form_submit_button("Log In"):
                try:
                    st.session_state["logged_in"] = True
                    st.rerun()
                except Exception as e:
                    st.error("Invalid Email or password. Please try again.")
                # Validate email / password
        if st.button("Don't have an account? Sign Up"):
            st.session_state["auth_mode"] = "signup"
            st.rerun()
    else:
        st.title("Sign Up")
        with st.form("Sign Up"):
            sign_up_email = st.text_input("Enter your email:")
            sign_up_password = st.text_input("Make a password:")
            sign_up_password_confirm = st.text_input("Confirm your password:")

            if st.form_submit_button("Create an Account"):
                if sign_up_password == sign_up_password_confirm:    

                    st.success("Account created! Please log in")
                    st.session_state["auth_mode"] = "login"
                    try:
                        # Validate email / password
                        st.success("Account created! Please log in")
                        st.session_state["auth_mode"] = "login"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error {e}")
                else:
                    pass
        
        
        
        
        
        if st.button("Already have an account? Log In"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
else:

    tab1, tab2, tab3 = st.tabs(["Onboarding", "Homepage", "Activity Form"])

    with tab1:
        onboarding()
    with tab2:
        homepage()
    with tab3:
        activity_form()

    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     onboarding()
    # with col2:
    #     homepage()
    # with col3:
    #     st.write("Hi im in col 3")
    
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.rerun()