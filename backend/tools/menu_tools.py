from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import Menu


def get_menu_by_category(
    db: Session,
    category: str
) -> List[dict]:
    """
    Fetch all menu items for a given category (fuzzy match).
    """
    category = category.lower().strip()

    items = (
        db.query(Menu)
        .filter(Menu.category.ilike(f"%{category}%"))
        .all()
    )

    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price
        }
        for item in items
    ]


def search_menu_item(
    db: Session,
    query: str
) -> List[dict]:
    """
    Search menu items by partial name.
    """
    query = query.lower().strip()

    items = (
        db.query(Menu)
        .filter(Menu.name.ilike(f"%{query}%"))
        .all()
    )

    return [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price
        }
        for item in items
    ]


def get_item_price(
    db: Session,
    item_name: str
) -> Optional[float]:
    """
    Get price of a single menu item by name.
    """
    item_name = item_name.lower().strip()

    item = (
        db.query(Menu)
        .filter(Menu.name.ilike(f"%{item_name}%"))
        .first()
    )

    return item.price if item else None
