import os
import json
import cv2
import numpy as np

from processors.detectors.shape_detectors.shape_detector import ShapeDetector
from processors.detectors.color_detectors.color_ranges import ColorRanges


class ColorDetector:
    def __init__(self):
        self.shape_detector = ShapeDetector()
        self.frame_counter = 0
        self.json_path = os.path.join("calibration", "hsv_ranges.json")

    def detect_color(self, frame, color="red"):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        color_range = self.load_color_range(color)

        lower1 = np.array(color_range["lower1"])
        upper1 = np.array(color_range["upper1"])
        lower2 = np.array(color_range["lower2"])
        upper2 = np.array(color_range["upper2"])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

        result = self.shape_detector.detect_squares(frame, mask)
        if isinstance(result, tuple):
            frame_with_squares = result[0]
        else:
            frame_with_squares = result

        self.draw_center_rectangle(frame_with_squares)
        return frame_with_squares, mask

    def load_color_range(self, color):
        data = self.load_json_ranges()
        if color in data:
            hsv_data = data[color]
            # Validate structure
            if all(k in hsv_data for k in ("lower1", "upper1", "lower2", "upper2")):
                return hsv_data
            else:
                print(f"---Warning--- Malformed HSV data for '{color}' in JSON. Using fallback.")

        # fallback if the JSON is not in correct format at startup
        print(f"---Info--- '{color}' not found in JSON. Using default values from color_ranges.py")
        fallback = ColorRanges.get_range(color)
        if fallback is None:
            print(f"---Error--- No fallback HSV values found for '{color}'")
            return {
                "lower1": [0, 0, 0],
                "upper1": [0, 0, 0],
                "lower2": [0, 0, 0],
                "upper2": [0, 0, 0]
            }

        return fallback

    def load_json_ranges(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"---Warning--- Could not load JSON: {e}")
        return {}

    def draw_center_rectangle(self, frame):
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2
        size = 30
        cv2.rectangle(frame, (cx - size // 2, cy - size // 2), (cx + size // 2, cy + size // 2), (255, 0, 0), 2)
