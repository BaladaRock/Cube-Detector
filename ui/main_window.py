import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

from processors.camera_processor import CameraHandler
from processors.detectors.color_detectors.color_detector import ColorDetector
from calibration.hsv_calibrator import HSVCalibrator
from ui.calibration_window import CalibrationWindow


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # Define the list of colors based on the cube's classic colors
        self.colors = ["red", "orange", "yellow", "green", "blue", "white"]

        self.video_label = None
        self.mask_label = None

        # Calibration-specific fields
        self.calibrator = HSVCalibrator()
        self.current_color = "red"
        self.color_selector = None
        self.save_button = None
        self.info_label = None

        self.init_ui()
        self.camera = CameraHandler()
        self.color_detector = ColorDetector()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        self.setWindowTitle("Cube Processor - Calibration Mode")

        self.video_label = QLabel(self)
        self.mask_label = QLabel(self)

        # Layout video + mask
        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_label)
        video_layout.addWidget(self.mask_label)

        # Open Calibration button
        self.calibration_button = QPushButton("Open Calibration Window")
        self.calibration_button.setFixedHeight(40)
        self.calibration_button.clicked.connect(self.open_calibration_window)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.calibration_button)
        main_layout.addLayout(video_layout)

        self.setLayout(main_layout)

    def update_frame(self):
        original_frame = self.camera.get_frame()
        if original_frame is None:
            # print("---Warning--- No frame received from camera.")
            return

        combined_mask = None
        frame_to_display = original_frame.copy()

        for color in self.colors:
            processed_frame, mask = self.color_detector.detect_color(original_frame, color=color)
            if isinstance(processed_frame, tuple):
                processed_frame, _ = processed_frame

            frame_to_display = processed_frame
            combined_mask = mask if combined_mask is None else cv2.bitwise_or(combined_mask, mask)

            # Convert processed frame to QImage
            h, w, ch = frame_to_display.shape
            bytes_per_line = ch * w
            processed_qimg = QImage(frame_to_display.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(processed_qimg))

            # Convert combined mask to grayscale QImage
            h_m, w_m = combined_mask.shape
            mask_qimg = QImage(combined_mask.data, w_m, h_m, combined_mask.strides[0], QImage.Format_Grayscale8)
            self.mask_label.setPixmap(QPixmap.fromImage(mask_qimg))
        else:
            # print("---Warning--- No frame received from camera!")
            return

    def set_current_color(self, color):
        self.current_color = color
        self.info_label.setText(f"Scan the {color.upper()} face")

    def save_current_color(self):
        frame = self.camera.get_frame()
        if frame is not None:
            self.calibrator.measure_and_save(frame, self.current_color)

    def open_calibration_window(self):
        self.calibration_window = CalibrationWindow(self.camera)
        self.calibration_window.show()

    def closeEvent(self, event):
        self.camera.release()
        event.accept()
