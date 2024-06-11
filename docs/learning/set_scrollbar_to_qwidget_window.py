
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QScrollArea,
    QScrollBar
    )

import sys

''' APP '''
app = QApplication(sys.argv)


'''
QSCROLLAREA WINDOW <-- QWIDGET WINDOW <-- QWIDGETS
'''
WINDOW_WIDTH, WINDOW_HEIGHT = 220, 400
window_main = QScrollArea()
window_widgets = QWidget()

''' SCROLL BARS '''
scroll_bar_ver = QScrollBar()
scroll_bar_ver.setStyleSheet(
                                "QScrollBar::vertical"
                                    "{"
                                    "width: 10px;"
                                    "}"
                                )

scroll_bar_hor = QScrollBar()
scroll_bar_hor.setStyleSheet(
                                "QScrollBar::horizontal"
                                    "{"
                                    "height: 0px;"
                                    "}"
                                )

window_main.setVerticalScrollBar(scroll_bar_ver)
window_main.setHorizontalScrollBar(scroll_bar_hor)

''' WIDGETS '''
counter = 0
counter_max = 30
while counter != counter_max:
    text = QLabel(f'{counter} - RANDOM TEXT', window_widgets)
    text.move(50, 20 + counter*30)
    counter += 1

'''
LEARNED
The scrollbars visibility depends on the window_widgets window size,
not on the widgets amount the window_widgets window contains
- window_widgets.resize(WINDOW_WIDTH-20, (counter_max + 1)*30)
  - WINDOW_WIDTH - 20 --> the horizontal scrollbar invisible
  - or as above set a 0px horizontal scrollbar --> scrollbar invisible
  - (counter_max + 1)*30 --> makes the vertical scrollbar dependent
    on the widgets amount
'''
window_main.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
window_widgets.resize(WINDOW_WIDTH, (counter_max + 1)*30)


window_main.setWidget(window_widgets)

window_main.show()

sys.exit(app.exec())