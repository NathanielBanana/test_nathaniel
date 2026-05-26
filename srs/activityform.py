import streamlit as st
from ai import get_json_response
from srs.calender_gen import system_prompt
import json
from firebase_utils import db
from datetime import datetime, timedelta

def _build_time_options(step_minutes=30):
    options = []
    current = datetime.strptime("12:00 AM", "%I:%M %p")
    while current.day == 1:
        options.append(current.strftime("%I:%M %p").lstrip("0"))
        current += timedelta(minutes=step_minutes)
    return options

TIME_OPTIONS = _build_time_options(30)

def format_12h_time(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        value = value.time()
    return value.strftime("%I:%M %p").lstrip("0")

def activity_form():
    if "fixed_time_blocks" not in st.session_state:
         st.session_state['fixed_time_blocks'] = []
    if "floating_time_blocks" not in st.session_state:
         st.session_state['floating_time_blocks'] = []
    fixed_time_blocks = st.session_state['fixed_time_blocks']

    floating_time_blocks =  st.session_state['floating_time_blocks']

    return_response = {}

    wakeup_time = st.select_slider(
        "What time do you usually wake up?",
        options=[
            "5:00 AM",
            "5:30 AM",
            "6:00 AM",
            "6:30 AM",
            "7:00 AM",
            "7:30 AM",
            "8:00 AM",
            "8:30 AM",            
        ]
    )
    sleep_time = st.select_slider(
        "What time do you usually go to sleep?",
        options=[
            "8:00 PM",
            "8:30 PM",
            "9:00 PM",
            "9:30 PM",
            "10:00 PM",
            "10:30 PM",
            "11:00 PM",
            "11:30 PM",
            "12:00 AM",
            
        ]
    )
    
    st.write('Add Schedule!')
    tab1, tab2 = st.tabs(["Fixed Blocks", "Floating Blocks"])

    with tab1:
        
        fixed_block_name = st.text_input("Name of the fixed block")

        start_fixed_time = st.select_slider(
            "Start Time",
            options=TIME_OPTIONS,
            key='fixed_start'
        )

        end_fixed_time = st.select_slider(
            "End Time",
            options=TIME_OPTIONS,
            key='fixed_end'
        )

        if st.button("Add Fixed Block"):
            fixed_time_blocks.append(
                {
                    'name': fixed_block_name,
                    'start_time': start_fixed_time,
                    'end_time': end_fixed_time,
                }
            )
            st.rerun()

        for block in fixed_time_blocks:
            st.write(
                block['name']
                + " "
                + format_12h_time(block["start_time"])
                + " : "
                + format_12h_time(block["end_time"])
            )

    with tab2:

        floating_block_name = st.text_input("Name of the Floating Block")

        floating_block_importance = st.select_slider(
            "How Important is this Task?",
            options=[
                'Not Important',
                'Slightly Important',
                'Important',
                'Very Important'
            ]
        )

        floating_block_difficulty = st.select_slider(
            "How difficult is this task?",
            options=[
                'Easy',
                'Normal',
                'Hard',
                'Very Hard'
            ]

        )
       
        if st.button('Add Floating Block'):
            floating_time_blocks.append(
                {
                    'name' : floating_block_name,
                    'importance' : floating_block_importance,
                    'difficulty' : floating_block_difficulty      
                }
            )
            st.rerun()
        for block in floating_time_blocks:
            st.write(block['name'] + " " + str(block["importance"]) + " : " + str(block["difficulty"]))
    
    if st.button('Generate Calendar'):


        user_prompt = json.dumps({
            "wakeup_time": wakeup_time,
            "sleep_time": sleep_time,
            "floating_blocks": floating_time_blocks,
            "fixed_blocks": fixed_time_blocks
        }, default=str)

        response = get_json_response(system_prompt, user_prompt)

        # FIX: unwrap if needed
        if isinstance(response, dict):
            list_value = next((v for v in response.values() if isinstance(v, list)), None)
            if list_value is not None:
                response = list_value

        st.session_state["generated_schedule"] = response
        st.session_state["current_view"] = "schedule"

        uid = st.session_state['user_session']['uid']

        save_data = response if isinstance(response, dict) else {"schedule": response}
        db.collection('uesrs').document(uid).collection("schedules").document(str(datetime.now())).set(save_data)
        st.rerun()