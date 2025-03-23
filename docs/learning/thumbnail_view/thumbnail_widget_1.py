"""
Cheers all!
Widget bg color: https://stackoverflow.com/q/12655538
"""

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
import sys

QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)


class ThumbnailWidget(QWidget):
    def __init__(self, widget_bg_color):
        super().__init__()
        self.setFixedSize(100,100)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color:{widget_bg_color};")

    def mousePressEvent(self, a0):
        print("Clicked")
        self.setStyleSheet(f"background-color: pink;")

    def mouseDoubleClickEvent(self, a0):
        print("Double clicked")


app = MyApp()
window = QWidget()
window.resize(400, 400)
window.setWindowTitle('Thumbnail')

test_widget1 = ThumbnailWidget("blue")
test_widget2 = ThumbnailWidget("red")
test_widget3 = ThumbnailWidget("orange")

box_layout = QHBoxLayout(window)
box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

box_layout.addWidget(test_widget1)
box_layout.addWidget(test_widget2)
box_layout.addWidget(test_widget3)

window.show()
sys.exit(app.exec())