import streamlit as st

fixed_time_blocks = []

floating_time_blocks = []

def activity_form():
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
            "9:00 AM",
            
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
    tab1, tab2 = st.tabs(["Fixed Blocks', Floating Blocks"])

    with tab1:
        
        fixed_block_name = st.text_input("Name of the fixed block")

        start_fixed_time = st.time_input('Start Time')

        end_fixed_time = st.time_input('End Time')

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

        start_floating_time = st.time_input('Start Time')

        end_floating_time = st.time_input('End Time')

        if st.button('Add Floating Block'):
            floating_time_blocks.append(
                {
                    'name' : floating_block_name,
                    'start_time': start_floating_time,
                    'end_time': end_floating_time,
                }
            )
            st.rerun()
        for block in floating_time_blocks:
            st.write(block['name'] + " " + str(block["start_time"]) + " : " + str(block["end_time"]))

        