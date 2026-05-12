import streamlit as st
from ai import get_json_response
from pages.calender_gen import system_prompt
import json

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

        start_fixed_time = st.time_input('Start Time', key='fixed_start')

        end_fixed_time = st.time_input('End Time', key='fixed_end')

        if st.button("Add Fixed Block"):
            fixed_time_blocks.append(
                {
                    'name' : fixed_block_name,
                    'start_time': start_fixed_time,
                    'end_time': end_fixed_time,
                }
            )
            st.rerun()

        for block in fixed_time_blocks:
            st.write(block['name'] + " " + str(block["start_time"]) + " : " + str(block["end_time"]))

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

        import json

        user_prompt = json.dumps({
            "wakeup_time": wakeup_time,
            "sleep_time": sleep_time,
            "floating_blocks": floating_time_blocks,
            "fixed_blocks": fixed_time_blocks
        })

        response = get_json_response(system_prompt, user_prompt)

        # FIX: unwrap if needed
        if isinstance(response, dict) and "events" in response:
            response = response["events"]

        st.session_state["generated_schedule"] = response

        st.switch_page("pages/schedule.py")