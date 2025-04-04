import cv2
import json
import numpy as np
import os


class HSVCalibrator:
    def __init__(self, output_path=None):
        # Set default path in calibration folder
        if output_path is None:
            self.output_path = os.path.join(os.path.dirname(__file__), "hsv_ranges.json")
        else:
            self.output_path = output_path

    def measure_and_save(self, frame, color_name):
        avg_hsv = self._compute_average_hsv(frame)
        hsv_data = self._generate_hsv_range(avg_hsv, color_name)
        self._save_to_json(color_name, hsv_data)
        print(f"Calibrated {color_name.upper()}: {hsv_data}!")

    def _compute_average_hsv(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2
        roi_size = 30

        roi = hsv[cy - roi_size // 2:cy + roi_size // 2, cx - roi_size // 2:cx + roi_size // 2]
        avg_h = int(np.mean(roi[:, :, 0]))
        avg_s = int(np.mean(roi[:, :, 1]))
        avg_v = int(np.mean(roi[:, :, 2]))

        return avg_h, avg_s, avg_v

    def _generate_hsv_range(self, avg_hsv, color_name):
        h, s, v = avg_hsv
        offset_h = 10
        offset_s = 50
        offset_v = 50

        lower1 = [max(0, h - offset_h), max(0, s - offset_s), max(0, v - offset_v)]
        upper1 = [min(180, h + offset_h), min(255, s + offset_s), min(255, v + offset_v)]

        # For red, allow second range (not used for others yet)
        if color_name.lower() == "red":
            lower2 = [170, max(0, s - offset_s), max(0, v - offset_v)]
            upper2 = [180, min(255, s + offset_s), min(255, v + offset_v)]
        else:
            lower2 = [0, 0, 0]
            upper2 = [0, 0, 0]

        return {
            "lower1": lower1,
            "upper1": upper1,
            "lower2": lower2,
            "upper2": upper2
        }

    def _save_to_json(self, color_name, hsv_data):
        if os.path.exists(self.output_path):
            with open(self.output_path, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[color_name] = hsv_data

        with open(self.output_path, "w") as f:
            json.dump(data, f, indent=4)
