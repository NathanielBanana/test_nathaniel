import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth as admin_auth
import pyrebase

@st.cache_resource
def _init_admin():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

@st.cache_resource
def _init_pyrebase():
    return pyrebase.initialize_app(dict(st.secrets["firebase_web"])).auth()

db = _init_admin()
auth = _init_pyrebase()