## Agentic Resort AI Assistant

### Overview

Agentic Resort AI Assistant simulates a real-world resort environment where different departments are handled by specialized AI agents.
A central Router Agent classifies user intent and routes queries to the appropriate department agent.

The system supports:

- Natural language guest interaction

- Food ordering and bill calculation

- Room service requests

- Reception FAQs

- Live operational visibility via dashboard

This project demonstrates agentic AI design, LLM orchestration, and modular backend architecture.


## System Architecture

### High-Level Flow
```text
                       User Input
                           ↓
          Router Agent (Intent Classification)
                           ↓
+----------------+--------------------+--------------------+
| Reception Agent | Restaurant Agent | Room Service Agent |
+----------------+--------------------+--------------------+
         ↓                 ↓                   ↓
     Static / DB     Menu + Orders      Service Requests
                           ↓
            Operational Dashboard (Streamlit)
```                 

## Core Components
###
**1️. Router Agent**

**Purpose**:
Routes each user message to the appropriate department agent.

How it works:

Uses an LLM (ChatOpenAI) for intent classification

Supported intents:

-   RECEPTION

-   RESTAURANT

-   ROOM_SERVICE

Includes keyword-based fallback for reliability

Why:
Prevents overloading a single agent and ensures clean responsibility separation.
##
### **2️. Receptionist Agent**

Handles general resort enquiries.

Capabilities:

-   Check-in time

-   Check-out time

-   Facility information (gym, spa, pool, Wi-Fi)

-   Room availability (mocked)

Implementation:

Static responses stored in config / code

Mock room availability logic (acceptable per assignment)
##
### **3️. Restaurant Agent (LLM-Driven)**

Handles the complete food ordering workflow.

Capabilities:

-   Show menu by category

-   Search food items

-   Get item prices

-   Add items to order

-   View current order

-   Confirm order & calculate bill

**Key Design Choices:**

- Hybrid Intent Handling

  -   LLM for flexible natural language understanding

  -   Deterministic rule guards for critical flows (e.g., “show breakfast”)

- Uses SQLAlchemy to fetch menu data

- Uses in-memory order store (can be replaced by DB/Redis later)

**Order Data Structure Includes:**

-   Ordered items

-   Item prices

-   Total amount

-   Timestamp

-   Order status
##
### **4️. Order Memory & Tools**

Purpose:
Maintain state across conversation turns.

Current Implementation:

In-memory Python store

Functions:

  -  add_item

  -  view_order

  -  calculate_total

  -  confirm_order

Note:
Designed for easy migration to persistent storage.
##
### **5️. Room Service Agent**

Handles service requests from guests.

Capabilities:

-   Room cleaning

-   Laundry

-   Extra amenities (towels, pillows, blankets, toiletries)

Request Data Includes:

-   Room number (mocked)

-   Request type

-   Timestamp

-   Status (Pending / In Progress / Completed)
##
### **6️. Resort Operations Dashboard**

Built using Streamlit.

Displays:

-   Restaurant orders

-   Order totals

-   Room service requests

-   Request statuses

Purpose:
Provides a simple operational view for staff.

##  Tech Stack
###
-   Python 3

-   LangChain + OpenAI (ChatOpenAI)

-   SQLAlchemy

-   SQLite

-   Streamlit (Dashboard)

-   Pandas (Excel data ingestion)
  
##  How to Run
###
1️. Install dependencies
pip install -r requirements.txt

2️. Set OpenAI API Key
Create a .env file:
OPENAI_API_KEY=your_api_key_here

3️. Run the Chat Assistant
python -m backend.main

4️. Run the Dashboard (Optional)
streamlit run dashboard/app.py


##  Dashboard Screenshots
###
Resort Operations Dashboard
![Dashboard Home](screenshots/Dashboard_home.png)

Restaurant Order Workflow
![Restaurant Orders](screenshots/restaurant_order.jpg)
