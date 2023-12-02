
from PyQt6.QtWidgets import QListWidget, QHBoxLayout
from PyQt6.QtWidgets import QFrame, QTabWidget, QScrollBar
from PyQt6.QtGui import QFont

from .func_coll import (
    save_json,
    active_utility,
    generate_track_list_detail,
    add_new_list_item,
    cv, # data
    cur, # db
    settings, # json dic
    PATH_JSON_SETTINGS,
    )


class MyTabs(QTabWidget):

    def __init__(self, play_track):
        super().__init__()

        ''' tabs_created_at_first_run
            USED TO AVOID THE 
            __.currentChanged.connect(self.active_tab)
            SIGNAL AT THE TABS CREATION
        '''
        self.tabs_created_at_first_run = False
        self.play_track = play_track
        self.setFont(QFont('Times', 10, 500))
        self.tabs_creation()
        active_utility() # LOAD ACTIVE NAME and DURATION LIST WIDGETS
        self.setCurrentIndex(cv.active_tab)
        self.currentChanged.connect(self.active_tab)
        cv.active_pl_name.setCurrentRow(cv.last_track_index)
        self.tabs_created_at_first_run = True
        


    def active_tab(self):
        if self.tabs_created_at_first_run:
            cv.active_tab = self.currentIndex()
            settings['last_used_tab'] = cv.active_tab
            save_json(settings, PATH_JSON_SETTINGS)
            active_utility()    # set the current lists(name, duration)


    def name_list_to_duration_row_selection(self):
        cv.active_pl_duration.setCurrentRow(cv.active_pl_name.currentRow())
        cv.active_pl_duration.setStyleSheet(
                            "QListWidget::item:selected"
                                "{"
                                "background: #CCE8FF;"
                                "color: red;"   # font
                                "}"
                            )


    def duration_list_to_name_row_selection(self):
        cv.active_pl_name.setCurrentRow(cv.active_pl_duration.currentRow())
        cv.active_pl_name.setStyleSheet(
                            "QListWidget::item:selected"
                                "{"
                                "background: #CCE8FF;"
                                "color: red;"   # font
                                "}"
                            )
        

    def tabs_creation(self):
        for pl in cv.paylist_widget_dic:
            if settings[pl]['tab_index'] != None:
                
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
            
                cv.paylist_widget_dic[pl]['name_list_widget'] = QListWidget()
                cv.paylist_widget_dic[pl]['name_list_widget'].setVerticalScrollBar(scroll_bar_name_ver)
                cv.paylist_widget_dic[pl]['name_list_widget'].setHorizontalScrollBar(scroll_bar_name_hor)
                # cv.paylist_widget_dic[pl]['name_list_widget'].setAlternatingRowColors(True)
                cv.paylist_widget_dic[pl]['name_list_widget'].currentItemChanged.connect(self.name_list_to_duration_row_selection)

                cv.paylist_widget_dic[pl]['duration_list_widget'] = QListWidget()
                cv.paylist_widget_dic[pl]['duration_list_widget'].setVerticalScrollBar(scroll_bar_duration_ver)
                cv.paylist_widget_dic[pl]['duration_list_widget'].setHorizontalScrollBar(scroll_bar_duration_hor)
                # cv.paylist_widget_dic[pl]['duration_list_widget'].setAlternatingRowColors(True)
                cv.paylist_widget_dic[pl]['duration_list_widget'].setFixedWidth(70)
                cv.paylist_widget_dic[pl]['duration_list_widget'].currentItemChanged.connect(self.duration_list_to_name_row_selection)

                name_list_widget = cv.paylist_widget_dic[pl]['name_list_widget']
                name_list_widget.itemDoubleClicked.connect(self.play_track)
                duration_list_widget = cv.paylist_widget_dic[pl]['duration_list_widget']
                tab_title = settings[pl]['tab_title']
                

                layout = QHBoxLayout()
                layout.setSpacing(0)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(name_list_widget, 90)
                layout.addWidget(duration_list_widget, 10)

                frame = QFrame()
                frame.setStyleSheet(
                                "QFrame"
                                    "{"
                                    "border: 0px;"
                                    "}"
                                )
                frame.setLayout(layout)

                self.addTab(frame, tab_title)

                ''' PLAYLIST DB --> LIST WIDGET '''
                cur.execute("SELECT * FROM {0}".format(pl))
                playlist = cur.fetchall()
                for item in playlist:
                    track_name, duration = generate_track_list_detail(item)
                    add_new_list_item(track_name, name_list_widget, 'left')
                    add_new_list_item(duration, duration_list_widget, 'right')
