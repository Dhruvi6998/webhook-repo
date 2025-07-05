from pymongo import MongoClient
from datetime import datetime
import pytz

# Set timezone to Indian Standard Time
IST = pytz.timezone('Asia/Kolkata')

# Connect to MongoDB (local server)
client = MongoClient("mongodb://localhost:27017")

# Create/use a database called webhookDB
db = client.webhookDB

# Create/use a collection called events
collection = db.events

# Function to save an event into MongoDB
def save_event(event_type, payload):
    data = {}  # this will hold the final data to be saved

    # Get current time in IST and format it nicely
    now_ist = datetime.now(IST)
    timestamp = now_ist.strftime('%d %B %Y - %I:%M %p IST')

    try:
        # If the event is a push (code push to a branch)
        if event_type == "push":
            data = {
                "type": "push",
                "author": payload['pusher']['name'],
                "to_branch": payload['ref'].split('/')[-1],  # extract branch name
                "timestamp": timestamp
            }

        # If the event is a pull request
        elif event_type == "pull_request":
            action = payload.get('action')  # e.g., opened, closed
            pr = payload.get('pull_request', {})  # pull request details
            merged = pr.get('merged', False)  # check if PR was merged

            # If PR was merged
            if action == "closed" and merged:
                data = {
                    "type": "merge",  # label it as a merge event
                    "author": pr['user']['login'],  # who created the PR
                    "from_branch": pr['head']['ref'],  # source branch
                    "to_branch": pr['base']['ref'],   # target branch
                    "timestamp": timestamp
                }
            else:
                # If PR was just opened or closed without merging
                data = {
                    "type": "pull_request",
                    "author": pr['user']['login'],
                    "from_branch": pr['head']['ref'],
                    "to_branch": pr['base']['ref'],
                    "timestamp": timestamp
                }

        # Insert the event data into the database only if it's filled
        if data:
            collection.insert_one(data)

    except Exception as e:
        print(f"[ERROR] Failed to save event: {e}")

# Function to get the 10 most recent events from MongoDB
def get_latest_events():
    return list(collection.find().sort("_id", -1).limit(10))
