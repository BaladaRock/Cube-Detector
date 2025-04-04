import json
import os

RANGES_FILE = "calibration/hsv_ranges.json"

def save_color_range(color_name, hsv_mean, delta=20):
    h, s, v = hsv_mean
    lower = [max(0, h - delta), max(0, s - delta), max(0, v - delta)]
    upper = [min(180, h + delta), min(255, s + delta), min(255, v + delta)]

    data = load_all_ranges()
    data[color_name] = {"lower": lower, "upper": upper}

    with open(RANGES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_all_ranges():
    if not os.path.exists(RANGES_FILE):
        return {}
    with open(RANGES_FILE, "r") as f:
        return json.load(f)

def get_range(color_name):
    data = load_all_ranges()
    return data.get(color_name)
