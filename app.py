from flask import Flask, request, jsonify, render_template
from models import save_event, get_latest_events  # Import the functions from your models.py

# Initialize the Flask app
app = Flask(__name__)

# Route for the homepage (renders the HTML UI)
@app.route('/')
def index():
    return render_template('index.html')  # This file should be inside the 'templates' folder

# Webhook endpoint that GitHub will POST to when an event occurs
@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')  # Get the event type from the header
    payload = request.json  # Get the JSON data (actual event details)
    save_event(event_type, payload)  # Save it to MongoDB using your custom function
    return '', 204  # Respond with 204 No Content (GitHub expects a response)

# API endpoint to return the latest 10 events as JSON
@app.route('/events', methods=['GET'])
def events():
    events = get_latest_events()  # Get latest events from MongoDB
    for event in events:
        del event['_id']  # Remove the MongoDB object ID (not needed in frontend)
    return jsonify(events)  # Send data to frontend

# Run the Flask app on port 5000 in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000)
