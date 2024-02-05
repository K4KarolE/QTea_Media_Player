''' 
WINDOW QUEUE
'''


from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QTabWidget,
    QScrollBar,
    QAbstractItemView,
    QListWidget
    )

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from pathlib import Path

from .cons_and_vars import cv
from .playlists_list_widget import MyListWidget
from .func_coll import (
    save_json,
    update_active_playlist_vars_and_widgets,
    generate_track_list_detail,
    add_new_list_item,
    add_queue_window_list_widgets_header,
    generate_duration_to_display,
    save_playing_last_track_index,
    cur, # db
    connection, # db
    settings, # json dic
    PATH_JSON_SETTINGS,
    )
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
        WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500
        
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
        
    
        
        scroll_bar_name_ver = QScrollBar()
        scroll_bar_name_hor = QScrollBar()
        scroll_bar_duration_ver = QScrollBar()
        scroll_bar_duration_hor = QScrollBar()

        scroll_bar_name_ver.valueChanged.connect(scroll_bar_duration_ver.setValue)
        scroll_bar_duration_ver.valueChanged.connect(scroll_bar_name_ver.setValue)

        scroll_bar_name_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        scroll_bar_name_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
        
        scroll_bar_duration_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"               
                        )
        
        scroll_bar_duration_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
        

        
        ''' LISTS CREATION '''
        ''' Lists -> QHBoxLayout -> QFrame -> Add as a Tab '''
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for item in cv.queue_widget_dic:
            title = cv.queue_widget_dic[item]['list_widget_title']
            ratio = cv.queue_widget_dic[item]['list_widget_window_ratio']
            cv.queue_widget_dic[item]['list_widget'] = QListWidget()
            list_widget = cv.queue_widget_dic[item]['list_widget']
            
            add_queue_window_list_widgets_header(title, list_widget)
            layout.addWidget(list_widget, ratio)





        frame = QFrame()
        frame.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame.setLayout(layout)

        tabs.addTab(frame, 'Queue')



        
        

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
        
        # tab_queue.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # set_widgets_window_style(tab_queue)
        # tabs.addTab(tab_queue, 'Queue')

        tab_search = QWidget()
        tab_search.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        set_widgets_window_style(tab_search)
        tabs.addTab(tab_search, 'Search')

