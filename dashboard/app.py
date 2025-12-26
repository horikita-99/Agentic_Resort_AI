# dashboard/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()


import streamlit as st
from backend.db.database import SessionLocal
from backend.tools.menu_tools import get_menu_by_category
from backend.tools.order_tools import view_order, confirm_order
from backend.agents.restaurant_agent import handle_restaurant_query

# DB session
db = SessionLocal()

st.set_page_config(page_title="Resort AI Dashboard", layout="wide")

st.title("🏨 Resort AI Dashboard")

# ---------------- MENU SECTION ----------------
st.header("🍽 Restaurant Menu")

category = st.selectbox(
    "Select Menu Category",
    [
        "Breakfast",
        "Veg Starters",
        "Non-Veg Starters",
        "Veg Main Course",
        "Non-Veg Main Course",
        "Desserts",
        "Drinks"
    ],
)

menu_items = get_menu_by_category(db, category)

if not menu_items:
    st.warning("No items found for this category.")

for item in menu_items:
    col1, col2, col3 = st.columns([5, 2, 2])
    col1.write(item["name"])
    col2.write(f"₹ {item['price']}")
    if col3.button(f"Add {item['name']}", key=item["id"]):
        handle_restaurant_query(f"add {item['name']} to my order", db)
        st.success(f"{item['name']} added to order")


# ---------------- CHAT ASSISTANT ----------------
st.divider()
st.header("💬 Resort AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask something (menu, room service, reception):")

if st.button("Send") and user_input:
    from backend.agents.router_agent import route_intent
    from backend.agents.restaurant_agent import handle_restaurant_query
    from backend.agents.room_service import handle_room_service_query
    from backend.agents.reception_agent import handle_reception_query

    intent = route_intent(user_input)

    if intent == "RESTAURANT":
        response = handle_restaurant_query(user_input, db)
    elif intent == "ROOM_SERVICE":
        response = handle_room_service_query(user_input)
    else:
        response = handle_reception_query(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for speaker, msg in st.session_state.chat_history:
    st.write(f"**{speaker}:** {msg}")




# ---------------- ORDER SECTION ----------------
st.divider()
st.header("🧾 Current Order")

order = view_order()

if order["items"]:
    for item in order["items"]:
        st.write(f"- {item['name']} : ₹ {item['price']}")
    st.subheader(f"Total: ₹ {order['total']}")
else:
    st.info("No items in order.")

if st.button("✅ Confirm Order"):
    confirmed = confirm_order()
    st.success(f"Order confirmed! Total bill: ₹ {confirmed['total']}")
