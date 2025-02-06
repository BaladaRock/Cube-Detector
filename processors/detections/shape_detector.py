import cv2

class ShapeDetector:
    """ Detects geometric shapes in a given mask. """

    def detect_squares(self, mask):
        """ Detects squares in the given binary mask. """
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
