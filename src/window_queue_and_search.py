''' 
WINDOW QUEUE & SEARCH WINDOW is displayed once
"Q" button clicked under the playlists section

Window title update is declared in
src/func_play_coll/update_window_title()
'''

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QTabWidget,
    QVBoxLayout,
    QScrollBar,
    QLineEdit,
    QPushButton
    )

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    inactive_track_font_style,
    add_new_list_item,
    add_queue_window_list_widgets_header,
    get_playlist_details_from_queue_tab_list,
    get_playlist_details_from_search_tab_list,
    update_playing_playlist_vars_and_widgets
    )
from .list_widget_queue_tab import MyQueueListWidget
from .list_widget_search_tab import MySearchListWidget
from .message_box import MyMessageBoxError


class MyQueueAndSearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        WINDOW_WIDTH, WINDOW_HEIGHT = 700, 400
        WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT = 500, 200
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setWindowIcon(br.icon.queue_blue)
        self.setWindowTitle("Queue & Search")
        self.search_criteria = ""
        self.is_empty_search_result = False
        self.empty_search_result_msg = ""
        
        TABS_POS_X, TABS_POS_Y  = 12, 12
        TABS_WIDTH = int(WINDOW_WIDTH - TABS_POS_X *2)
        TABS_HEIGHT = int(WINDOW_HEIGHT - TABS_POS_Y *2)
        tabs = QTabWidget()
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
        
        ''' 
        #################
            QUEUE TAB
        ################
        Lists -> QHBoxLayout -> QFrame -> 
        Add as a Tab --> Layout --> Window
        '''
        scroll_bar_else_ver = QScrollBar()
        scroll_bar_duration_ver = QScrollBar()
      
        scroll_bar_else_ver.valueChanged.connect(scroll_bar_duration_ver.setValue)
        scroll_bar_duration_ver.valueChanged.connect(scroll_bar_else_ver.setValue)

        scroll_bar_else_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        
        scroll_bar_duration_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"
                        )               
        
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for item in cv.queue_widget_dic:
            title = cv.queue_widget_dic[item]['list_widget_title']
            ratio = cv.queue_widget_dic[item]['list_widget_window_ratio']
            fixed_width = cv.queue_widget_dic[item]['fixed_width']
            
            cv.queue_widget_dic[item]['list_widget'] = MyQueueListWidget(self.queue_play_list_item)
            list_widget = cv.queue_widget_dic[item]['list_widget']
            list_widget.itemDoubleClicked.connect(self.queue_play_list_item)
            
            if fixed_width:
                list_widget.setFixedWidth(fixed_width)
            
            if item == 'duration_list_widget':
                list_widget.setVerticalScrollBar(scroll_bar_duration_ver)
            else:
                list_widget.setVerticalScrollBar(scroll_bar_else_ver)

            add_queue_window_list_widgets_header(title, list_widget)
            layout.addWidget(list_widget, ratio)
        
        cv.queue_widget_dic['queue_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.queue_row_changed_sync('queue_list_widget'))
        cv.queue_widget_dic['name_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.queue_row_changed_sync('name_list_widget'))
        cv.queue_widget_dic['playlist_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.queue_row_changed_sync('playlist_list_widget'))
        cv.queue_widget_dic['duration_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.queue_row_changed_sync('duration_list_widget'))

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
        ###################
            SEARCH TAB     
        ###################
        '''
        layout_search_base = QVBoxLayout()
        layout_search_base.setSpacing(10)    # top - bottom
        layout_search_base.setContentsMargins(10, 10, 10, 10) # around base(top & bottom)

        layout_search_top = QHBoxLayout()
        layout_search_top.setSpacing(10)    # button - line edit

        layout_search_bottom = QHBoxLayout()
        layout_search_bottom.setSpacing(0)

        layout_search_base.addLayout(layout_search_top, 10)
        layout_search_base.addLayout(layout_search_bottom, 90)


        ''' TOP WIDGETS '''
        SEARCH_WIDGETS_HEIGHT = 25
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setFixedHeight(SEARCH_WIDGETS_HEIGHT)
        self.search_line_edit.setFont(inactive_track_font_style)
        self.search_line_edit.returnPressed.connect(lambda: self.search_button_clicked())

        search_button = QPushButton()
        search_button.setIcon(br.icon.search)
        search_button.setFixedSize(28, 28)
        search_button.clicked.connect(lambda: self.search_button_clicked())
        search_button.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #D5DFE2, stop: 0.8 #D5DFE2, stop: 1 #C2C2C2);"
                            "border: 1px solid grey;"
                            "border-radius: 6px;"
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : white;"
                            "}"
                        )


        ''' BOTTOM WIDGETS '''
        scroll_bar_search_title_ver = QScrollBar()
        scroll_bar_search_queue_ver = QScrollBar()
        
        scroll_bar_search_title_ver.valueChanged.connect(scroll_bar_search_queue_ver.setValue)
        scroll_bar_search_queue_ver.valueChanged.connect(scroll_bar_search_title_ver.setValue)
        
        scroll_bar_search_title_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        
        scroll_bar_search_queue_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"
                        )
       
        cv.search_title_list_widget = MySearchListWidget(self.search_play_list_item)
        cv.search_title_list_widget.itemDoubleClicked.connect(self.search_play_list_item)
        cv.search_title_list_widget.setVerticalScrollBar(scroll_bar_search_title_ver)
        cv.search_title_list_widget.setStyleSheet(
                                                "QListWidget::item:selected"
                                                    "{"
                                                    "background: #CCE8FF;" 
                                                    "color: black;"   
                                                    "}"
                                                )

        cv.search_queue_list_widget = MySearchListWidget(self.search_play_list_item)
        cv.search_queue_list_widget.itemDoubleClicked.connect(self.search_play_list_item)
        cv.search_queue_list_widget.setVerticalScrollBar(scroll_bar_search_queue_ver)
        cv.search_queue_list_widget.setFixedWidth(50)
        cv.search_queue_list_widget.setStyleSheet(
                                                "QListWidget::item:selected"
                                                    "{"
                                                    "background: #CCE8FF;" 
                                                    "color: black;"   
                                                    "}"
                                                )
        
        cv.search_title_list_widget.currentRowChanged.connect(lambda: self.search_row_changed_sync(cv.search_title_list_widget))
        cv.search_queue_list_widget.currentRowChanged.connect(lambda: self.search_row_changed_sync(cv.search_queue_list_widget))


        layout_search_top.addWidget(search_button)
        layout_search_top.addWidget(self.search_line_edit)
        layout_search_bottom.addWidget(cv.search_title_list_widget, 99)
        layout_search_bottom.addWidget(cv.search_queue_list_widget, 1)

        frame_search = QFrame()
        frame_search.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame_search.setLayout(layout_search_base)

        tabs.addTab(frame_search, 'Search')


        '''
        #################################
            TABS -> Layout -> Window
        #################################
        '''
        layout_window = QVBoxLayout(self)
        layout_window.addWidget(tabs)


    ''' QUEUE FUNCS '''
    def queue_play_list_item(self):
        current_row_index = cv.queue_widget_dic['name_list_widget']['list_widget'].currentRow() - 1
        playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_tab_list(current_row_index)
        cv.playing_playlist_index = playlist_index
        update_playing_playlist_vars_and_widgets()
        br.play_funcs.play_track(track_index)
        br.button_play_pause.setIcon(br.icon.pause)
    

    def queue_row_changed_sync(self, list_widget_row_changed):
        current_row = cv.queue_widget_dic[list_widget_row_changed]['list_widget'].currentRow()
        for item in cv.queue_widget_dic:
            if item != list_widget_row_changed:
                if current_row == 0:    # first row: Order number, Title, Queue, Duration
                    color = '#D5DFE2'
                else:
                    color = '#CCE8FF'
                cv.queue_widget_dic[item]['list_widget'].setCurrentRow(current_row)
                cv.queue_widget_dic[item]['list_widget'].setStyleSheet(
                                                            "QListWidget::item:selected"
                                                                "{"
                                                                f"background: {color};" 
                                                                "color: black;"   
                                                                "}"
                                                            )
    

    ''' SEARCH FUNCS '''
    def search_row_changed_sync(self, list_widget):
        current_row = list_widget.currentRow()
        if list_widget == cv.search_title_list_widget:
            cv.search_queue_list_widget.setCurrentRow(current_row)
        else:
            cv.search_title_list_widget.setCurrentRow(current_row)
            
 
    def search_play_list_item(self):
        if not self.is_empty_search_result:
            if not cv.track_change_on_main_playlist_new_search_needed:
                current_row_index = cv.search_title_list_widget.currentRow()
                playlist, playlist_index, track_index = get_playlist_details_from_search_tab_list(current_row_index)
                cv.playing_playlist_index = playlist_index
                update_playing_playlist_vars_and_widgets()
                br.play_funcs.play_track(track_index)
                br.button_play_pause.setIcon(br.icon.pause)
            else:
                MyMessageBoxError('New search needed', 'Playlists has been changed, please run the search again. ')

    
    def search_button_clicked(self):
        cv.track_change_on_main_playlist_new_search_needed = False
        self.search_criteria = self.search_line_edit.text().strip().lower()
        self.empty_search_result_msg = f'-- Could not find any matches for "{self.search_criteria}" --'

        if len(self.search_criteria) > 2:
            self.search_create_result_dic()
            cv.search_title_list_widget.clear()
            cv.search_queue_list_widget.clear()
            if cv.search_result_dic:
                self.is_empty_search_result = False
                self.search_display_result()
            else:
                self.is_empty_search_result = True
                add_new_list_item(self.empty_search_result_msg, cv.search_title_list_widget, True)
        else:
            MyMessageBoxError('Invalid search', 'The search criteria has to be more than 2 characters long.')
           


    def search_create_result_dic(self):
        result_counter = 0
        cv.search_result_dic = {}
        cv.search_result_queued_tracks_index_list = []
        for playlist in cv.playlist_widget_dic:
            playlist_title = cv.playlist_widget_dic[playlist]['line_edit'].text()
            if playlist_title:  # avoiding hidden playlists
                name_list_widget = cv.playlist_widget_dic[playlist]['name_list_widget']
                for track_index in range(0, name_list_widget.count()):
                    track_title = name_list_widget.item(track_index).text()
                    if self.search_criteria in track_title.lower():
                        queue_list_widget = cv.playlist_widget_dic[playlist]['queue_list_widget']
                        queue_number = queue_list_widget.item(track_index).text()
                        if queue_number:
                            cv.search_result_queued_tracks_index_list.append(result_counter)

                        cv.search_result_dic[result_counter] = {
                            'track_title': track_title,
                            'playlist': playlist,
                            'track_index': track_index,
                            'queue_number': queue_number
                            }
                        result_counter += 1
    

    def search_display_result(self):
        for item in cv.search_result_dic:
            track_title = cv.search_result_dic[item]['track_title']
            add_new_list_item(track_title, cv.search_title_list_widget)
            
            playlist = cv.search_result_dic[item]['playlist']
            track_index = cv.search_result_dic[item]['track_index']
            queue_number = cv.search_result_dic[item]['queue_number']
            if [playlist, track_index] in cv.queue_tracks_list:
                add_new_list_item(queue_number, cv.search_queue_list_widget, True)
            else:
                add_new_list_item('', cv.search_queue_list_widget, True)
