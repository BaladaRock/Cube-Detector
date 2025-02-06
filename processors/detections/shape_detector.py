import cv2
import numpy as np


class ShapeDetector:
    # Detects geometric shapes in a given mask and tracks movement.

    def __init__(self):
        self.prev_squares = []  # Stores last detected squares

    def detect_squares(self, frame, mask):
        # Detect squares from the mask
        squares = self.find_squares(mask)

        # Track movement by matching squares from the previous frame
        tracking_lines = self.match_squares(squares)

        # Draw the results on the frame
        frame_with_shapes = self.draw_squares_and_tracks(frame, squares, tracking_lines)

        # Save detected squares for the next frame
        self.prev_squares = squares.copy()

        return frame_with_shapes

    def find_squares(self, mask):
        # Finds squares inside the binary mask.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        squares = []

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)

            if len(approx) == 4:  # Looking for quadrilaterals
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                if 0.8 < aspect_ratio < 1.2:  # Nearly square
                    squares.append((x, y, w, h))

        return squares

    # Matches squares between frames to track movement.
    def match_squares(self, squares):
        tracking_lines = []

        if len(self.prev_squares) > 0:
            for (x, y, w, h) in squares:
                closest_match = min(
                    self.prev_squares,
                    key=lambda s: np.linalg.norm(np.array([x, y]) - np.array([s[0], s[1]])),
                    default=None
                )

                if closest_match:
                    tracking_lines.append(((x + w // 2, y + h // 2),
                                           (closest_match[0] + closest_match[2] // 2,
                                            closest_match[1] + closest_match[3] // 2)))

        return tracking_lines

    # we use this to draw the recognized shapes
    def draw_squares_and_tracks(self, frame, squares, tracking_lines):
        for (start, end) in tracking_lines:
            cv2.line(frame, start, end, (255, 0, 255), 2)  # Magenta line for tracking
        for (x, y, w, h) in squares:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box

        return frame
