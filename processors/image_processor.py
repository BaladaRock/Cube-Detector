import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.frame_counter = 0 # Counter used to print the values every n frames

    def process_frame(self, frame):
        # store the corresponding hsv values for each color:

        # red:    H:11-13; S:145-152; V: 193-195
        # orange: H:176-178; S:111-119; V: 156-161

        # Print the point in the middle of the frame
        self.frame_counter += 1
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        if self.frame_counter % 10 == 0:
            h, w, _ = frame.shape
            center_pixel = hsv[h // 2, w // 2]
            print(f"HSV Center Pixel: {center_pixel}")

        # Adjust intervals for red colour
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        return result, mask