# backend/agents/router_agent.py

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


# ---------- Intent Labels ----------
RECEPTION = "RECEPTION"
RESTAURANT = "RESTAURANT"
ROOM_SERVICE = "ROOM_SERVICE"


# ---------- LLM Setup ----------
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


# ---------- Prompt ----------
ROUTER_PROMPT = ChatPromptTemplate.from_template(
    """
You are an intent router for a resort chatbot.

Classify the user's request into exactly ONE of the following categories:
- RECEPTION: check-in, check-out, facilities, room availability, general queries
- RESTAURANT: menu, food ordering, prices, bill
- ROOM_SERVICE: cleaning, laundry, towels, pillows, blankets, amenities

Respond with ONLY the category name.

User message:
{message}
"""
)


# ---------- Keyword Fallback ----------
def keyword_fallback(message: str) -> str:
    msg = message.lower()

    if any(word in msg for word in ["order", "menu", "food", "eat",
        "price", "cost", "how much",
        "starter", "starters",
        "dish", "item",
        "veg", "non-veg", "non veg",
        "appetizer", "main course",
        "dessert", "desserts",
        "breakfast", "lunch", "dinner"]):
        return RESTAURANT

    if any(word in msg for word in ["clean", "laundry", "towel", "pillow", "blanket", "amenities","room service","housekeeping"]):
        return ROOM_SERVICE

    return RECEPTION


# ---------- Router Function ----------
def route_intent(
    message: str,
    history: List[str] | None = None
) -> str:
    """
    Routes user message to the correct department agent.
    """

    try:
        prompt = ROUTER_PROMPT.format_messages(message=message)
        response = llm.invoke(prompt)
        intent = response.content.strip().upper()

        if intent in {RECEPTION, RESTAURANT, ROOM_SERVICE}:
            return intent

        return keyword_fallback(message)

    except Exception:
        # Safety fallback if LLM fails
        return keyword_fallback(message)
