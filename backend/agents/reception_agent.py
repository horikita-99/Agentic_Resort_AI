# backend/agents/reception_agent.py

from typing import Dict


def handle_reception_query(message: str) -> Dict:
    text = message.lower()

    if any(word in text for word in ["check in", "check-in"]):
        return {
            "type": "reception",
            "message": "Check-in starts at 2:00 PM. Please carry a valid ID."
        }

    if any(word in text for word in ["check out", "check-out"]):
        return {
            "type": "reception",
            "message": "Check-out time is 11:00 AM."
        }

    if any(word in text for word in ["room available", "rooms available", "any rooms", "availability", "vacant"]):
        return {
            "type": "reception",
            "message": "Rooms are available. Please specify single or double occupancy."
        }

    if any(word in text for word in ["pool", "gym", "spa", "facilities"]):
        return {
            "type": "reception",
            "message": "We have a swimming pool, gym, spa, restaurant, and free Wi-Fi."
        }

    return {
        "type": "reception",
        "message": "How can I assist you at the reception?"
    }
