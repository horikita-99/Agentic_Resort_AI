from typing import Dict

def handle_room_service_query(message: str) -> Dict:
    text = message.lower()

    if "clean" in text:
        service = "Room cleaning"
    elif "towel" in text:
        service = "Extra towels"
    elif "pillow" in text:
        service = "Extra pillows"
    elif "blanket" in text:
        service = "Extra blankets"
    elif "laundry" in text:
        service = "Laundry service"
    else:
        service = "General room service"

    return {
        "type": "room_service",
        "service": service,
        "status": "Request has been logged and will be handled shortly."
    }
