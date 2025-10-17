import json
import os
import json
import os

DATA_FILE = os.path.join(os.getcwd(), "store.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "admin": [
                {"admin": "Babs", "pin": 3016}
            ],
            "user": []
        }
        save_data(default_data)
        return default_data

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {
                "admin": [
                {"admin": "Babs", "pin": 3016}
            ],
                "user": []
            }
            save_data(data)

    # ✅ Ensure correct structure even if file is edited manually
    if "admin" not in data or "user" not in data:
        data = {
            "admin":  [
                {"admin": "Babs", "pin": 3016}
            ],
            "user": []
        }
        save_data(data)

    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Saving data to: {DATA_FILE}")
