''' Learning how to mix static and dynamic layouts/widgets '''

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton
    )
from PyQt6.QtCore import Qt

import sys


''' APP '''
class MyApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
   
app = MyApp()


''' WINDOW '''
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500
window = QWidget()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
# window.setMinimumSize(400, 400)
window.setWindowTitle("Layout test")


''' 1 '''
# verty = QHBoxLayout(window)
# verty.addWidget(QPushButton('TTTT'))
# verty.addWidget(QPushButton('PPPP'))

''' 2 '''
# verty = QHBoxLayout(window)

# verty_left = QFrame()
# t = QPushButton('TTTT', verty_left)
# q = QPushButton('QQQQ', verty_left)
# q.move(100,0)


# verty.addWidget(verty_left)
# verty.addWidget(QPushButton('PPPP'))


''' 3 '''
# verty = QHBoxLayout(window)

# verty_left = QFrame()
# t = QPushButton('TTTT', verty_left)
# q = QPushButton('QQQQ', verty_left)
# q.move(100,0)

# verty_right = QFrame()
# t = QPushButton('AAAA', verty_right)
# q = QPushButton('BBBB', verty_right)
# q.move(100,0)


# verty.addWidget(verty_left, 50)
# verty.addWidget(verty_right, 50)


''' 3 '''
# verty = QHBoxLayout(window)

# verty_left = QVBoxLayout()
# verty_right = QVBoxLayout()
# # verty_right.setAlignment(Qt.AlignmentFlag.AlignRight)

# verty.addLayout(verty_left)
# verty.addLayout(verty_right)

# # LEFT WIDGETS
# t = QPushButton('TTTT')
# q = QPushButton('QQQQ')
# verty_left.addWidget(t)
# verty_left.addWidget(q)


# # RIGHT WIDGETS
# verty_right_qframe = QFrame()
# a = QPushButton('AAAA', verty_right_qframe)
# b = QPushButton('BBBB')
# verty_right.addWidget(b, 50)
# verty_right.addWidget(verty_right_qframe, 20)


''' 4 '''
# verty = QHBoxLayout(window)

# verty_left = QVBoxLayout()
# verty_right = QVBoxLayout()
# # verty_right.setAlignment(Qt.AlignmentFlag.AlignRight)

# verty.addLayout(verty_left)
# verty.addLayout(verty_right)

# # LEFT WIDGETS
# t = QPushButton('TTTT')
# q = QPushButton('QQQQ')
# verty_left.addWidget(t)
# verty_left.addWidget(q)


# # RIGHT WIDGETS
# verty_right_qframe = QFrame()
# verty_right_layout = QHBoxLayout()
# verty_right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
# verty_right_qframe.setLayout(verty_right_layout)

# a = QPushButton('AAAA')
# c = QPushButton('CCCC')
# verty_right_layout.addWidget(a)
# verty_right_layout.addWidget(c)

# b = QPushButton('BBBB')
# verty_right.addWidget(b, 20)
# verty_right.addWidget(verty_right_qframe , 80)


''' 5 '''
verty = QHBoxLayout(window)

verty_left = QVBoxLayout()
verty_right = QHBoxLayout()
verty_right.setAlignment(Qt.AlignmentFlag.AlignRight)

verty.addLayout(verty_left)
verty.addLayout(verty_right)

a = QPushButton('AAAA')
a.setFixedSize(70,25)

b = QPushButton('BBBB')
b.setFixedSize(70,25)

verty_left.addWidget(a)
verty_right.addWidget(b)


window.show()

sys.exit(app.exec())