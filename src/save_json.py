import json
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_json(data, filename):
    path = DATA_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    path = DATA_DIR / filename
    with open(path, "r") as f:
        return json.load(f)