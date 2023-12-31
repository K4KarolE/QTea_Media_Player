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

from src import cv, settings, inactive_track_font_style, PATH_JSON_SETTINGS
from src import save_json
from src import MyButtons, MyImage


WIDGET_POS_X=50
WIDGET_POS_Y=50
NUMBER_COUNTER = 1


app = QApplication(sys.argv)

window_settings = QWidget()
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
window_settings.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

for pl in cv.paylist_widget_dic:
    number = QLabel(window_settings, text=f'{NUMBER_COUNTER}.')
    number.move(WIDGET_POS_X - 25, WIDGET_POS_Y)
    number.setFont(inactive_track_font_style)

    cv.paylist_widget_dic[pl]['line_edit'] = QLineEdit(window_settings)
    cv.paylist_widget_dic[pl]['line_edit'].setText(settings[pl]['tab_title'])
    cv.paylist_widget_dic[pl]['line_edit'].setGeometry(50, WIDGET_POS_Y, 120, 20)
    cv.paylist_widget_dic[pl]['line_edit'].setFont(inactive_track_font_style)

    NUMBER_COUNTER += 1
    WIDGET_POS_Y += 40


def is_at_least_one_playlist_title_kept():
    pl_list_with_title = []
    for pl in cv.paylist_widget_dic:
        playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
        if len(playlist_title) != 0:
            pl_list_with_title.append(pl)
    if len(pl_list_with_title) == 0:
        print('ERROR - AT LEAST ONE TITLE REQUIRED')
        return False
    else:
        return pl_list_with_title

    

def button_save_clicked(to_save = False):
    
    if is_at_least_one_playlist_title_kept():
        pl_list_with_title = is_at_least_one_playlist_title_kept()

        for pl in cv.paylist_widget_dic:
            playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
            
            if playlist_title != settings[pl]['tab_title']:
                settings[pl]['tab_title'] = playlist_title
                to_save = True

        ''' IF THE LAST USED TAB/PLAYLIST REMOVED '''
        if  len(settings[cv.paylist_list[cv.active_tab]]['tab_title']) == 0:
               cv.active_tab = settings[pl_list_with_title[-1]]['tab_index']
               settings['last_used_tab'] = cv.active_tab
               to_save = True

        if to_save:
            save_json(settings, PATH_JSON_SETTINGS)


button_save = QPushButton(window_settings, text='SAVE')
button_save.setGeometry(50, WIDGET_POS_Y + 60, 120, 20)    
button_save.clicked.connect(button_save_clicked)


window_settings.show()

sys.exit(app.exec())