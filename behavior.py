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


def get_current_time_of_day():
    hour = datetime.now().hour
    if hour < 12:
        return "morning"
    elif hour < 17:
        return "afternoon"
    else:
        return "evening"


def predict_next_item(user_id: str):
    events = get_user_events(user_id)
    if not events:
        return None

    current_time = get_current_time_of_day()

    time_items = []
    for item, timestamp in events:
        try:
            hour = datetime.fromisoformat(timestamp).hour
            if current_time == "morning" and hour < 12:
                time_items.append(item)
            elif current_time == "afternoon" and 12 <= hour < 17:
                time_items.append(item)
            elif current_time == "evening" and hour >= 17:
                time_items.append(item)
        except:
            continue

    if time_items:
        return Counter(time_items).most_common(1)[0][0]

    return get_favorite_item(events)


def generate_prediction_message(user_id: str):
    prediction = predict_next_item(user_id)
    current_time = get_current_time_of_day()

    if not prediction:
        return None

    messages = {
        "coffee": f"Ready for your {current_time} coffee? ☕ I've been waiting!",
        "onigiri": f"Feeling hungry? Your usual onigiri sounds perfect right now! 🍙",
        "sandwich": f"How about your favorite sandwich? 🥪 You deserve it!",
        "juice": f"Time for your {current_time} juice? 🧃 Stay refreshed!",
    }

    return messages.get(prediction, f"How about some {prediction}? I think you'd love it right now!")


def generate_pet_message(user_id: str):
    events = get_user_events(user_id)

    if not events:
        return "Hi! I'm so happy to meet you! Go buy something from the store!"

    favorite = get_favorite_item(events)
    time_of_day = get_time_of_day(events)
    total = len(events)

    if total == 1:
        return "Thanks for your first purchase! Keep it up!"

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
    prediction_message = generate_prediction_message(user_id)

    return {
        "user_id": user_id,
        "total_purchases": len(events),
        "favorite_item": favorite,
        "shopping_time": time_of_day,
        "pet_message": message,
        "prediction_message": prediction_message
    }

import random

ADVENTURE_TEMPLATES = {
    "coffee": [
        "I sneaked into a 7-Eleven and found something amazing for you!",
        "I went on a morning adventure and discovered a secret deal!",
        "I explored the neighborhood and found your favorite waiting for you!",
    ],
    "onigiri": [
        "I went on a food adventure and found the freshest onigiri in town!",
        "I explored every aisle and found something delicious just for you!",
        "I went on an adventure and your favorite snack is calling your name!",
    ],
    "sandwich": [
        "I went on a lunch adventure and found the perfect deal!",
        "I explored the 7-Eleven and found something hearty for you!",
        "I went on an adventure and discovered your sandwich is waiting!",
    ],
    "juice": [
        "I went on a refreshing adventure and found the perfect drink!",
        "I explored and found something to keep you energized!",
        "I went on an adventure and your favorite juice is on special!",
    ],
}

DISCOUNT_CODES = {
    "coffee": "SIMBA-COFFEE-2026",
    "onigiri": "SIMBA-ONIGIRI-2026",
    "sandwich": "SIMBA-SANDWICH-2026",
    "juice": "SIMBA-JUICE-2026",
}

def generate_adventure(user_id: str):
    prediction = predict_next_item(user_id)

    if not prediction:
        prediction = "coffee"

    templates = ADVENTURE_TEMPLATES.get(prediction, ADVENTURE_TEMPLATES["coffee"])
    story = random.choice(templates)
    code = DISCOUNT_CODES.get(prediction, "SIMBA711-2026")

    return {
        "item": prediction,
        "story": story,
        "call_to_action": f"Let's go grab some {prediction} at a 7-Eleven near you to discuss my adventure!",
        "discount_code": code,
        "discount_text": f"Show this code at checkout for 10% off your {prediction}!"
    }