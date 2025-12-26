from typing import Dict, List
from datetime import datetime

# In-memory order store (mock DB)
order_state = {
    "room_number": "101",      # mock room number
    "items": [],
    "status": "IN_PROGRESS",
    "timestamp": None,
}


def add_item(item: Dict):
    item["quantity"] = 1
    order_state["items"].append(item)
    order_state["timestamp"] = datetime.now()


def get_order() -> List[Dict]:
    return order_state["items"]


def calculate_total() -> float:
    return sum(item["price"] * item["quantity"] for item in order_state["items"])


def get_metadata() -> Dict:
    return {
        "room_number": order_state["room_number"],
        "status": order_state["status"],
        "timestamp": order_state["timestamp"],
    }


def confirm_order():
    order_state["status"] = "CONFIRMED"
    order_state["timestamp"] = datetime.now()


def clear_order():
    order_state["items"] = []
    order_state["status"] = "IN_PROGRESS"
    order_state["timestamp"] = None
