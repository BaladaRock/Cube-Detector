from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from calibration.hsv_calibrator import HSVCalibrator

class CalibrationWindow(QWidget):
    def __init__(self, camera):
        super().__init__()

        self.setFixedSize(300, 200)
        with open("ui/styles/main_style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle("Colors Calibration")
        self.calibrator = HSVCalibrator()
        self.camera = camera
        self.current_color = "red"

        self.color_selector = QComboBox()
        self.color_selector.addItems(["red", "orange", "yellow", "green", "blue", "white"])
        self.color_selector.currentTextChanged.connect(self.set_current_color)

        self.save_button = QPushButton("Save Color")
        self.save_button.clicked.connect(self.save_current_color)

        self.info_label = QLabel("Scan the RED face")

        layout = QVBoxLayout()
        layout.addWidget(self.color_selector)
        layout.addWidget(self.save_button)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def set_current_color(self, color):
        self.current_color = color
        self.info_label.setText(f"Scan the {color.upper()} face")

    def save_current_color(self):
        frame = self.camera.get_frame()
        if frame is not None:
            self.calibrator.measure_and_save(frame, self.current_color)
