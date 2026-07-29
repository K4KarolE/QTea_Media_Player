"""
Used to display the logo image
when the video area is not active:
- playing music
- player is in stopped state
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from .class_data import cv
from .logger import logger_runtime

@logger_runtime
class MyImage(QLabel):
    def __init__(self, img_size):
        super().__init__()
        self.img_size = img_size
        self.image = self.get_image()
        self.setPixmap(self.image)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_image(self):
        img_path = f'skins/{cv.skin_dir}/images/logo.png'
        if Path(img_path).is_file():
            return QPixmap(img_path).scaledToWidth(self.img_size, Qt.TransformationMode.SmoothTransformation)
        else:
            default_img_path = 'skins/default/images/logo.png'
            return QPixmap(default_img_path).scaledToWidth(self.img_size, Qt.TransformationMode.SmoothTransformation)