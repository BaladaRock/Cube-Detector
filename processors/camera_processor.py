import cv2

class CameraHandler:
    # Handles webcam capture.

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    # Captures a frame from the webcam and returns it in RGB format.
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    # Releases the webcam.
    def release(self):
        self.cap.release()
