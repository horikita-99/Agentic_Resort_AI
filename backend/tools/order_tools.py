# backend/tools/order_tools.py

from sqlalchemy.orm import Session
from backend.db.models import Menu
from backend.memory.order_memory import (
    add_item,
    get_order,
    calculate_total,
    confirm_order as memory_confirm_order,
    get_metadata,
)

def add_item_to_order(db: Session, item_name: str):
    item = (
        db.query(Menu)
        .filter(Menu.name.ilike(f"%{item_name}%"))
        .first()
    )

    if not item:
        return {"error": "Item not found"}

    add_item({
        "id": item.id,
        "name": item.name,
        "price": item.price,
    })

    return {"added": item.name, "price": item.price}


def view_order():
    return {
        "items": get_order(),
        "total": calculate_total(),
        "metadata": get_metadata(),
    }


def confirm_order():
    memory_confirm_order()  # ✅ correct function call

    return {
        "items": get_order(),
        "total": calculate_total(),
        "metadata": get_metadata(),
    }







