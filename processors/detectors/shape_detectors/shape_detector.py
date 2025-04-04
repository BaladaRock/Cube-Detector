import time

import cv2
from processors.detectors.shape_detectors.grid_helper import GridHelper
from processors.detectors.shape_detectors.tracking_helper import TrackingHelper

class ShapeDetector:
    def __init__(self):
        self.tracker = TrackingHelper()
        self.timer_count = 0  # Counter for debug printing

    def detect_squares(self, frame, mask):
        squares = self.tracker.find_squares(mask)

        # Keep only 9 squares closest to image center
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2

        def distance_to_center(square):
            x, y, sw, sh = square
            center_x, center_y = x + sw // 2, y + sh // 2
            return (center_x - cx) ** 2 + (center_y - cy) ** 2

        squares = sorted(squares, key=distance_to_center)[:9]

        # Try forming a grid
        grid = GridHelper.form_grid(squares)

        # Optional debug print every 50 frames
        now = time.time()
        if now - self.timer_count > 1:
            print(f"[DEBUG] Found {len(squares)} square(s)")
            if grid:
                print("[DEBUG] Grid formed successfully!")
            else:
                print("[DEBUG] Failed to form grid")
            self.timer_count = now

        # Draw grid if successful, otherwise fallback to drawing raw squares
        if grid:
            GridHelper.draw_grid(frame, grid)
        else:
            self.tracker.draw_shapes(frame, squares, tracking_lines=[])

        return frame, squares
