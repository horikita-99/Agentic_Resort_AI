from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from backend.db.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float, nullable=False)


class Room(Base):
    __tablename__ = "rooms"

    room_number = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="Available")


class RestaurantOrder(Base):
    __tablename__ = "restaurant_orders"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, nullable=False)
    items = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")
    timestamp = Column(DateTime, default=datetime.utcnow)


class RoomServiceRequest(Base):
    __tablename__ = "room_service_requests"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, nullable=False)
    request_type = Column(String, nullable=False)
    status = Column(String, default="Pending")
    timestamp = Column(DateTime, default=datetime.utcnow)
