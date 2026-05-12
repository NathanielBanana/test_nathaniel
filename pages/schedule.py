import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

st.title("📅 Your AI Schedule")

# safety check
if "generated_schedule" not in st.session_state:
    st.warning("No schedule found. Go generate one first.")
    st.stop()

tasks = st.session_state["generated_schedule"]

today = datetime.now().date()
events = []

for task in tasks:
    start_time = task.get("start_time", "15:00")
    end_time = task.get("end_time", "16:00")

    importance = task.get("importance")

    if importance == "Very Important":
        color = "#FF4B4B"
    elif importance == "Important":
        color = "#FF8C42"
    else:
        color = "#6CD4FF"

    events.append({
        "title": f"{task['name']} ({task.get('difficulty','')})",
        "start": f"{today}T{start_time}",
        "end": f"{today}T{end_time}",
        "backgroundColor": color,
    })

calendar_options = {
    "initialView": "timeGridDay",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "timeGridDay,timeGridWeek,dayGridMonth",
    },
}

calendar_component = calendar(
    events=events,
    options=calendar_options,
    key="calendar"
)

st.write(calendar_component)