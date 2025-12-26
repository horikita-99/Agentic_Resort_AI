# backend/main.py

from dotenv import load_dotenv
load_dotenv()

from backend.agents.router_agent import route_intent
from backend.agents.restaurant_agent import handle_restaurant_query
from backend.db.database import SessionLocal


def chat():
    print("🏨 Welcome to Resort AI Assistant")
    print("Type 'exit' to quit\n")

    db = SessionLocal()

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        intent = route_intent(user_message)

        if intent == "RESTAURANT":
            from backend.agents.restaurant_agent import handle_restaurant_query
            response = handle_restaurant_query(user_message, db)

        elif intent == "RECEPTION":
            from backend.agents.reception_agent import handle_reception_query
            response = handle_reception_query(user_message)

        elif intent == "ROOM_SERVICE":
            from backend.agents.room_service import handle_room_service_query
            response = handle_room_service_query(user_message)


        else:
            response = {
                "type": "error",
                "message": "Sorry, I didn't understand that."
            }

        print("Bot:", response)


if __name__ == "__main__":
    chat()
