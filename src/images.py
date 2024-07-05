from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from .class_data import cv


class MyImage(QLabel):
    def __init__(self, img_name, img_size):
        super().__init__()
        self.image = QPixmap(f'skins/{cv.skin_selected}/images/{img_name}').scaledToWidth(img_size, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(self.image)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)