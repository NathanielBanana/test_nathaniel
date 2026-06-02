import streamlit as st
from ai import get_json_response
from srs.calender_gen import system_prompt
import json
from firebase_utils import db
from datetime import datetime, date, timedelta

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



def _extract_events(response):
    """Normalize whatever the LLM returned into a list of event dicts."""
    if response is None:
        return []

    if isinstance(response, list):
        return [ev for ev in response if isinstance(ev, dict)]

    if isinstance(response, dict):
        if isinstance(response.get("events"), list):
            return [ev for ev in response["events"] if isinstance(ev, dict)]

        for value in response.values():
            if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
                return value

        values = list(response.values())
        if values and all(isinstance(v, dict) for v in values):
            return values

    return []


def activity_form():
    if "fixed_time_blocks" not in st.session_state:
        st.session_state["fixed_time_blocks"] = []
    if "floating_time_blocks" not in st.session_state:
        st.session_state["floating_time_blocks"] = []

    fixed_time_blocks = st.session_state["fixed_time_blocks"]
    floating_time_blocks = st.session_state["floating_time_blocks"]

    schedule_date = st.date_input("Schedule date", value=date.today())

    wakeup_time = st.select_slider(
        "What time will you wake up?",
        options=[
            "5:00 AM", "5:30 AM", "6:00 AM", "6:30 AM",
            "7:00 AM", "7:30 AM", "8:00 AM", "8:30 AM",
        ],
    )
    sleep_time = st.select_slider(
        "What time will you go to sleep?",
        options=[
            "8:00 PM", "8:30 PM", "9:00 PM", "9:30 PM",
            "10:00 PM", "10:30 PM", "11:00 PM", "11:30 PM", "12:00 AM",
        ],
    )

    st.write("Add Schedule!")
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

        fixed_in_person = st.toggle("In-person activity?", value=False, key='fixed_in_person')

        fixed_travel_time = None
        if fixed_in_person:
            fixed_travel_time = st.number_input(
                "How many minutes travel time?",
                min_value=0,
                max_value=120,
                value=15,
                key='fixed_travel_time'
            )
        
        if st.button("Add Fixed Block"):
            if not fixed_block_name.strip():
                st.error("Please enter a fixed block name.")
            elif TIME_OPTIONS.index(end_fixed_time) <= TIME_OPTIONS.index(start_fixed_time):
                st.error("End time must be later than start time.")
            else:
                fixed_time_blocks.append(
                    {
                        'name': fixed_block_name,
                        'start_time': start_fixed_time,
                        'end_time': end_fixed_time,
                        'in_person': fixed_in_person,
                        'travel_time_minutes': fixed_travel_time,
                    }
                )
                st.rerun()

        for block in fixed_time_blocks:
            display_text = (
                block['name']
                + " "
                + format_12h_time(block["start_time"])
                + " - "
                + format_12h_time(block["end_time"])
            )
            if block.get('in_person'):
                travel_time = block.get('travel_time_minutes', 0)
                display_text += f" [In-person, {travel_time} min travel]"
            st.write(display_text)

    with tab2:
        floating_block_name = st.text_input("Name of the Floating Block")
        floating_block_importance = st.select_slider(
            "How Important is this Task?",
            options=["Not Important", "Slightly Important", "Important", "Very Important"],
        )
        floating_block_difficulty = st.select_slider(
            "How difficult is this task?",
            options=["Easy", "Normal", "Hard", "Very Hard"],
        )

        float_in_person = st.toggle("In-person activity?", value=False, key='float_in_person')

        float_travel_time = None
        if float_in_person:
            float_travel_time = st.number_input(
                "How many minutes travel time?",
                min_value=0,
                max_value=120,
                value=15,
                key='float_travel_time'
            )

        if st.button("Add Floating Block"):
            floating_time_blocks.append({
                "name": floating_block_name,
                "importance": floating_block_importance,
                "difficulty": floating_block_difficulty,
                "in_person": float_in_person,
                "travel_time_minutes": float_travel_time,
            })
            st.rerun()

        for block in floating_time_blocks:
            display_text = f"{block['name']} {block['importance']} : {block['difficulty']}"
            if block.get('in_person'):
                travel_time = block.get('travel_time_minutes', 0)
                display_text += f" [In-person, {travel_time} min travel]"
            st.write(display_text)

    if st.button("Generate Calendar"):
        user_payload = {
            "date": schedule_date.isoformat(),
            "wakeup_time": wakeup_time,
            "sleep_time": sleep_time,
            "fixed_blocks": fixed_time_blocks,
            "floating_blocks": floating_time_blocks,
        }
        user_prompt = json.dumps(user_payload, default=str)

        try:
            response = get_json_response(system_prompt, user_prompt)
        except Exception as e:
            st.error(f"Failed to generate schedule: {e}")
            return

        events = _extract_events(response)

        if not events:
            st.error("The model did not return any events. Raw response shown below — try again or adjust inputs.")
            st.write(response)
            return

        st.session_state["generated_schedule"] = events
        st.session_state["generated_schedule_raw"] = response
        st.session_state["current_view"] = "schedule"

        uid = st.session_state["user_session"]["uid"]
        save_doc = {
            "date": schedule_date.isoformat(),
            "created_at": datetime.now(),
            "wakeup_time": wakeup_time,
            "sleep_time": sleep_time,
            "fixed_blocks": fixed_time_blocks,
            "floating_blocks": floating_time_blocks,
            "events": events,
        }
        db.collection("users").document(uid).collection("schedules").document(
            f"{schedule_date.isoformat()}-{datetime.now().strftime('%H%M%S')}"
        ).set(save_doc)

        st.rerun()
