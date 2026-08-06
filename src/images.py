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
    def __init__(self):
        super().__init__()
        self.image = self.get_image()
        self.setPixmap(self.image)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_image(self):
        img_path = f'skins/{cv.skin_logo_path_list[0]}/images/{cv.skin_logo_path_list[1]}'
        if Path(img_path).is_file():
            return QPixmap(img_path).scaledToWidth(int(cv.skin_logo_img_size), Qt.TransformationMode.SmoothTransformation)
        else:
            default_img_path = 'skins/default/images/logo.png'
            return QPixmap(default_img_path).scaledToWidth(int(cv.skin_logo_img_size), Qt.TransformationMode.SmoothTransformation)


class MySkinsTabImage(QLabel):
    """ Used in the Settings Window / Skins tab """
    def __init__(self, img_file_path):
        super().__init__()
        self.generate_image(img_file_path)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def generate_image(self, img_file_path):
        if Path(img_file_path).is_file():
            img_ready = QPixmap(img_file_path).scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        else:
            default_img_path = 'skins/default/images/logo.png'
            img_ready = QPixmap(default_img_path).scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(img_ready)