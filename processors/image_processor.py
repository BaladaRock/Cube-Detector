import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        pass

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # We should define here the colour interval in order to process the cube
        lower_bound = np.array([0, 120, 70])  # red
        upper_bound = np.array([10, 255, 255])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

        return result