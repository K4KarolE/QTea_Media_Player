from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTabWidget
    )

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from pathlib import Path

from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
from .cons_and_vars import save_json
from .func_coll import inactive_track_font_style



class MySettingsWindow(QWidget):
    
    
    def __init__(self):
        super().__init__()

        ''' WINDOW '''
        WINDOW_WIDTH, WINDOW_HEIGHT = 250, 530
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(str(Path(Path().resolve(), 'skins', cv.skin_selected, 'settings.png'))))
        self.setWindowTitle("Settings")


        ''' TABS '''
        WIDGET_POS_X=25
        WIDGET_POS_Y=25
        number_counter = 1
        
        TABS_POS_X = 10
        TABS_POS_Y = 10

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Times', 10, 500))
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background: #287DCC;" 
                            "color: white;"   # font
                            "}"
                        )

        tab_playlist = QWidget() 
        tab_general = QWidget()

        tabs.addTab(tab_playlist, 'Playlists')
        tabs.addTab(tab_general, 'General')
        tabs.resize(WINDOW_WIDTH-TABS_POS_X*2, WINDOW_HEIGHT-TABS_POS_Y*6) 
        tabs.move(TABS_POS_X+2, TABS_POS_Y+2)
        

        ''' TAB - PLAYLISTS '''
        for pl in cv.paylist_widget_dic:
            number = QLabel(tab_playlist, text=f'{number_counter}.')
            number.setFont(inactive_track_font_style)
            
            if number_counter >= 10:
                number.move(WIDGET_POS_X - 7, WIDGET_POS_Y)
            else:
                number.move(WIDGET_POS_X, WIDGET_POS_Y)

            cv.paylist_widget_dic[pl]['line_edit'] = QLineEdit(tab_playlist)
            cv.paylist_widget_dic[pl]['line_edit'].setText(settings[pl]['tab_title'])
            cv.paylist_widget_dic[pl]['line_edit'].setGeometry(WIDGET_POS_X + 20, WIDGET_POS_Y, 150, 20)
            cv.paylist_widget_dic[pl]['line_edit'].setFont(inactive_track_font_style)

            number_counter += 1
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

            
        ''' BUTTON - SAVE'''
        BUTTON_SAVE_WIDTH = 50
        BUTTON_SAVE_HIGHT = 25
        BUTTON_SAVE_POS_X = WINDOW_WIDTH - TABS_POS_X - BUTTON_SAVE_WIDTH
        BUTTON_SAVE_POS_Y = WINDOW_HEIGHT - TABS_POS_Y - BUTTON_SAVE_HIGHT

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
            
            self.hide()


        button_save = QPushButton(self, text='SAVE')
        button_save.setGeometry(BUTTON_SAVE_POS_X, BUTTON_SAVE_POS_Y, BUTTON_SAVE_WIDTH, BUTTON_SAVE_HIGHT)    
        button_save.clicked.connect(button_save_clicked)
