import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.frame_counter = 0 # Counter used to print the values every n frames

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        # hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        # Red color range based on measured values
        lower_red1 = np.array([170, 120, 70])  # Lower boundary for red
        upper_red1 = np.array([180, 255, 255])

        lower_red2 = np.array([0, 120, 70])  # Covering wrap-around reds
        upper_red2 = np.array([10, 255, 255])

        # # Orange color range based on measured values (to be excluded)
        # lower_orange = np.array([4, 120, 100])
        # upper_orange = np.array([10, 255, 255])

        # Create red mask
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # # Create orange mask (to subtract)
        # mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        #
        # # Final mask: Keep red, remove orange
        # mask = cv2.bitwise_and(mask_red, cv2.bitwise_not(mask_orange))

        # Apply mask
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Draw a blue rectangle in the center for HSV measurement
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2
        roi_size = 10  # Slightly larger area for better visibility

        # Draw on the original frame so it shows in the main window
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

        return frame, mask  # Return normal frame + red mask



