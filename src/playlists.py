''' PLAYLISTS/TABS CREATION '''

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QScrollBar,
    QTabWidget,
    QWidget
    )

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    connection, # db
    cur, # db
    settings, # json dic
    add_new_list_item,
    generate_duration_to_display,
    generate_track_list_detail,
    save_json,
    save_playing_pl_last_track_index,
    update_active_playlist_vars_and_widgets
    )
from .func_thumbnail import (
    thumbnail_repositioning_after_playlist_change,
    update_thumbnail_view_button_style_after_playlist_change
    )
from .list_widget_playlists import MyListWidget
from .thumbnail_window import ThumbnailMainWindow


class MyPlaylists(QTabWidget):
    '''
    playlists_created_at_first_run variable
    USED TO AVOID THE 
        __.currentChanged.connect(self.active_playlist)
    SIGNAL AT THE PLAYLISTS CREATION
    '''
    def __init__(self):
        super().__init__()
        self.playlists_created_at_first_run = False
        self.setFont(QFont('Verdana', 10, 500))
        self.playlists_creation()
        self.setCurrentIndex(cv.playing_playlist_index)
        self.currentChanged.connect(self.active_playlist_changed)
        self.playlists_created_at_first_run = True
        cv.active_playlist_index = self.currentIndex()
        update_active_playlist_vars_and_widgets()
        
        # IF ADD TO THE QUEUE WITHOUT ROW SELECTION AT THE STARTUP
        # GOING TO SELECT THE LAST PLAYED ROW
        cv.current_track_index = cv.active_pl_last_track_index
        
        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
        self.add_dummy_playlist()
        self.hide_playlists_with_no_title()
        self.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background-color: #287DCC;" 
                            "color: white;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 5px;"
                            "padding: 6px"
                            "}"
                        "QTabBar::tab:!selected"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.3 white, stop: 0.8 #C9C9C9, stop: 1 #C2C2C2);"
                            "color: black;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 6px;"
                            "padding: 6px"
                            "}"
                        "QTabWidget::pane"
                            "{" 
                            "position: absolute;"
                            "top: 0.3em;"
                            "}"
                        )


    ''' WORKAROUND / LEARNED '''
    ''' 
    The last tab added to the TABS widget should NOT be hidden
    it will make the right tab selection arrow inactive/unusable to
    select the un-hidden tabs beyond the visible tabs
    workaround --> we leave the last tab always visible and disabled
    '''
    def add_dummy_playlist(self):
        self.addTab(QWidget(), '')
        self.setTabEnabled(cv.playlist_amount, False)

    def hide_playlists_with_no_title(self):
        for index in cv.playlists_without_title_to_hide_index_list:
            self.setTabVisible(index, False)

    def active_playlist_changed(self):
        if self.playlists_created_at_first_run:
            cv.active_playlist_index = self.currentIndex()
            settings['last_used_playlist'] = cv.active_playlist_index
            save_json()
            update_active_playlist_vars_and_widgets()    # set the current lists(name, duration)
            br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
            cv.current_track_index = cv.active_pl_name.currentRow()
            cv.shuffle_played_tracks_list.clear()
            thumbnail_repositioning_after_playlist_change()
            update_thumbnail_view_button_style_after_playlist_change()
    

    ''' SYNC THE LIST'S(NAME, QUEUE, DURATION) SELECTION '''
    def row_changed_sync_pl(self, list_widget_row_changed):
        current_playlist_list_widgets_dic = cv.playlist_widget_dic[cv.active_db_table]
        cv.current_track_index = current_playlist_list_widgets_dic[list_widget_row_changed].currentRow()
        for item in current_playlist_list_widgets_dic:
                if item not in [
                    list_widget_row_changed,
                    'active_pl_sum_duration',
                    'thumbnail_window',
                    'thumbnail_widgets_dic',
                    'thumbnail_window_validation',
                    'line_edit']:
                    current_playlist_list_widgets_dic[item].setCurrentRow(cv.current_track_index)
     
    
    def playlists_creation(self):
        playlist_index_counter = 0
        
        for pl in cv.playlist_widget_dic:
            playlist_title = settings[pl]['playlist_title']
            if not playlist_title:
                cv.playlists_without_title_to_hide_index_list.append(playlist_index_counter)
            playlist_index_counter += 1


            def set_last_played_row_style():
                name_list_widget.setStyleSheet(
                                        "QListWidget::item:selected"
                                            "{"
                                            "background: #CCE8FF;" 
                                            "color: black;"   # font
                                            "}"
                                        )
                
                queue_list_widget.setStyleSheet(
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
            
            cv.playlist_widget_dic[pl]['name_list_widget'] = MyListWidget()
            name_list_widget = cv.playlist_widget_dic[pl]['name_list_widget']
            name_list_widget.setVerticalScrollBar(scroll_bar_name_ver)
            name_list_widget.setHorizontalScrollBar(scroll_bar_name_hor)
            # MOVE TRACK UP / DOWN
            name_list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
            name_list_widget.model().rowsMoved.connect(lambda: self.drag_and_drop_list_item_action())


            cv.playlist_widget_dic[pl]['queue_list_widget'] = MyListWidget()
            queue_list_widget = cv.playlist_widget_dic[pl]['queue_list_widget']
            queue_list_widget.setVerticalScrollBar(scroll_bar_name_ver)
            queue_list_widget.setHorizontalScrollBar(scroll_bar_name_hor)


            cv.playlist_widget_dic[pl]['duration_list_widget'] = MyListWidget()
            duration_list_widget = cv.playlist_widget_dic[pl]['duration_list_widget']
            duration_list_widget.setVerticalScrollBar(scroll_bar_duration_ver)
            duration_list_widget.setHorizontalScrollBar(scroll_bar_duration_hor)
            duration_list_widget.setFixedWidth(70)

            cv.playlist_widget_dic[pl]['thumbnail_window'] = ThumbnailMainWindow()
            thumbnail_window = cv.playlist_widget_dic[pl]['thumbnail_window']
            thumbnail_window.hide()


            layout = QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(name_list_widget, 84)
            layout.addWidget(queue_list_widget, 6)
            layout.addWidget(duration_list_widget, 10)
            layout.addWidget(thumbnail_window)


            frame = QFrame()
            frame.setStyleSheet(
                            "QFrame"
                                "{"
                                "border: 0px;"
                                "}"
                            )
            frame.setLayout(layout)

            self.addTab(frame, playlist_title)


            ''' PLAYLIST DB --> LIST WIDGET '''
            cur.execute("SELECT * FROM {0}".format(pl))
            playlist = cur.fetchall()
            for item in playlist:
                rack_row_db, track_name, duration = generate_track_list_detail(item)
                add_new_list_item(track_name, name_list_widget)
                add_new_list_item('', queue_list_widget)
                add_new_list_item(duration, duration_list_widget)
                cv.playlist_widget_dic[pl]['active_pl_sum_duration'] += int(item[1])
            
            ''' SET BACK / SELECT LAST USED ROWS '''
            name_list_widget.setCurrentRow(settings[pl]['last_track_index'])
            queue_list_widget.setCurrentRow(settings[pl]['last_track_index'])
            duration_list_widget.setCurrentRow(settings[pl]['last_track_index'])
            
            ''' 
                LAST PLAYED ROWS' STYLE
                the currently playing track's style is different --> ignored
            '''
            if cv.play_at_startup == 'False':
                set_last_played_row_style()
            elif cv.play_at_startup == 'True' and pl != cv.playlist_list[cv.playing_playlist_index]:
                set_last_played_row_style()
            

            ''' 
                SYNC THE LIST'S(NAME, DURATION) SELECTION AND STYLE
                AFTER NEWLY SELECTED TRACK
            '''
            name_list_widget.currentRowChanged.connect(lambda: self.row_changed_sync_pl('name_list_widget'))
            duration_list_widget.currentRowChanged.connect(lambda: self.row_changed_sync_pl('duration_list_widget'))
            queue_list_widget.currentRowChanged.connect(lambda: self.row_changed_sync_pl('queue_list_widget'))



    def drag_and_drop_list_item_action(self):
        cv.track_change_on_main_playlist_new_search_needed = True

        prev_row_id = cv.active_pl_duration.currentRow()
        new_row_id = cv.active_pl_name.currentRow()

        new_row_id_db = new_row_id + 1
        prev_row_id_db = prev_row_id + 1

        current_queue_pl_item = cv.active_pl_queue.currentItem()
        current_duration_pl_item = cv.active_pl_duration.currentItem()
        
        
        ''' MOVE / UPDATE QUEUE WITH THE TITLE '''
        cv.active_pl_queue.takeItem(prev_row_id)
        cv.active_pl_queue.insertItem(new_row_id, current_queue_pl_item)
        cv.active_pl_queue.setCurrentRow(new_row_id)
        self.update_queued_tracks_index(prev_row_id, new_row_id)
    
        ''' MOVE DURATION WITH THE TITLE '''
        cv.active_pl_duration.takeItem(prev_row_id)
        cv.active_pl_duration.insertItem(new_row_id, current_duration_pl_item)
        cv.active_pl_duration.setCurrentRow(new_row_id)


        ''' WHEN MOVING TRACK CURRENTLY PLAYING '''
        def set_track_index_when_moving_currently_playing():
            if cv.playing_pl_last_track_index == prev_row_id:
                cv.playing_pl_last_track_index = new_row_id
                cv.playing_track_index = cv.playing_pl_last_track_index
                save_playing_pl_last_track_index()
                return True
            else:
                return False

        ''' 
            MOVE DOWN / MOVE UP    
        '''
        temporary_row_id = 0
        cur.execute("UPDATE {0} SET row_id = {1} WHERE row_id = {2}".format(cv.active_db_table, temporary_row_id, prev_row_id_db))
        connection.commit()

        
        # MOVING TRACK DOWN
        if new_row_id_db > prev_row_id_db:

            cur.execute("UPDATE {0} SET row_id = row_id - 1 WHERE row_id > {1} AND row_id <= {2}".format(cv.active_db_table, prev_row_id_db, new_row_id_db))
            connection.commit()
            
            cur.execute("UPDATE {0} SET row_id = {1} WHERE row_id = {2}".format(cv.active_db_table, new_row_id_db, temporary_row_id))
            connection.commit()

            cur.execute("SELECT * FROM {0} WHERE row_id >= {1} AND row_id <= {2}".format(cv.active_db_table, prev_row_id_db, new_row_id_db))
            playlist = cur.fetchall()
            for item in playlist:
                rack_row_db, list_name, duration = generate_track_list_detail(item)
                cv.active_pl_name.item(rack_row_db-1).setText(list_name)
            

            if not set_track_index_when_moving_currently_playing() and cv.playing_pl_last_track_index in range(prev_row_id, new_row_id + 1):
                cv.playing_pl_last_track_index -= 1
                cv.playing_track_index = cv.playing_pl_last_track_index
                print(cv.playing_pl_last_track_index)
                save_playing_pl_last_track_index()
        
        # MOVING TRACK UP
        else:
            for item in range(prev_row_id_db - 1, new_row_id_db - 1, -1):
                cur.execute("UPDATE {0} SET row_id = row_id + 1 WHERE row_id = {1}".format(cv.active_db_table, item))
            connection.commit()

            cur.execute("UPDATE {0} SET row_id = {1} WHERE row_id = {2}".format(cv.active_db_table, new_row_id_db, temporary_row_id))
            connection.commit()

            cur.execute("SELECT * FROM {0} WHERE row_id <= {1} AND row_id >= {2}".format(cv.active_db_table, prev_row_id_db, new_row_id_db))
            playlist = cur.fetchall()
            for item in playlist:
                rack_row_db, list_name, duration = generate_track_list_detail(item)
                cv.active_pl_name.item(rack_row_db-1).setText(list_name)
            
            if not set_track_index_when_moving_currently_playing() and cv.playing_pl_last_track_index in range(new_row_id, prev_row_id + 1):
                cv.playing_pl_last_track_index += 1
                cv.playing_track_index = cv.playing_pl_last_track_index
                save_playing_pl_last_track_index()
        


    def update_queued_tracks_index(self, prev_row_id, new_row_id):
        if cv.active_db_table in cv.queue_playlists_list:
            for item in cv.queue_tracks_list:   # item = [playlist_3, 6]
                if cv.active_db_table == item[0]:
                    
                    # MOVING THE QUEUED TRACK
                    if item[1] == prev_row_id:
                        item[1] = new_row_id

                    # MOVING A TRACK BELOW THE QUEUED TRACK
                    elif item[1] in range(prev_row_id, new_row_id + 1 ):
                        item[1] = item[1] - 1
                    
                    # MOVING A TRACK ABOVE THE QUEUED TRACK
                    elif item[1] in range(new_row_id, prev_row_id + 1):
                        item[1] = item[1] + 1
