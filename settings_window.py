from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QSplitter,
    QLineEdit,
    QLabel
    )

from PyQt6.QtGui import QIcon, QFont


import sys
from src import Path

from src import cv, cur, settings, active_track_font_style, inactive_track_font_style
from src import MyButtons, MyImage


def get_playlist_name(table):
    return cur.execute("SELECT * FROM {0}".format(table)).fetchall() 


WIDGET_POS_X=50
WIDGET_POS_Y=50
NUMBER_COUNTER = 1


app = QApplication(sys.argv)

window_settings = QWidget()
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
window_settings.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

for pl in cv.paylist_widget_dic:
    number = QLabel(window_settings, text=f'{NUMBER_COUNTER}.')
    number.move(WIDGET_POS_X - 20, WIDGET_POS_Y)
    number.setFont(inactive_track_font_style)

    cv.paylist_widget_dic[pl]['line_edit'] = QLineEdit(window_settings)
    cv.paylist_widget_dic[pl]['line_edit'].setText(settings[pl]['tab_title'])
    cv.paylist_widget_dic[pl]['line_edit'].setGeometry(50, WIDGET_POS_Y, 120, 20)
    cv.paylist_widget_dic[pl]['line_edit'].setFont(inactive_track_font_style)

    NUMBER_COUNTER += 1
    WIDGET_POS_Y += 40
    

window_settings.show()

sys.exit(app.exec())