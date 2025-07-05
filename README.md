# webhook-repo
This project shows GitHub activities like push, pull request, and merge on a webpage.
It uses:

Python (Flask) – to receive events

 MongoDB – to store the events

 HTML – to show events in your browser

Files in This Project
1. app.py
This is the main file.

It starts the server.

It receives GitHub events (like push or pull request).

It sends saved events to the webpage.

2. models.py
This file saves GitHub events to MongoDB.

It also gets the latest 10 events to show on the page.

It shows the current time in Indian time (IST).

3. templates/index.html
This is the webpage.

It shows recent events (push, pull request, merge).

It updates every 15 seconds.

Event type like "PUSH" or "MERGE" is shown in red color.

What It Does
You connect a GitHub webhook to this app.

When you push or create a pull request, GitHub sends data to this app.

The app saves the event in MongoDB.

The webpage shows what happened.

How to Run
Start MongoDB
(open terminal and type: mongod)

Run the Flask app

python app.py
Open your browser and go to:

http://localhost:5000
In your GitHub repo:

Go to Settings > Webhooks

Add a new webhook:

Payload URL: http://your-ip:5000/webhook

Content type: application/json

Select events: Push, Pull request, etc.
