import cv2

class CameraHandler:
    """ Handles webcam capture. """

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        """ Captures a frame from the webcam and returns it in RGB format. """
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def release(self):
        """ Releases the webcam. """
        self.cap.release()
