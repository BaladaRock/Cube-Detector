import cv2

class ShapeDetector:
    # Detects geometric shapes in a given mask.

    def detect_squares(self, frame, mask):
        # Finds squares inside a binary mask and draws them on the original frame.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        squares = []

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)

            if len(approx) == 4:  # Looking for quadrilaterals
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                if 0.8 < aspect_ratio < 1.2:  # Nearly square
                    squares.append((x, y, w, h))

        # Draw detected squares on the frame
        for (x, y, w, h) in squares:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box

        return frame
