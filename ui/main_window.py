import sys

import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from processors.camera_processor import CameraHandler
from processors.image_processor import ImageProcessor


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.mask_label = None
        self.video_label = None
        self.processor = None
        self.init_ui()
        self.camera = CameraHandler()
        self.processor = ImageProcessor()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # every 30 seconds

    def init_ui(self):
        self.setWindowTitle("Camera Web")

        self.video_label = QLabel(self)
        self.mask_label = QLabel(self)

        # Set default empty images to avoid NoneType errors
        self.video_label.setPixmap(QPixmap())
        self.mask_label.setPixmap(QPixmap())

        layout = QHBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.mask_label)
        self.setLayout(layout)

    def update_frame(self):
        frame = self.camera.get_frame()
        if frame is not None:
            processed_frame, mask = self.processor.process_frame(frame)

            # Convert the ORIGINAL frame (normal colors)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            original_qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(original_qimg))

            # Convert mask to grayscale for display
            h_m, w_m = mask.shape
            mask_qimg = QImage(mask.data, w_m, h_m, mask.strides[0], QImage.Format_Grayscale8)
            self.mask_label.setPixmap(QPixmap.fromImage(mask_qimg))

    def closeEvent(self, event):
        self.camera.release()
        event.accept()