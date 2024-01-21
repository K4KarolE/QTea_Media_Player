''' TABS - PLAYLISTS CREATION '''

from PyQt6.QtWidgets import (
    QListWidget,
    QHBoxLayout,
    QFrame,
    QTabWidget,
    QScrollBar,
    QListView,
    QAbstractItemView
    )
from PyQt6.QtGui import QFont

from PyQt6.QtCore import Qt

from .cons_and_vars import cv
from .func_coll import (
    save_json,
    update_active_tab_vars_and_widgets,
    generate_track_list_detail,
    add_new_list_item,
    generate_duration_to_display,
    cur, # db
    settings, # json dic
    PATH_JSON_SETTINGS,
    )



class MyTabs(QTabWidget):

    def __init__(self, play_track, duration_sum_widg=None):
        super().__init__()

        ''' tabs_created_at_first_run
            USED TO AVOID THE 
            __.currentChanged.connect(self.active_tab)
            SIGNAL AT THE TABS CREATION
        '''
        self.play_track = play_track
        self.duration_sum_widg = duration_sum_widg
        self.tabs_created_at_first_run = False
        self.setFont(QFont('Times', 10, 500))
        self.tabs_creation()
        self.setCurrentIndex(cv.playing_tab)
        self.currentChanged.connect(self.active_tab_changed)
        # cv.active_pl_name.setCurrentRow(cv.last_track_index)
        self.tabs_created_at_first_run = True
        self.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background: #287DCC;" 
                            "color: white;"   # font
                            "}"
                        )
        

    def active_tab_changed(self):
        if self.tabs_created_at_first_run:
            cv.active_tab = self.currentIndex()
            settings['last_used_tab'] = cv.active_tab
            save_json(settings, PATH_JSON_SETTINGS)
            update_active_tab_vars_and_widgets()    # set the current lists(name, duration)
            self.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))


    ''' SYNC THE LIST'S(NAME, DURATION) SELECTION AND STYLE '''
    def name_list_to_duration_row_selection(self):
        cv.active_pl_duration.setCurrentRow(cv.active_pl_name.currentRow())
        if cv.active_pl_name.currentRow() != cv.last_track_index:
            cv.active_pl_duration.setStyleSheet(
                                "QListWidget::item:selected"
                                    "{"
                                    "background: #CCE8FF;" 
                                    "color: black;"   # font
                                    "}"
                                )

    def duration_list_to_name_row_selection(self):
        cv.active_pl_name.setCurrentRow(cv.active_pl_duration.currentRow())
        if cv.active_pl_duration.currentRow() != cv.last_track_index:
            cv.active_pl_name.setStyleSheet(
                                "QListWidget::item:selected"
                                    "{"
                                    "background: #CCE8FF;" 
                                    "color: black;"   
                                    "}"
                                )
    ''' LEARNED '''
    ''' 
        The last tab added to the TABS widget should not be hidden
        it will make the right tab selection arrow inactive/unusable to
        select the un-hidden tabs beyond the visible TABS window
    '''
    def tabs_creation(self):
 
        for pl in cv.paylist_widget_dic:

            tab_title = settings[pl]['tab_title']

            if tab_title:

                def set_last_played_row_style():
                    name_list_widget.setStyleSheet(
                                            "QListWidget::item:selected"
                                                "{"
                                                "background: #CCE8FF;" 
                                                "color: black;"   # font
                                                "}"
                                            )
                    duration_list_widget.setStyleSheet(
                                            "QListWidget::item:selected"
                                                "{"
                                                "background: #CCE8FF;" 
                                                "color: black;"   # font
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
                cv.paylist_widget_dic[pl]['name_list_widget'] = QListWidget() #.model().rowsAboutToBeMoved #.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
                name_list_widget = cv.paylist_widget_dic[pl]['name_list_widget']
                name_list_widget.setVerticalScrollBar(scroll_bar_name_ver)
                name_list_widget.setHorizontalScrollBar(scroll_bar_name_hor)
                name_list_widget.itemDoubleClicked.connect(self.play_track)
                # name_list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
                # name_list_widget.model().rowsMoved.connect(lambda: self.drag_and_drop_list_item())
            

                cv.paylist_widget_dic[pl]['duration_list_widget'] = QListWidget()
                duration_list_widget = cv.paylist_widget_dic[pl]['duration_list_widget']
                duration_list_widget.setVerticalScrollBar(scroll_bar_duration_ver)
                duration_list_widget.setHorizontalScrollBar(scroll_bar_duration_hor)
                duration_list_widget.itemDoubleClicked.connect(self.play_track)
                duration_list_widget.setFixedWidth(70)
                
            
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
                    add_new_list_item(track_name, name_list_widget)
                    add_new_list_item(duration, duration_list_widget)
                    cv.paylist_widget_dic[pl]['active_pl_sum_duration'] += int(item[1])
                
                ''' SET BACK / SELECT LAST USED ROWS '''
                name_list_widget.setCurrentRow(settings[pl]['last_track_index'])
                duration_list_widget.setCurrentRow(settings[pl]['last_track_index'])
                
                ''' 
                    LAST PLAYED ROWS' STYLE
                    the currently playing track's style is different --> ignored
                '''
                if cv.play_at_startup == 'False':
                    set_last_played_row_style()
                elif cv.play_at_startup == 'True' and pl != cv.paylist_list[cv.playing_tab]:
                    set_last_played_row_style()
                

                ''' 
                    SYNC THE LIST'S(NAME, DURATION) SELECTION AND STYLE
                    AFTER NEWLY SELECTED TRACK
                '''
                name_list_widget.currentRowChanged.connect(self.name_list_to_duration_row_selection)
                duration_list_widget.currentRowChanged.connect(self.duration_list_to_name_row_selection)
            
        update_active_tab_vars_and_widgets()
        self.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
    
    def drag_and_drop_list_item(self):
        print(cv.active_pl_duration.currentRow())
    


