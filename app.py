"""
Live NSE/BSE Stock Market Website
----------------------------------
Backend: Flask + Flask-SocketIO
Data source: Dhan API (broker API)
Live updates: pushed to browser every few seconds via WebSocket

HOW TO RUN LOCALLY (for testing before hosting):
1. Install Python 3.10+ from python.org
2. Open terminal / cmd in this folder
3. Run:  pip install -r requirements.txt
4. Set your Dhan API credentials below (or as environment variables)
5. Run:  python app.py
6. Open browser at http://localhost:5000

HOW TO HOST PUBLICLY (so anyone can visit the site):
See README.md in this folder - step by step Render.com deployment guide.
"""

import eventlet
eventlet.monkey_patch()

import os
import time
import threading
import requests
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------------------------------------------------
# DHAN API CONFIG - put your credentials here
# (Better: set these as environment variables when hosting,
#  don't upload your real keys to a public GitHub repo)
# ---------------------------------------------------------
DHAN_CLIENT_ID = os.environ.get("DHAN_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
DHAN_ACCESS_TOKEN = os.environ.get("DHAN_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
DHAN_BASE_URL = "https://api.dhan.co/v2"

# Symbols to track - edit this list with the stocks you want to show
# securityId is Dhan's internal ID for each symbol (from their master CSV)
WATCHLIST = [
    {"symbol": "RELIANCE", "securityId": "2885", "exchangeSegment": "NSE_EQ"},
    {"symbol": "TCS", "securityId": "11536", "exchangeSegment": "NSE_EQ"},
    {"symbol": "HDFCBANK", "securityId": "1333", "exchangeSegment": "NSE_EQ"},
    {"symbol": "INFY", "securityId": "1594", "exchangeSegment": "NSE_EQ"},
    {"symbol": "SBIN", "securityId": "3045", "exchangeSegment": "NSE_EQ"},
]

REFRESH_SECONDS = 3  # how often to pull fresh data and push to browser


def fetch_live_quotes():
    """
    Calls Dhan's Market Quote API for all symbols in WATCHLIST.
    Returns a list of dicts with symbol, ltp (last traded price), change, pChange, volume.
    """
    headers = {
        "access-token": DHAN_ACCESS_TOKEN,
        "client-id": DHAN_CLIENT_ID,
        "Content-Type": "application/json",
    }

    # Group security IDs by exchange segment (Dhan's quote API expects this format)
    payload = {}
    for item in WATCHLIST:
        seg = item["exchangeSegment"]
        payload.setdefault(seg, []).append(int(item["securityId"]))

    try:
        resp = requests.post(
            f"{DHAN_BASE_URL}/marketfeed/quote",
            json=payload,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})
    except Exception as e:
        print("Error fetching Dhan data:", e)
        return []

    results = []
    for item in WATCHLIST:
        seg = item["exchangeSegment"]
        sec_id = item["securityId"]
        quote = data.get(seg, {}).get(sec_id, {})
        if not quote:
            continue
        ltp = quote.get("last_price", 0)
        prev_close = quote.get("close", ltp) or ltp
        change = round(ltp - prev_close, 2) if prev_close else 0
        p_change = round((change / prev_close) * 100, 2) if prev_close else 0
        results.append(
            {
                "symbol": item["symbol"],
                "ltp": ltp,
                "change": change,
                "pChange": p_change,
                "volume": quote.get("volume", 0),
            }
        )
    return results


def background_price_updater():
    """Runs forever in a background thread, pushes fresh prices every REFRESH_SECONDS."""
    while True:
        quotes = fetch_live_quotes()
        if quotes:
            socketio.emit("price_update", quotes)
        time.sleep(REFRESH_SECONDS)


@app.route("/")
def index():
    return render_template("index.html", watchlist=WATCHLIST)


@socketio.on("connect")
def handle_connect():
    print("Client connected")


# Start the background price updater as soon as the module loads,
# so it works both with "python app.py" AND with gunicorn (Render).
updater_thread = threading.Thread(target=background_price_updater, daemon=True)
updater_thread.start()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
