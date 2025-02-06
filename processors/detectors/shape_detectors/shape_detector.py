from processors.detectors.shape_detectors.contour_tracker_detector import ContourBasedTracker
from processors.detectors.shape_detectors.opticalflow_tracker_detector import OpticalFlowTracker

class ShapeDetector:
    # Manages both Contour Tracking and Optical Flow Tracking.

    def __init__(self):
        self.contour_tracker = ContourBasedTracker()
        self.optical_flow_tracker = OpticalFlowTracker()

    def detect_squares(self, frame, mask):
        # Switch between contour tracking and optical flow tracking
        # return self.contour_tracker.detect_squares(frame, mask)
        return self.optical_flow_tracker.detect_squares(frame, mask)
