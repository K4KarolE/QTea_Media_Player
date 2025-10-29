'''
Used to display the logo image
when the video area is not active:
- playing music
- player is in stopped state
'''

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from .class_data import cv
from .logger import logger_runtime

@logger_runtime
class MyImage(QLabel):
    def __init__(self, img_name, img_size):
        super().__init__()
        self.image = QPixmap(f'skins/{cv.skin_selected}/images/{img_name}').scaledToWidth(img_size, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(self.image)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)