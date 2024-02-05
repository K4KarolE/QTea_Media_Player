''' 
WINDOW QUEUE
'''

from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTabWidget,
    QScrollArea,
    QScrollBar
    )

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from pathlib import Path

from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
from .cons_and_vars import save_json
from .func_coll import inactive_track_font_style
from .message_box import MyMessageBoxError
from .icons import MyIcon


class MyQueueWindow(QWidget):
    
    def __init__(self, playlists_all, av_player):
        super().__init__()
        self.playlists_all = playlists_all
        self.av_player = av_player

        '''
        ##############
            WINDOW          
        ##############
        '''
        WINDOW_WIDTH, WINDOW_HEIGHT = 500, 630
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.setWindowIcon(MyIcon().queue)
        self.setWindowTitle("Queue")


        '''
        ############
            TABS         
        ############
        ''' 
        TABS_POS_X, TABS_POS_Y  = 12, 12
        TABS_WIDTH = int(WINDOW_WIDTH - TABS_POS_X *2)
        TABS_HEIGHT = int(WINDOW_HEIGHT - TABS_POS_Y *2)

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Verdana', 10, 500))
        tabs.resize(TABS_WIDTH, TABS_HEIGHT) 
        tabs.move(TABS_POS_X, TABS_POS_Y)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background-color: #287DCC;" 
                            "color: white;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        "QTabBar::tab:!selected"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.3 white, stop: 0.8 #C9C9C9, stop: 1 #C2C2C2);"
                            "color: black;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        "QTabWidget::pane"
                            "{" 
                            "position: absolute;"
                            "top: 0.3em;"
                            "border: 1px solid #C2C2C2;"
                            "border-radius: 2px;"
                            "}"
                        )
        
    
        tab_queue = QWidget() 
        tab_search = QWidget()

        QLabel('test', tab_queue)




        LINE_EDIT_HIGHT = 20
        WIDGETS_POS_X=25
        WIDGETS_POS_Y=20
        WIDGETS_NEXT_LINE_POS_Y_DIFF = 25


        def get_dic_values_before_widget_creation(dic_value):
            item_text = dic_value['text']
            item_value = dic_value['value']
            return item_text, item_value

        def get_dic_values_after_widget_creation(dic_value):
            item_text = dic_value['text']
            item_value = dic_value['value']
            line_edit_text = dic_value['line_edit_widget'].text()
            line_edit_text = line_edit_text.strip().title()
            return item_text, item_value, line_edit_text
        


        '''
        ######################
            TAB - QUEUE        
        ######################
        '''
        WIDGET_HOTKEY_POS_X = WIDGETS_POS_X
        widget_hotkey_pos_y = WIDGETS_POS_Y
        HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF = 180

        


        
        '''
        ######################
            TAB - SEARCH         
        ######################
        '''
        WIDGET_GENERAL_POS_X = WIDGETS_POS_X
        widget_general_pos_y = WIDGETS_POS_Y
        GENERAL_LABEL_LINE_EDIT_POS_X_DIFF = 170

        
        

        ''' 
        #####################
            TABS COMPILING     
        #####################
        
        
        '''
        def set_widgets_window_style(widgets_window):
            widgets_window.setStyleSheet(
                            "QWidget"
                                "{"
                                "background-color: #F9F9F9;"
                                "}"
                            "QLineEdit"
                                "{"
                                "background-color: white;"
                                "}"
                                )
        
        tab_queue.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        set_widgets_window_style(tab_queue)
        tabs.addTab(tab_queue, 'Queue')

        tab_search.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        set_widgets_window_style(tab_search)
        tabs.addTab(tab_search, 'Search')

