import json
import os


DATA_FILE = os.path.expanduser("~/.yacht_club.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"yachts": {}, "trips": [], "maintenance": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("yachts", {})
        data.setdefault("trips", [])
        data.setdefault("maintenance", [])
        return data
    except (json.JSONDecodeError, IOError):
        return {"yachts": {}, "trips": [], "maintenance": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
