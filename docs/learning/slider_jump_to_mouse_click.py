'''
Slider jumps to the position of the mouse click 

Cheers mate!
https://python-forum.io/thread-10564.html
'''

from PyQt6.QtWidgets import QSlider, QApplication, QMainWindow, QStyle
from PyQt6.QtCore import Qt

import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.resize(400, 350)
window.setWindowTitle('Jumpy Slider')


class QJumpSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
     
    def mousePressEvent(self, event):
        # JUMP TO CLICK POSITION
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        slider2.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
     
    def mouseMoveEvent(self, event):
        # JUMP TO POINTER POSITION WHILE MOVING
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        slider2.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))


# SLIDER IN CONTROL
slider = QJumpSlider(window)
slider.move(50,50)
slider.resize(300, 100)
slider.setOrientation(Qt.Orientation.Horizontal)

# TARGET SLIDER/WIDGET
slider2 = QSlider(window)
slider2.move(50,200)
slider2.resize(300,100)
slider2.setOrientation(Qt.Orientation.Horizontal)

window.show()

sys.exit(app.exec())