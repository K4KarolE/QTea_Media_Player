"""
    It is a modified "learning / set_scrollbar_to_tab_widget.py" to understand how can
    we place an empty tab in the QTabWidget and fill it later

    It looks like the widget inside a tab is not accessible via the tab_widget (QTabWidget())
    Solution: add a shell of a QWidget (in this case: window_scroll_area_2nd_tab = QScrollArea())
    for the 2nd tab and modify it later
"""

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QWidget,
)

import sys

''' APP '''
app = QApplication(sys.argv)


'''
MAIN WINDOW <-- TAB WIDGET <-- QSCROLLAREA WINDOW <-- QWIDGET WINDOW <-- QWIDGETS
'''
WINDOW_WIDTH, WINDOW_HEIGHT = 220, 400
window_main = QWidget()
window_scroll_area_1st_tab = QScrollArea()
window_scroll_area_2nd_tab = QScrollArea()
window_widgets = QWidget()
tab_widget = QTabWidget()


''' QWIDGET WINDOW <-- QWIDGETS '''
counter = 0
counter_max = 30
while counter != counter_max:
    text = QLabel(f'{counter} - RANDOM TEXT', window_widgets)
    text.move(50, 20 + counter*30)
    counter += 1
window_widgets.resize(WINDOW_WIDTH, (counter_max + 1)*30)


''' QSCROLLAREA WINDOW <-- QWIDGET WINDOW '''
window_scroll_area_1st_tab.setWidget(window_widgets)


''' TAB WIDGET <-- QSCROLLAREA WINDOW '''
tab_widget.addTab(window_scroll_area_1st_tab, 'Test - 1')
tab_widget.addTab(window_scroll_area_2nd_tab, 'Test - 2')
tab_widget.setGeometry(20, 50, WINDOW_WIDTH, WINDOW_HEIGHT)


'''
    BUTTON
    Moves the "window_widgets" from the 1st to the 2nd tab
'''
button = QPushButton("Move the 1st tab content to the 2nd tab", window_main)
button.setGeometry(20,10,250,30)
button.clicked.connect(lambda: tab_widget_action())

def tab_widget_action():
    window_scroll_area_2nd_tab.setWidget(window_widgets)


''' MAIN WINDOW <-- TAB WIDGET '''
tab_widget.setParent(window_main)

window_main.show()

sys.exit(app.exec())