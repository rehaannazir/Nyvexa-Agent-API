import uuid
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool

from app.utils.calendar_manager import read_calendar as _read_calendar
from app.utils.calendar_manager import write_calendar as _write_calendar


def _parse(dt: str) -> datetime:

    try:
        return datetime.fromisoformat(dt)
    except ValueError:
        raise ValueError(f"'{dt}' is not a valid ISO 8601 datetime (e.g. 2026-08-03T14:00:00).")


def _overlaps(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:

    return start_a < end_b and start_b < end_a


def _find_conflict(
    events: dict, start: datetime, end: datetime, exclude_id: Optional[str] = None
) -> Optional[dict]:

    for event in events.values():
        if event["id"] == exclude_id:
            continue

        if _overlaps(start, end, _parse(event["start_time"]), _parse(event["end_time"])):
            return event

    return None


@tool
def schedule_event(
    title: str, start_time: str, end_time: str, attendee: str = "", notes: str = ""
) -> dict:
    """Schedule a new calendar event. Times must be ISO 8601 (e.g. 2026-08-03T14:00:00).
    Fails if the slot conflicts with an existing event."""

    start = _parse(start_time)
    end = _parse(end_time)

    if end <= start:
        raise ValueError("end_time must be after start_time.")

    events = _read_calendar()

    conflict = _find_conflict(events, start, end)
    if conflict:
        raise ValueError(
            f"Time slot conflicts with existing event '{conflict['title']}' "
            f"({conflict['start_time']} - {conflict['end_time']})."
        )

    event_id = uuid.uuid4().hex[:8]

    record = {
        "id": event_id,
        "title": title,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "attendee": attendee,
        "notes": notes,
        "status": "scheduled",
    }

    events[event_id] = record
    _write_calendar(events)

    return record


@tool
def get_event(event_id: str) -> dict:
    """Fetch a single calendar event by id."""

    events = _read_calendar()
    event = events.get(event_id)

    if not event:
        raise ValueError(f"No event found with id '{event_id}'.")

    return event


@tool
def update_event(
    event_id: str,
    title: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    notes: Optional[str] = None,
) -> dict:
    """Update an existing event's title, time, or notes. Re-checks for conflicts if the time changes."""

    events = _read_calendar()
    event = events.get(event_id)

    if not event:
        raise ValueError(f"No event found with id '{event_id}'.")

    new_start = _parse(start_time) if start_time else _parse(event["start_time"])
    new_end = _parse(end_time) if end_time else _parse(event["end_time"])

    if new_end <= new_start:
        raise ValueError("end_time must be after start_time.")

    if start_time or end_time:
        conflict = _find_conflict(events, new_start, new_end, exclude_id=event_id)
        if conflict:
            raise ValueError(
                f"Time slot conflicts with existing event '{conflict['title']}' "
                f"({conflict['start_time']} - {conflict['end_time']})."
            )

    if title is not None:
        event["title"] = title
    if notes is not None:
        event["notes"] = notes

    event["start_time"] = new_start.isoformat()
    event["end_time"] = new_end.isoformat()

    events[event_id] = event
    _write_calendar(events)

    return event


@tool
def cancel_event(event_id: str) -> str:
    """Cancel (delete) a calendar event by id."""

    events = _read_calendar()

    if event_id not in events:
        raise ValueError(f"No event found with id '{event_id}'.")

    del events[event_id]
    _write_calendar(events)

    return f"Event '{event_id}' cancelled."


@tool
def list_events(date: Optional[str] = None) -> list[dict]:
    """List all calendar events, optionally filtered to a single date (YYYY-MM-DD)."""

    events = list(_read_calendar().values())

    if date:
        events = [e for e in events if e["start_time"].startswith(date)]

    return sorted(events, key=lambda e: e["start_time"])


@tool
def check_availability(start_time: str, end_time: str) -> bool:
    """Check whether a given time slot is free (True) or conflicts with an existing event (False)."""

    start = _parse(start_time)
    end = _parse(end_time)

    if end <= start:
        raise ValueError("end_time must be after start_time.")

    return _find_conflict(_read_calendar(), start, end) is None
