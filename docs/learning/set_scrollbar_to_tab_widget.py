
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QScrollArea,
    QScrollBar,
    QTabWidget
    )

import sys

''' APP '''
app = QApplication(sys.argv)


'''
MAIN WINDOW <-- TAB WIDGET <-- QSCROLLAREA WINDOW <-- QWIDGET WINDOW <-- QWIDGETS
'''
WINDOW_WIDTH, WINDOW_HEIGHT = 220, 400
window_main = QWidget()
window_scrollarea = QScrollArea()
window_widgets = QWidget()
tab_widget = QTabWidget()


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
                                    "height: 0px;"  # -> not visible
                                    "}"
                                )

window_scrollarea.setVerticalScrollBar(scroll_bar_ver)
window_scrollarea.setHorizontalScrollBar(scroll_bar_hor)


''' QWIDGET WINDOW <-- QWIDGETS '''
counter = 0
counter_max = 30
while counter != counter_max:
    text = QLabel(f'{counter} - RANDOM TEXT', window_widgets)
    text.move(50, 20 + counter*30)
    counter += 1
window_widgets.resize(WINDOW_WIDTH, (counter_max + 1)*30)


''' QSCROLLAREA WINDOW <-- QWIDGET WINDOW '''
window_scrollarea.setWidget(window_widgets)


''' TAB WIDGET <-- QSCROLLAREA WINDOW '''
tab_widget.addTab(window_scrollarea, 'Test - 1')
tab_widget.addTab(QWidget(), 'Test - 2 - Empty tab') # JUST FOR TO BE A 2ND TAB
tab_widget.setGeometry(20, 20, WINDOW_WIDTH, WINDOW_HEIGHT)


''' MAIN WINDOW <-- TAB WIDGET '''
tab_widget.setParent(window_main)

window_main.show()

sys.exit(app.exec())