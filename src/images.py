from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

class MyImage(QLabel):
    def __init__(self, img_name, img_size):
        super().__init__()
        
        self.image = QPixmap(f'skins/{img_name}').scaledToWidth(img_size, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(self.image)
        self.resize(self.image.width(), self.image.height())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)