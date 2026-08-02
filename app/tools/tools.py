from app.tools.calculator import calculator
from app.tools.crm import (
    add_contact,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    list_contacts,
)
from app.tools.calender import (
    schedule_event,
    get_event,
    update_event,
    cancel_event,
    list_events,
    check_availability,
)

TOOLS = [
    calculator,
    add_contact,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    list_contacts,
    schedule_event,
    get_event,
    update_event,
    cancel_event,
    list_events,
    check_availability,
]
