import streamlit as st
from streamlit_calendar import calendar


def _normalize_events(raw_events):
    """Coerce LLM-shaped events into the exact dict shape streamlit-calendar wants."""
    if isinstance(raw_events, dict):
        if isinstance(raw_events.get("events"), list):
            raw_events = raw_events["events"]
        else:
            list_value = next(
                (v for v in raw_events.values() if isinstance(v, list)),
                None,
            )
            if list_value is not None:
                raw_events = list_value
            else:
                values = list(raw_events.values())
                if values and all(isinstance(v, dict) for v in values):
                    raw_events = values

    if not isinstance(raw_events, list):
        return []

    normalized = []
    for ev in raw_events:
        if not isinstance(ev, dict):
            continue
        title = ev.get("title") or ev.get("name") or "Untitled"
        start = ev.get("start") or ev.get("start_time")
        end = ev.get("end") or ev.get("end_time")
        color = ev.get("backgroundColor") or ev.get("color") or "#4287f5"
        if not start or not end:
            continue
        normalized.append({
            "title": str(title),
            "start": str(start),
            "end": str(end),
            "backgroundColor": str(color),
            "borderColor": str(color),
        })
    return normalized


def show_schedule():
    st.title("📅 Your AI Schedule")

    raw = st.session_state.get("generated_schedule")
    if raw is None:
        st.warning("No schedule found. Go generate one first.")
        st.stop()

    events = _normalize_events(raw)

    if not events:
        st.warning("Schedule is empty or in an unexpected format.")
        with st.expander("Raw response from model"):
            st.write(st.session_state.get("generated_schedule_raw", raw))
        st.stop()

    initial_date = None
    first_start = events[0].get("start", "")
    if isinstance(first_start, str) and "T" in first_start:
        initial_date = first_start.split("T")[0]

    with st.expander("Debug: events being passed to calendar"):
        st.write({"initialDate": initial_date, "events": events})

    calendar_options = {
        "initialView": "timeGridDay",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "timeGridDay,timeGridWeek,dayGridMonth",
        },
        "slotMinTime": "05:00:00",
        "slotMaxTime": "24:00:00",
        "allDaySlot": False,
        "nowIndicator": True,
        "height": 700,
    }
    if initial_date:
        calendar_options["initialDate"] = initial_date

    # Key must change when events change so the component re-mounts and renders them.
    calendar_key = "calendar_" + str(hash(str(events)))

    calendar(
        events=events,
        options=calendar_options,
        key=calendar_key,
    )
