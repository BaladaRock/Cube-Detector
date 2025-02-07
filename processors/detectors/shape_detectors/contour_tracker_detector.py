import numpy as np

from processors.detectors.shape_detectors.tracking_helper import TrackingHelper


class ContourBasedTracker:
    # Uses contours to detect squares and track movement.

    def __init__(self):
        self.tracking_helper = TrackingHelper()

    def detect_squares(self, frame, mask):
        # Finds squares inside the binary mask using TrackingHelper.
        squares = self.tracking_helper.find_squares(mask)

        # Track movement using previous frame data
        tracking_lines = []
        if len(self.tracking_helper.prev_squares) > 0:
            for (x, y, w, h) in squares:
                best_match = None
                min_distance = float("inf")

                # Euclidian distance
                for prev_x, prev_y, prev_w, prev_h in self.tracking_helper.prev_squares:
                    distance = np.linalg.norm(np.array([x, y]) - np.array([prev_x, prev_y]))
                    if distance < min_distance:
                        min_distance = distance
                        best_match = (prev_x, prev_y, prev_w, prev_h)

                if best_match:
                    tracking_lines.append(((x + w // 2, y + h // 2),
                                           (best_match[0] + best_match[2] // 2,
                                            best_match[1] + best_match[3] // 2)))

        # Store detected squares for next frame
        self.tracking_helper.store_squares(squares)

        # Draw detected shapes
        frame = self.tracking_helper.draw_shapes(frame, squares, tracking_lines)

        return frame, squares
