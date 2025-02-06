import sys

import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from processors.camera_processor import CameraHandler
from processors.image_processor import ImageProcessor


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.video_label = None
        self.processor = None
        self.initUI()
        self.camera = CameraHandler()
        self.processor = ImageProcessor()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # every 30 seconds

    def initUI(self):
        self.setWindowTitle("Camera Web")

        self.video_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

    def update_frame(self):
        # return the frame read from the camera, in RGB format
        frame = self.camera.get_frame()
        if frame is not None:
            processed_frame, mask = self.processor.process_frame(frame)  # Apply the image processing here
            h, w, ch = processed_frame.shape
            bytes_per_line = ch * w
            processed_img = QImage(processed_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(processed_img))

            # Convert the original frame
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Convert the mask
            mask_qimg = QImage(mask.data, mask.shape[1], mask.shape[0], mask.strides[0], QImage.Format_Grayscale8)

            # Display both the main and the mask window
            self.video_label.setPixmap(QPixmap.fromImage(qimg))
            cv2.imshow("Mask", mask)  # Mask
            cv2.waitKey(1)

    def closeEvent(self, event):
        self.camera.release()
        event.accept()