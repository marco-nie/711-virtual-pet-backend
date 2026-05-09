from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://marco-nie.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EVENTS = []


class Event(BaseModel):
    user_id: str
    event_type: str
    item: str | None = None


@app.get("/")
def home():
    return {"message": "711 Virtual Pet Backend Running"}


@app.post("/event")
def collect_event(event: Event):
    EVENTS.append({
        "user_id": event.user_id,
        "event_type": event.event_type,
        "item": event.item,
        "timestamp": str(datetime.now())
    })
    return {"status": "success"}


@app.get("/events")
def get_events():
    return EVENTS