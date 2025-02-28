from flask import Flask, request, redirect, url_for, jsonify, session, abort, send_from_directory
import sqlite3
import requests
from bs4 import BeautifulSoup
import os
import hashlib
import secrets
import logging
import time
import re
import threading
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
csrf = CSRFProtect(app)

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Secure Headers Middleware
def secure_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
app.after_request(secure_headers)

# Define paths
BASE_DIR = "United Conservative Party Lethbridge-West Website"
DB_PATH = os.path.join(BASE_DIR, "events.db")
EVENTS_HTML_PATH = os.path.join(BASE_DIR, "events.html")

# Database setup
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT NOT NULL,
                          description TEXT NOT NULL,
                          image TEXT NOT NULL,
                          link TEXT NOT NULL)''')
        conn.commit()

init_db()

# Scraping function (Modify based on target site structure)
def scrape_events():
    url = "https://example.com/events"  # Replace with the actual URL
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        logging.warning("Failed to fetch events, status code: %s", response.status_code)
        return "Failed to fetch events"
    
    soup = BeautifulSoup(response.text, "html.parser")
    events = []
    
    for event in soup.find_all("div", class_="event-class"):  # Adjust selector
        title = event.find("h2").text.strip()
        description = event.find("p").text.strip()
        image = event.find("img")["src"]
        link = event.find("a")["href"]
        
        events.append((title, description, image, link))
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO events (title, description, image, link) VALUES (?, ?, ?, ?)", events)
        conn.commit()
    
    return "Events scraped and stored successfully"

# Background job to check for new events periodically
def scheduled_scrape():
    while True:
        scrape_events()
        time.sleep(3600)  # Scrape every hour

# Start the background thread
def start_scraping_thread():
    thread = threading.Thread(target=scheduled_scrape, daemon=True)
    thread.start()

# API to fetch events
def get_events():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
    
    return jsonify(events)

# Dashboard route
@app.route("/")
def dashboard():
    return send_from_directory(BASE_DIR, "dashboard.html")

# Events Page Route
@app.route("/events")
def events_page():
    return send_from_directory(BASE_DIR, "events.html")

# Route to delete event
@app.route("/delete/<int:event_id>", methods=["POST"])
@csrf.exempt
def delete_event(event_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
    return redirect(url_for("dashboard"))

# Scrape events manually from dashboard
@app.route("/scrape", methods=["POST"])
@csrf.exempt
def manual_scrape():
    scrape_events()
    return redirect(url_for("dashboard"))

# Input Validation
def validate_input(data):
    if not isinstance(data, str):
        abort(400, "Invalid input")
    data = re.sub(r'[^a-zA-Z0-9 .,!?@#&()\-]', '', data)  # Allow only safe characters
    return data.replace("<", "&lt;").replace(">", "&gt;")

if __name__ == "__main__":
    start_scraping_thread()  # Start scheduled scraping in the background
    scrape_events()  # Initial scrape on startup
    app.run(debug=False, host="0.0.0.0", port=5000)
