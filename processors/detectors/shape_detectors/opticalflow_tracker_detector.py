import cv2
import numpy as np

from processors.detectors.shape_detectors.tracking_helper import TrackingHelper


class OpticalFlowTracker:
    # Uses Lucas-Kanade Optical Flow to track squares in motion.

    def __init__(self):
        self.prev_gray = None  # Stores previous frame in grayscale
        self.tracking_helper = TrackingHelper()

    def detect_squares(self, frame, mask):
        # Convert frame to grayscale for Optical Flow
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect squares using TrackingHelper
        squares = self.tracking_helper.find_squares(mask)

        # Track movement using Optical Flow
        tracking_lines = []
        if self.prev_gray is not None and len(self.tracking_helper.prev_squares) > 0:
            tracking_lines = self.track_squares(gray, squares)

        # Store detected squares for next frame
        self.tracking_helper.store_squares(squares)
        self.prev_gray = gray  # Save the previous grayscale frame

        frame = self.tracking_helper.draw_shapes(frame, squares, tracking_lines)

        return frame, squares

    def track_squares(self, gray, squares):
        # Uses Optical Flow (Lucas-Kanade) to track squares between frames.
        tracking_lines = []

        if len(self.tracking_helper.prev_squares) == 0:
            return tracking_lines  # No previous data to track

        # Convert previous square centers to points
        prev_pts = np.float32([[x + w // 2, y + h // 2] for x, y, w, h in self.tracking_helper.prev_squares]).reshape(-1, 1, 2)

        # Calculate Optical Flow
        next_pts, status, _ = cv2.calcOpticalFlowPyrLK(self.prev_gray, gray, prev_pts, None)

        # Draw tracking lines if Optical Flow finds a match
        for i, (new, old) in enumerate(zip(next_pts, prev_pts)):
            if status[i]:  # If Optical Flow successfully tracked the point
                new_x, new_y = new.ravel()
                old_x, old_y = old.ravel()
                tracking_lines.append(((int(old_x), int(old_y)), (int(new_x), int(new_y))))

        return tracking_lines
