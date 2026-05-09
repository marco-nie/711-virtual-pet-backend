import sqlite3
from datetime import datetime
from collections import Counter

DB_PATH = "events.db"


def get_user_events(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT item, timestamp FROM events WHERE user_id = ? AND event_type = 'purchase'",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_favorite_item(events):
    if not events:
        return None
    items = [e[0] for e in events if e[0]]
    if not items:
        return None
    return Counter(items).most_common(1)[0][0]


def get_time_of_day(events):
    if not events:
        return None
    hours = []
    for _, timestamp in events:
        try:
            hour = datetime.fromisoformat(timestamp).hour
            hours.append(hour)
        except:
            continue
    if not hours:
        return None
    avg_hour = sum(hours) / len(hours)
    if avg_hour < 12:
        return "morning"
    elif avg_hour < 17:
        return "afternoon"
    else:
        return "evening"


def generate_pet_message(user_id: str):
    events = get_user_events(user_id)

    if not events:
        return f"Hi! I'm so happy to meet you! Go buy something from the store!"

    favorite = get_favorite_item(events)
    time_of_day = get_time_of_day(events)
    total = len(events)

    if total == 1:
        return f"Thanks for your first purchase! Keep it up!"

    if favorite and time_of_day:
        return f"I know you love your {favorite} in the {time_of_day}! You've treated me {total} times!"

    if favorite:
        return f"Your favorite is {favorite}! You've bought it {total} times total!"

    return f"Thanks for {total} purchases! You're the best!"


def get_user_profile(user_id: str):
    events = get_user_events(user_id)
    favorite = get_favorite_item(events)
    time_of_day = get_time_of_day(events)
    message = generate_pet_message(user_id)

    return {
        "user_id": user_id,
        "total_purchases": len(events),
        "favorite_item": favorite,
        "shopping_time": time_of_day,
        "pet_message": message
    }