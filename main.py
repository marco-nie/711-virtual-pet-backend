from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import os
from behavior import get_user_profile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://marco-nie.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "events.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            event_type TEXT,
            item TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


class Event(BaseModel):
    user_id: str
    event_type: str
    item: str | None = None


@app.get("/")
def home():
    return {"message": "711 Virtual Pet Backend Running"}


@app.post("/event")
def collect_event(event: Event):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO events (user_id, event_type, item, timestamp) VALUES (?, ?, ?, ?)",
        (event.user_id, event.event_type, event.item, str(datetime.now()))
    )
    conn.commit()
    conn.close()
    return {"status": "success"}


@app.get("/events")
def get_events():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT user_id, event_type, item, timestamp FROM events").fetchall()
    conn.close()
    return [
        {"user_id": r[0], "event_type": r[1], "item": r[2], "timestamp": r[3]}
        for r in rows
    ]

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    return get_user_profile(user_id)

@app.get("/predict/{user_id}")
def predict(user_id: str):
    from behavior import generate_prediction_message
    message = generate_prediction_message(user_id)
    return {"prediction": message}