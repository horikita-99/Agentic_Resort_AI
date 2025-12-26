#!/usr/bin/env python3
"""
Test script for the restaurant agent.
"""

from dotenv import load_dotenv
load_dotenv()

from backend.db.database import SessionLocal, engine
from backend.db.models import Base
from backend.agents.restaurant_agent import handle_restaurant_query

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a database session
db = SessionLocal()

try:
    # Test queries
    test_queries = [
        "Show non veg starters",
        "What's the price of pizza?",
        "I want to see the menu",
        "Do you have pasta?",
    ]
    
    print("Testing Restaurant Agent...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        result = handle_restaurant_query(query, db)
        print(f"Result Type: {result['type']}")
        
        if result['type'] == 'price':
            price = result['data']
            print(f"Price: Rs.{price}" if price else "Item not found")
        elif result['type'] == 'menu':
            items = result['data']
            print(f"Items found: {len(items)}")
            for item in items[:5]:  # Show first 5
                print(f"  - {item['name']}: Rs.{item['price']}")
        elif result['type'] == 'search':
            items = result['data']
            print(f"Items found: {len(items)}")
            for item in items[:5]:  # Show first 5
                print(f"  - {item['name']} ({item.get('category', 'N/A')}): Rs.{item['price']}")
        
        print("-" * 60)
        
finally:
    db.close()

