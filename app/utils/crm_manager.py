from pathlib import Path
import json

CRM_PATH = Path(__file__).resolve().parent.parent / "memory" / "crm.json"
CRM_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_crm() -> dict:

    if not CRM_PATH.exists():
        return {}

    content = CRM_PATH.read_text(encoding="utf-8").strip()

    return json.loads(content) if content else {}


def write_crm(contacts: dict) -> None:

    CRM_PATH.write_text(json.dumps(contacts, indent=2, default=str), encoding="utf-8")
