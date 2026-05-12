import streamlit as st
from streamlit_calendar import calendar

st.title("📅 Your AI Schedule")

# safety check
if "generated_schedule" not in st.session_state:
    st.warning("No schedule found. Go generate one first.")
    st.stop()

events = st.session_state["generated_schedule"]

# unwrap if the AI returned a dict wrapper
if isinstance(events, dict):
    # find the first list value in the dict
    list_value = next((v for v in events.values() if isinstance(v, list)), None)
    if list_value is not None:
        events = list_value
    else:
        # maybe it's a dict whose values are individual event objects
        values = list(events.values())
        if values and all(isinstance(v, dict) for v in values):
            events = values

if not isinstance(events, list) or len(events) == 0:
    st.warning("Schedule is empty or in an unexpected format.")
    st.write(events)
    st.stop()

# normalize events that came back with raw input field names instead of calendar field names
normalized = []
for ev in events:
    if not isinstance(ev, dict):
        continue
    title = ev.get("title") or ev.get("name") or "Untitled"
    start = ev.get("start") or ev.get("start_time")
    end = ev.get("end") or ev.get("end_time")
    color = ev.get("backgroundColor") or ev.get("color") or "#4287f5"
    if not start or not end:
        continue
    normalized.append({
        "title": title,
        "start": str(start),
        "end": str(end),
        "backgroundColor": color,
    })
events = normalized

if len(events) == 0:
    st.warning("No valid events found.")
    st.stop()

# pick an initial date from the first event so the calendar lands on the right day
initial_date = None
first_start = events[0].get("start", "")
if isinstance(first_start, str) and "T" in first_start:
    initial_date = first_start.split("T")[0]

calendar_options = {
    "initialView": "timeGridDay",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "timeGridDay,timeGridWeek,dayGridMonth",
    },
}
if initial_date:
    calendar_options["initialDate"] = initial_date

calendar_component = calendar(
    events=events,
    options=calendar_options,
    key="calendar"
)

st.write(calendar_component)
