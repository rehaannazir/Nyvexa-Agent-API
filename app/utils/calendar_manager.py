import json
from pathlib import Path

CALENDAR_PATH = Path(__file__).resolve().parent.parent / "memory" / "calendar.json"
CALENDAR_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_calendar() -> dict:

    if not CALENDAR_PATH.exists():
        return {}

    content = CALENDAR_PATH.read_text(encoding="utf-8").strip()

    return json.loads(content) if content else {}


def write_calendar(events: dict) -> None:

    CALENDAR_PATH.write_text(json.dumps(events, indent=2, default=str), encoding="utf-8")
