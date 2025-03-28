"""
Cheers!
https://www.geeksforgeeks.org/prevent-freezing-in-python-pyqt-guis-with-qthread/
"""

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import time

QApplication.setDesktopSettingsAware(False) # avoid OS auto coloring


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w_width = 400
        self.w_height = 400
        self.resize(self.w_width, self.w_height)
        self.setWindowTitle('Learning Threading')
        self.thread = MyThread()
        self.thread.result_ready.connect(self.new_pos_ready)

    def new_pos_ready(self, pos_x):
        pm_button.move(pos_x , pm_button.pos().y())
        # button(s) will not move when the below is enabled
        # box_layout.addWidget(QLabel("Test"))
        # box_layout.addWidget(QLabel("Test 2nd"))


class MyThread(QThread):
    result_ready = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        """ Can not update widgets in this function """
        pos_x = pm_button.pos().x()
        for i in range(1, 200):
            pos_x += 2
            pos_x = pos_x % (window.w_width - pm_button.width())
            self.result_ready.emit(pos_x)
            print(i)
            time.sleep(0.1)
            # box_layout.addWidget(QPushButton("Test")) # will drop an error



class MyButton(QPushButton):
    def __init__(self, title):
        super().__init__()
        self.setText(title)

    def mouseDoubleClickEvent(self, a0):
        window.thread.start()


app = MyApp()
window = MyWindow()

box_layout = QVBoxLayout(window)
box_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

button_w, button_h = 70, 50

tr_button = MyButton("Trigger")
box_layout.addWidget(tr_button)
tr_button.setFixedSize(button_w, button_h)

pm_button = QPushButton("Moving")
box_layout.addWidget(pm_button)
pm_button.setFixedSize(button_w, button_h)

window.show()
sys.exit(app.exec())