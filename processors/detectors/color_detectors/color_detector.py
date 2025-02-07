import cv2
import numpy as np
from processors.detectors.color_detectors.color_ranges import ColorRanges
from processors.detectors.shape_detectors.shape_detector import ShapeDetector


class ColorDetector:
    # Handles color detection using HSV filtering.

    def __init__(self):
        self.shape_detector = ShapeDetector()
        self.frame_counter = 0  # Counter variable used to control print frequency

    def detect_color(self, frame, color="red"):
        # Detects the given color and returns the mask.
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        color_range = ColorRanges.get_range(color)
        if not color_range:
            return frame, np.zeros(frame.shape[:2], dtype=np.uint8)

        lower1 = np.array(color_range["lower1"])
        upper1 = np.array(color_range["upper1"])
        lower2 = np.array(color_range["lower2"])
        upper2 = np.array(color_range["upper2"])

        # Apply the masks
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Send mask to ShapeDetector
        frame_with_squares = self.shape_detector.detect_squares(frame, mask)

        # Draw measurement rectangle
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2
        roi_size = 50
        cv2.rectangle(frame, (center_x - roi_size // 2, center_y - roi_size // 2),
                      (center_x + roi_size // 2, center_y + roi_size // 2), (255, 0, 0), 2)

        # Print HSV values every 10 frames
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            roi = hsv[center_y - roi_size // 2:center_y + roi_size // 2 + 1,
                      center_x - roi_size // 2:center_x + roi_size // 2 + 1]

            avg_hue = np.mean(roi[:, :, 0])
            avg_saturation = np.mean(roi[:, :, 1])
            avg_value = np.mean(roi[:, :, 2])

            print(f"HSV Center Avg: H={avg_hue:.1f}, S={avg_saturation:.1f}, V={avg_value:.1f}")

        return frame_with_squares, mask
