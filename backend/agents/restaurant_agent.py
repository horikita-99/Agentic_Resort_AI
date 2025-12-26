from typing import Dict
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

from backend.tools.menu_tools import (
    get_menu_by_category,
    search_menu_item,
    get_item_price,
)

from backend.tools.order_tools import (
    add_item_to_order,
    view_order,
    confirm_order,
)


# ---------- LLM ----------
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)


# ---------- ACTION CLASSIFIER ----------
ACTION_PROMPT = ChatPromptTemplate.from_template(
    """
You are a restaurant assistant.

Classify the user's request into ONE action:
- SHOW_MENU (user wants to order food, see breakfast/lunch/dinner/menu)
- SEARCH_ITEM (user asks about availability of a dish)
- GET_PRICE (user asks cost/price)
- ADD_TO_ORDER (user says add/order a specific item)
- VIEW_ORDER (user wants to see current order)
- CONFIRM_ORDER (user wants to confirm order)

Respond ONLY with the action name.

User message:
{message}
"""
)


def handle_restaurant_query(message: str, db: Session) -> Dict:
    try:
        prompt = ACTION_PROMPT.format_messages(message=message)
        response = llm.invoke(prompt)
        action = response.content.strip().upper()
    except Exception:
        text_lower = message.lower()
        if "confirm" in text_lower:
            action = "CONFIRM_ORDER"
        elif "add" in text_lower:
            action = "ADD_TO_ORDER"
        elif "order" in text_lower:
            action = "SHOW_MENU"
        elif "price" in text_lower or "cost" in text_lower:
            action = "GET_PRICE"
        else:
            action = "SEARCH_ITEM"

    text = message.lower()

    # ---- ORDER VIEW / CONFIRM (GUARD) ----
    if (
        ("my order" in text or "show order" in text or "view order" in text)
        and "add" not in text
        and "confirm" not in text
    ):
        return {"type": "order_view", "data": view_order()}


    if "confirm order" in text or "place order" in text:
        return {"type": "order_confirmed", "data": confirm_order()}

    # ---- BREAKFAST ORDER SHORTCUT ----
    if "breakfast" in text and any(w in text for w in ["order", "want", "have", "get", "show", "see", "display"]):
        items = get_menu_by_category(db, "Breakfast")
        return {"type": "menu", "category": "Breakfast", "data": items[:10]}

    # ---- SHOW MENU ----
    if action == "SHOW_MENU":
        category_map = {
            "non-veg starters": "Non-Veg Starters",
            "non veg starters": "Non-Veg Starters",
            "non-veg main course": "Non-Veg Main Course",
            "veg starters": "Veg Starters",
            "veg main course": "Veg Main Course",
            "breakfast": "Breakfast",
            "desserts": "Desserts",
            "drinks": "Drinks",
            "beverages": "Drinks",
        }

        category = "Breakfast"
        for pattern, db_category in category_map.items():
            if pattern in text:
                category = db_category
                break

        items = get_menu_by_category(db, category)
        return {"type": "menu", "category": category, "data": items[:10]}

    # ---- GET PRICE ----
    if action == "GET_PRICE":
        for w in ["price", "cost", "how much", "of", "the", "?"]:
            text = text.replace(w, "")
        price = get_item_price(db, text.strip())
        return {"type": "price", "item": text.title(), "data": price}

    # ---- ADD TO ORDER ----
    if action == "ADD_TO_ORDER":
        for w in ["add", "to", "my", "order", "please"]:
            text = text.replace(w, "")
        result = add_item_to_order(db, text.strip())
        return {"type": "order_add", "data": result}

    # ---- CATEGORY CHECK (before search) ----
    # If user is asking to show/see a category, handle it as menu display
    category_keywords = {
        "breakfast": "Breakfast",
        "lunch": "Non-Veg Main Course",  # Default to main course
        "dinner": "Non-Veg Main Course",
        "desserts": "Desserts",
        "dessert": "Desserts",
        "drinks": "Drinks",
        "beverages": "Drinks",
        "starters": "Veg Starters",
        "main course": "Veg Main Course",
    }
    
    if any(word in text for word in ["show", "see", "display", "list", "menu"]):
        for keyword, category in category_keywords.items():
            if keyword in text:
                items = get_menu_by_category(db, category)
                return {"type": "menu", "category": category, "data": items[:10]}

    # ---- SEARCH ----
    for p in ["do you have", "any", "is there", "can i get", "?"]:
        text = text.replace(p, "")
    items = search_menu_item(db, text.strip())
    return {"type": "search", "data": items[:10]}
