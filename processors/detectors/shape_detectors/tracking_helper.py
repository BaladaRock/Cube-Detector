import cv2

# Helper class to handle square detection and tracking history.
class TrackingHelper:

    def __init__(self):
        self.prev_squares = []  # Stores last detected squares

    def store_squares(self, squares):
        # Saves detected squares for tracking in the next frame.
        self.prev_squares = squares.copy()

    def draw_shapes(self, frame, squares, tracking_lines):
        # Draw detected squares
        for (x, y, w, h) in squares:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box
        # Draw tracking lines
        for (start, end) in tracking_lines:
            cv2.line(frame, start, end, (255, 0, 255), 2)  # Magenta tracking line

        return frame

    def find_squares(self, mask):
        # Detects squares inside a binary mask using contours.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        squares = []

        for cnt in contours:
            # Douglas - Peucker algorithm to detect the corners of a form
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)

            if len(approx) == 4:  # Looking for quadrilaterals
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                if 0.8 < aspect_ratio < 1.2:  # Nearly square
                    squares.append((x, y, w, h))

        return squares
