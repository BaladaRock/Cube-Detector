import cv2
import numpy as np
from calibration.hsv_ranges_loader import save_color_range

class HSVCalibrator:
    def __init__(self):
        self.frame_counter = 0

    def measure_and_save(self, frame, current_color):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2
        roi = hsv[cy - 5: cy + 6, cx - 5: cx + 6]

        h_mean = np.mean(roi[:, :, 0])
        s_mean = np.mean(roi[:, :, 1])
        v_mean = np.mean(roi[:, :, 2])

        print(f"[{current_color}] Saved HSV: H={h_mean:.1f}, S={s_mean:.1f}, V={v_mean:.1f}")
        save_color_range(current_color, (h_mean, s_mean, v_mean))
