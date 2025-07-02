import cv2
import numpy as np

from processors.detectors.shape_detectors.contour_tracker_detector import ContourBasedTracker
from processors.detectors.shape_detectors.grid_helper import GridHelper
from processors.detectors.shape_detectors.opticalflow_tracker_detector import OpticalFlowTracker
from processors.detectors.shape_detectors.tracking_helper import TrackingHelper
from calibration import hsv_ranges_loader
from communication.face_state_manager import update_face

class ShapeDetector:
    def __init__(self):
        self.contour_tracker = ContourBasedTracker()
        self.optical_flow_tracker = OpticalFlowTracker()

        # we will use the default order, for storing the faces configurations and sending them through the API
        self.scan_order = ['F', 'B', 'U', 'R', 'L', 'D']
        self.face_ptr = 0
        self.required_stable_frames = 5  # we'll use this to avoid storing faces to early in teh process
        self.grid_stable_frames = 0

        self.tracker = TrackingHelper()

    def detect_squares(self, frame, mask):
        # Switch between contour tracking and optical flow tracking

        # return self.contour_tracker.detect_squares(frame, mask)
        # return self.optical_flow_tracker.detect_squares(frame, mask)
        # squares = self.tracker.find_squares(mask)

        squares = self.tracker.find_squares(mask)

        # Keep only 9 squares closest to image center
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2

        def distance_to_center(square):
            x, y, sw, sh = square
            center_x, center_y = x + sw // 2, y + sh // 2
            return (center_x - cx) ** 2 + (center_y - cy) ** 2

        squares = sorted(squares, key=distance_to_center)[:9]

        # Try forming a grid
        grid = GridHelper.form_grid(squares)

        # once the grid has been formed, send the information to the 'communication' folder
        if grid is not None:
            self.grid_stable_frames += 1
        else:
            self.grid_stable_frames = 0

        if (self.grid_stable_frames >= self.required_stable_frames
                and self.face_ptr < len(self.scan_order)):
            face_id = self.scan_order[self.face_ptr]

            color_grid = self.grid_to_colors(frame, grid)
            update_face(face_id, color_grid)

            print(f"[INFO] Face {face_id} saved ⇢ {color_grid}")
            self.face_ptr += 1
            self.grid_stable_frames = 0

        # Draw grid if successful, otherwise fallback to drawing raw squares
        if grid:
            GridHelper.draw_grid(frame, grid)
        else:
            self.tracker.draw_shapes(frame, squares, tracking_lines=[])

        return frame, squares

    def classify_pixel(self, hsv_pixel):
        h, s, v = hsv_pixel
        ranges = hsv_ranges_loader.load_all_ranges()
        for name, r in ranges.items():
            lo = np.array(r.get("lower") or r.get("lower1"))
            up = np.array(r.get("upper") or r.get("upper1"))
            if (lo <= [h, s, v]).all() and ([h, s, v] <= up).all():
                return name
            if "lower2" in r and any(r["lower2"]):
                lo2, up2 = np.array(r["lower2"]), np.array(r["upper2"])
                if (lo2 <= [h, s, v]).all() and ([h, s, v] <= up2).all():
                    return name
        return "white"

    def grid_to_colors(self, frame_bgr, grid):
        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        colors = []
        for row in grid:
            row_colors = []
            for x, y, w, h in row:
                cx, cy = int(x + w / 2), int(y + h / 2)
                patch = hsv[cy - 2:cy + 3, cx - 2:cx + 3].reshape(-1, 3)
                mean_hsv = patch.mean(axis=0).astype(int)
                row_colors.append(self.classify_pixel(mean_hsv))
            colors.append(row_colors)
        return colors
