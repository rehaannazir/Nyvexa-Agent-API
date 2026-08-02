import uuid
from datetime import datetime, timezone
from typing import Optional

from langchain_core.tools import tool

from app.utils.crm_manager import read_crm as _read_crm
from app.utils.crm_manager import write_crm as _write_crm


@tool
def add_contact(
    name: str, email: str, company: str = "", phone: str = "", notes: str = ""
) -> dict:
    """Add a new contact/lead to the CRM. Returns the created contact record including its id."""

    contacts = _read_crm()

    contact_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc).isoformat()

    record = {
        "id": contact_id,
        "name": name,
        "email": email,
        "company": company,
        "phone": phone,
        "notes": notes,
        "status": "new",
        "created_at": now,
        "updated_at": now,
    }

    contacts[contact_id] = record
    _write_crm(contacts)

    return record


@tool
def get_contact(contact_id: str) -> dict:
    """Fetch a single contact from the CRM by id."""

    contacts = _read_crm()
    contact = contacts.get(contact_id)

    if not contact:
        raise ValueError(f"No contact found with id '{contact_id}'.")

    return contact


@tool
def update_contact(
    contact_id: str,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    phone: Optional[str] = None,
) -> dict:
    """Update an existing contact's status, notes, or phone number."""

    contacts = _read_crm()
    contact = contacts.get(contact_id)

    if not contact:
        raise ValueError(f"No contact found with id '{contact_id}'.")

    if status is not None:
        contact["status"] = status
    if notes is not None:
        contact["notes"] = notes
    if phone is not None:
        contact["phone"] = phone

    contact["updated_at"] = datetime.now(timezone.utc).isoformat()

    contacts[contact_id] = contact
    _write_crm(contacts)

    return contact


@tool
def delete_contact(contact_id: str) -> str:
    """Delete a contact from the CRM by id."""

    contacts = _read_crm()

    if contact_id not in contacts:
        raise ValueError(f"No contact found with id '{contact_id}'.")

    del contacts[contact_id]
    _write_crm(contacts)

    return f"Contact '{contact_id}' deleted."


@tool
def search_contacts(query: str) -> list[dict]:
    """Search contacts by name, email, or company (case-insensitive substring match)."""

    contacts = _read_crm()
    query = query.lower()

    return [
        contact
        for contact in contacts.values()
        if query in contact["name"].lower()
        or query in contact["email"].lower()
        or query in contact["company"].lower()
    ]


@tool
def list_contacts(status: Optional[str] = None) -> list[dict]:
    """List all contacts, optionally filtered by status (e.g. 'new', 'contacted', 'closed')."""

    contacts = _read_crm()

    if status:
        return [
            contact
            for contact in contacts.values()
            if contact["status"].lower() == status.lower()
        ]

    return list(contacts.values())
