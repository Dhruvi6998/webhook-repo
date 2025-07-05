from flask import Flask, request, jsonify, render_template
from models import save_event, get_latest_events

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    save_event(event_type, payload)
    return '', 204

@app.route('/events', methods=['GET'])
def events():
    events = get_latest_events()
    for event in events:
        del event['_id']  # Remove MongoDB ID
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
