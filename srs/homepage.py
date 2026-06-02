import streamlit as st
from datetime import date, datetime, timedelta
from firebase_admin import firestore
from firebase_utils import db


def _parse_date_field(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, str):
        return value.split("T")[0]
    return None


def _normalize_schedule_document(doc_snapshot):
    data = doc_snapshot.to_dict() or {}
    schedule_date = _parse_date_field(data.get("date"))

    if not schedule_date:
        events = data.get("events")
        if isinstance(events, list) and events:
            first_event = events[0]
            start = first_event.get("start") or first_event.get("start_time")
            if isinstance(start, str) and "T" in start:
                schedule_date = start.split("T")[0]

    if not schedule_date:
        return None

    return {
        "doc_id": doc_snapshot.id,
        "date": schedule_date,
        "events": data.get("events") if isinstance(data.get("events"), list) else [],
        "events_count": len(data.get("events")) if isinstance(data.get("events"), list) else 0,
        "created_at": data.get("created_at"),
        "wakeup_time": data.get("wakeup_time"),
        "sleep_time": data.get("sleep_time"),
        "raw": data,
    }


def _load_upcoming_schedules(uid, start_date, end_date):
    schedule_ref = db.collection("users").document(uid).collection("schedules")
    try:
        docs = schedule_ref.where("date", ">=", start_date.isoformat()).where(
            "date", "<=", end_date.isoformat()
        ).stream()
    except Exception:
        docs = schedule_ref.stream()

    schedules = []
    for doc in docs:
        schedule = _normalize_schedule_document(doc)
        if schedule:
            schedules.append(schedule)
    return schedules


def _load_previous_schedules(uid, limit=10):
    schedule_ref = db.collection("users").document(uid).collection("schedules")
    schedules = []
    try:
        docs = schedule_ref.order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
        for doc in docs:
            schedule = _normalize_schedule_document(doc)
            if schedule:
                schedules.append(schedule)
    except Exception:
        docs = schedule_ref.stream()
        for doc in docs:
            schedule = _normalize_schedule_document(doc)
            if schedule:
                schedules.append(schedule)

    schedules.sort(key=lambda item: item.get("created_at") or item.get("date"), reverse=True)
    return schedules[:limit]


def _open_schedule(schedule):
    if not schedule or not schedule.get("events"):
        return
    st.session_state["generated_schedule"] = schedule["events"]
    st.session_state["generated_schedule_raw"] = schedule["raw"]
    st.session_state["current_view"] = "schedule"
    st.rerun()


def homepage():
    st.title("🗓️ Schedule Dashboard")
    st.markdown("Use this screen to see if you already have a schedule for the next 6 days and open saved schedules instantly.")

    if "user_session" not in st.session_state or "uid" not in st.session_state["user_session"]:
        st.warning("Please log in to view your schedule dashboard.")
        return

    uid = st.session_state["user_session"]["uid"]
    today = date.today()
    day_cards = [today + timedelta(days=i) for i in range(6)]

    upcoming = _load_upcoming_schedules(uid, today, today + timedelta(days=5))
    upcoming_by_date = {item["date"]: item for item in upcoming}

    st.subheader("Next 6 days")
    for row in range(0, 6, 3):
        cols = st.columns(3)
        for index, card_date in enumerate(day_cards[row:row + 3]):
            col = cols[index]
            iso_date = card_date.isoformat()
            with col:
                label = card_date.strftime('%a, %b %d')
                if card_date == today:
                    label += " — Today"
                st.markdown(f"**{label}**")

                summary = upcoming_by_date.get(iso_date)
                if summary:
                    st.success("Scheduled")
                    st.write(f"{summary['events_count']} event(s)")
                    if st.button("View schedule", key=f"view_{iso_date}"):
                        _open_schedule(summary)
                else:
                    st.info("No saved schedule")
                    st.write("Create one from the Activity Form tab.")
                    st.button("Plan this day", key=f"plan_{iso_date}", disabled=True)

    st.markdown("---")

    previous = _load_previous_schedules(uid, limit=10)
    with st.expander("Previous schedules", expanded=True):
        if not previous:
            st.write("No previous schedules found.")
        else:
            for schedule in previous:
                cols = st.columns([4, 1, 1])
                with cols[0]:
                    st.markdown(f"**{schedule['date']}**")
                    st.write(f"{schedule['events_count']} event(s)")
                    if schedule.get("wakeup_time") and schedule.get("sleep_time"):
                        st.caption(f"Wake: {schedule['wakeup_time']} • Sleep: {schedule['sleep_time']}")
                with cols[1]:
                    created_at = schedule.get("created_at")
                    if isinstance(created_at, datetime):
                        st.write(created_at.strftime("%b %d %I:%M %p"))
                    elif isinstance(created_at, str):
                        st.write(created_at)
                    else:
                        st.write("Saved schedule")
                with cols[2]:
                    if st.button("View", key=f"prev_{schedule['doc_id']}"):
                        _open_schedule(schedule)
