import streamlit as st
from datetime import date
from srs.onboarding import onboarding
from srs.homepage import homepage
from srs.activityform import activity_form
from srs.calender_gen import calender_gen
from firebase_utils import db, auth

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
            log_in_password = st.text_input("Enter your account password:", type='password')

            if st.form_submit_button("Log In"):
                try:
                    user = auth.sign_in_with_email_and_password(log_in_email, log_in_password)
                    st.session_state["logged_in"] = True

                    user_doc = db.collection('users').document(user["localId"]).get()
                    user_dict = user_doc.to_dict()
                    st.session_state["user"] = user_dict
                    st.session_state["user_session"] = {
                        "uid": user["localId"],
                        "id_token": user["idToken"],
                        "refresh_token": user["refreshToken"]
                    }
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
            sign_up_password = st.text_input("Make a password:", type='password')
            sign_up_password_confirm = st.text_input("Confirm your password:", type='password')

            if st.form_submit_button("Create an Account"):
                if sign_up_password == sign_up_password_confirm:    


                    try:
                        user = auth.create_user_with_email_and_password(sign_up_email, sign_up_password)
                        uid = user["localId"]

                        db.collection('users').document(uid).set({
                            "onboarding_complete": False,
                            "name": "",
                            "age": 0,
                            "email": sign_up_email,
                            "completed_onboarding": False
                        })

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
    if not st.session_state["user"]["completed_onboarding"]:
        onboarding()
    else:

        tab1, tab2 = st.tabs(["Homepage", "Activity Form"])


        with tab1:
            homepage()
        with tab2:
            activity_form()

    
        if st.button("Log Out"):
            st.session_state["logged_in"] = False
            st.rerun()