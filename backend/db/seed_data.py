# backend/db/seed_data.py

import pandas as pd
from sqlalchemy.orm import Session
from backend.db.database import engine, SessionLocal
from backend.db.models import Base, Menu, Room

MENU_FILE_PATH = "data/restaurant_menu.xlsx"


def seed_menu(db: Session):
    # Prevent duplicate seeding
    if db.query(Menu).first():
        print("Menu already seeded.")
        return

    # Read ALL sheets
    excel_data = pd.read_excel(MENU_FILE_PATH, sheet_name=None)

    for category, df in excel_data.items():
        for _, row in df.iterrows():
            item = Menu(
                name=row["Item Name"],
                category=category,              # Sheet name = category
                price=float(row["Price (₹)"])
            )
            db.add(item)

    db.commit()
    print("Menu seeded successfully from all sheets.")


def seed_rooms(db: Session):
    if db.query(Room).first():
        print("Rooms already seeded.")
        return

    for room_number in range(101, 111):
        db.add(Room(room_number=room_number, status="Available"))

    db.commit()
    print("Rooms seeded successfully.")


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_menu(db)
        seed_rooms(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
