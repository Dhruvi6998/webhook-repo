from pymongo import MongoClient
from datetime import datetime
import pytz

# Timezone for India
IST = pytz.timezone('Asia/Kolkata')

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.webhookDB
collection = db.events

def save_event(event_type, payload):
    data = {}

    # Get current IST time
    now_ist = datetime.now(IST)
    timestamp = now_ist.strftime('%d %B %Y - %I:%M %p IST')

    try:
        if event_type == "push":
            data = {
                "type": "push",
                "author": payload['pusher']['name'],
                "to_branch": payload['ref'].split('/')[-1],
                "timestamp": timestamp
            }

        elif event_type == "pull_request":
            action = payload.get('action')
            pr = payload.get('pull_request', {})
            merged = pr.get('merged', False)

            if action == "closed" and merged:
                data = {
                    "type": "merge",
                    "author": pr['user']['login'],
                    "from_branch": pr['head']['ref'],
                    "to_branch": pr['base']['ref'],
                    "timestamp": timestamp
                }
            else:
                data = {
                    "type": "pull_request",
                    "author": pr['user']['login'],
                    "from_branch": pr['head']['ref'],
                    "to_branch": pr['base']['ref'],
                    "timestamp": timestamp
                }

        if data:
            collection.insert_one(data)

    except Exception as e:
        print(f"[ERROR] Failed to save event: {e}")

def get_latest_events():
    return list(collection.find().sort("_id", -1).limit(10))

