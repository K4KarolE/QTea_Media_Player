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
    scroll_to_active_item_thumbnail_pl,
    thumbnail_repositioning_after_playlist_change,
    update_thumbnail_style_at_row_change,
    update_thumbnail_view_button_style_after_playlist_change
    )
from .list_widget_playlists import MyListWidget
from .logger import logger_runtime
from .thumbnail_window import ThumbnailMainWindow

@logger_runtime
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
        self.playlist_list_widgets_list = ['name_list_widget', 'queue_list_widget', 'duration_list_widget']
        cv.active_playlist_index = self.currentIndex()
        update_active_playlist_vars_and_widgets()

        # IF ADD TO THE QUEUE WITHOUT ROW SELECTION AT THE STARTUP
        # GOING TO SELECT THE LAST PLAYED ROW
        cv.current_track_index = cv.active_pl_last_track_index

        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
        self.add_dummy_playlist()
        self.hide_playlists_with_no_title()
        # Multi rows selection & moving
        self.rows_moved_triggered_counter:int = 1
        self.rows_amount:int
        self.how_many_rows_passed_by:int
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
        self.setTabEnabled(cv.playlists_amount, False)

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
            scroll_to_active_item_thumbnail_pl()


    ''' SYNC THE LIST'S(NAME, QUEUE, DURATION) SELECTION '''
    def row_changed_sync_pl(self, list_widget):
        """ The "is_multi_row_selection_sync_needed" variable to avoid recursive multi selection
            Selecting multiple rows in one of the columns/list widgets (name, queue, duration) >>
            Will sync the selection for the other 2 columns/list widgets
            in the src / list_widget_playlists
        """
        cv.row_change_action_counter += 1
        if cv.row_change_action_counter % 3 == 1:
            cv.row_change_action_counter = 1
            list_widget.is_multi_row_selection_sync_needed = True
            cv.current_track_index = list_widget.currentRow()
            for list_widget_to_sync in list_widget.row_selection_sync_list_widgets_list:
                list_widget_to_sync.clearSelection()
                list_widget_to_sync.setCurrentRow(cv.current_track_index)



    def playlists_creation(self):
        playlist_index_counter = 0

        for pl in cv.playlist_widget_dic:
            playlist_title = settings['playlists'][pl]['playlist_title']
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
                                f"width: {cv.scroll_bar_size}px;"
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


            name_list_widget.row_selection_sync_list_widgets_list = [queue_list_widget, duration_list_widget]
            queue_list_widget.row_selection_sync_list_widgets_list = [name_list_widget, duration_list_widget]
            duration_list_widget.row_selection_sync_list_widgets_list = [name_list_widget, queue_list_widget]


            cv.playlist_widget_dic[pl]['thumbnail_window'] = ThumbnailMainWindow()
            cv.playlist_widget_dic[pl]['thumbnail_window'].hide()


            layout = QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(name_list_widget, 84)
            layout.addWidget(queue_list_widget, 6)
            layout.addWidget(duration_list_widget, 10)
            layout.addWidget(cv.playlist_widget_dic[pl]['thumbnail_window'])


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
                _, track_name, track_path, duration = generate_track_list_detail(item)
                add_new_list_item(track_name, name_list_widget, None, track_path)
                add_new_list_item('', queue_list_widget)
                add_new_list_item(duration, duration_list_widget)
                cv.playlist_widget_dic[pl]['active_pl_sum_duration'] += int(item[1])

            ''' SET BACK / SELECT LAST USED ROWS '''
            name_list_widget.setCurrentRow(settings['playlists'][pl]['last_track_index'])
            queue_list_widget.setCurrentRow(settings['playlists'][pl]['last_track_index'])
            duration_list_widget.setCurrentRow(settings['playlists'][pl]['last_track_index'])

            ''' 
                LAST PLAYED ROWS' STYLE
                the currently playing track's style is different --> ignored
            '''
            if not cv.play_at_startup:
                set_last_played_row_style()
            elif cv.play_at_startup and pl != cv.playlist_list[cv.playing_playlist_index]:
                set_last_played_row_style()


            ''' 
                SYNC THE LIST'S(NAME, DURATION) SELECTION AND STYLE
                AFTER NEWLY SELECTED TRACK
            '''
            def name_list_widget_row_changed():
                self.row_changed_sync_pl(cv.active_pl_name)
                update_thumbnail_style_at_row_change()

            name_list_widget.currentRowChanged.connect(lambda: name_list_widget_row_changed())
            duration_list_widget.currentRowChanged.connect(lambda: self.row_changed_sync_pl(cv.active_pl_duration))
            queue_list_widget.currentRowChanged.connect(lambda: self.row_changed_sync_pl(cv.active_pl_queue))

            name_list_widget.set_multi_selection_settings()
            queue_list_widget.set_multi_selection_settings()
            duration_list_widget.set_multi_selection_settings()


    def drag_and_drop_list_item_action(self):
        if len(cv.active_pl_name.selectedItems()) == 1:
            self.drag_and_drop_single_selection()
        else: self.drag_and_drop_multi_selection()


    def drag_and_drop_single_selection(self):
        cv.row_change_action_counter += 1
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
                track_row_db, list_name, _, _ = generate_track_list_detail(item)
                cv.active_pl_name.item(track_row_db-1).setText(list_name)


            if not set_track_index_when_moving_currently_playing() and cv.playing_pl_last_track_index in range(prev_row_id, new_row_id + 1):
                cv.playing_pl_last_track_index -= 1
                cv.playing_track_index = cv.playing_pl_last_track_index
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
                track_row_db, list_name, _, _ = generate_track_list_detail(item)
                cv.active_pl_name.item(track_row_db-1).setText(list_name)

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


    def drag_and_drop_multi_selection(self):
        """ This function is triggered via the "name_list_widget.model().rowsMoved.connect"
            for every row which has been moved in the "cv.active_pl_name" list widget
            The "self.rows_moved_triggered_counter" var used to execute the sync
            between the name and queue, duration widgets only once when the
            name list widget items already has been relocated
        """
        if self.rows_moved_triggered_counter == len(cv.active_pl_duration.selected_items):
            cv.row_change_action_counter += 1
            cv.track_change_on_main_playlist_new_search_needed = True
            cv.is_multi_selected_drag_drop_in_action = True

            target_row_index = cv.active_pl_name.row(cv.active_pl_name.selected_items[0])

            ''' REPOSITION WIDGETS '''
            # Removing list widget items
            for _ in reversed(cv.active_pl_name.selected_items_row_index_list):
                cv.active_pl_queue.takeItem(_)
                cv.active_pl_duration.takeItem(_)

            # Re-introducing the removed list widget items
            for _ in reversed(cv.active_pl_queue.selected_items):
                cv.active_pl_queue.insertItem(target_row_index, _)
            for _ in reversed(cv.active_pl_duration.selected_items):
                cv.active_pl_duration.insertItem(target_row_index, _)

            self.rows_moved_triggered_counter = 0
            cv.is_multi_selected_drag_drop_in_action = False

            ''' DATABASE AND TRACKS TITLE UPDATE '''
            row_min_db = cv.active_pl_name.selected_items_row_index_list[0] + 1
            row_max_db = cv.active_pl_name.selected_items_row_index_list[-1] + 1
            self.rows_amount = len(cv.active_pl_name.selected_items_row_index_list)
            target_row_index_db = target_row_index + 1

            # Temporary row id placement for the rows we are moving
            cur.execute("UPDATE {0} SET row_id = row_id * -1 WHERE row_id BETWEEN {1} AND {2}"
                        .format(cv.active_db_table, row_min_db, row_max_db))
            connection.commit()

            # MOVING TRACKS DOWN
            if target_row_index > cv.active_pl_name.selected_items_row_index_list[0]:
                # Decrease the row ids between current and target rows
                target_row_index_db_down = target_row_index + self.rows_amount
                cur.execute("UPDATE {0} SET row_id = row_id - {1} WHERE row_id > {2} AND row_id <= {3}".
                            format(cv.active_db_table, self.rows_amount, row_min_db, target_row_index_db_down))

                # Update the row id for the rows with temporary row id
                self.how_many_rows_passed_by = target_row_index_db_down - row_max_db
                cur.execute("UPDATE {0} SET row_id = row_id * -1 + {1} WHERE row_id < 0"
                            .format(cv.active_db_table, self.how_many_rows_passed_by))
                connection.commit()

                # Rename widgets according to the new position (12.Coco Jamboo >> 23.Coco Jumboo)
                cur.execute(
                    "SELECT * FROM {0} WHERE row_id >= {1} AND row_id <= {2}".
                    format(cv.active_db_table, row_min_db, target_row_index_db_down))
                playlist = cur.fetchall()
                for item in playlist:
                    track_row_db, list_name, _, _ = generate_track_list_detail(item)
                    cv.active_pl_name.item(track_row_db - 1).setText(list_name)

                self.update_playing_track_index_multi_selection('Down')

            # MOVING TRACKS UP
            else:
                # Increase the row ids between current and target rows
                for item in reversed(range(target_row_index_db, row_min_db)):
                    cur.execute("UPDATE {0} SET row_id = row_id + {1} WHERE row_id = {2}".
                                format(cv.active_db_table, self.rows_amount, item))

                # Update the row id for the rows with temporary row id
                self.how_many_rows_passed_by = target_row_index_db - row_min_db
                cur.execute("UPDATE {0} SET row_id = row_id * -1 + {1} WHERE row_id < 0"
                            .format(cv.active_db_table, self.how_many_rows_passed_by))
                connection.commit()

                # Rename widgets according to the new position (12.Coco Jamboo >> 23.Coco Jumboo)
                cur.execute(
                    "SELECT * FROM {0} WHERE row_id >= {1} AND row_id <= {2}".
                    format(cv.active_db_table, target_row_index_db, row_max_db))
                playlist = cur.fetchall()
                for item in playlist:
                    track_row_db, list_name, _, _ = generate_track_list_detail(item)
                    cv.active_pl_name.item(track_row_db - 1).setText(list_name)

                self.update_playing_track_index_multi_selection('Up')

            # To make sure after the tracks relocation the selection is reduced back to one row only
            cv.active_pl_queue.setCurrentRow(target_row_index)

            # Update queued tracks index
            self.update_queued_tracks_index_multi_selection(target_row_index)

        self.rows_moved_triggered_counter += 1



    def is_playing_track_in_selection(self):
        return cv.playing_pl_last_track_index in cv.active_pl_name.selected_items_row_index_list


    def update_playing_track_index_multi_selection(self, direction:str):
        if cv.playing_pl_last_track_index: # avoid: start the app without playing + moving rows
            if self.is_playing_track_in_selection():
                cv.playing_pl_last_track_index = cv.playing_pl_last_track_index + self.how_many_rows_passed_by
            else:
                if direction == 'Up':
                    cv.playing_pl_last_track_index += self.rows_amount
                else:
                    cv.playing_pl_last_track_index -= self.rows_amount
            cv.playing_track_index = cv.playing_pl_last_track_index
            save_playing_pl_last_track_index()


    def update_queued_tracks_index_multi_selection(self, target_row_index):
        if cv.active_db_table in cv.queue_playlists_list:
            for item in cv.queue_tracks_list:
                if cv.active_db_table == item[0]:

                    # MOVING THE QUEUED TRACK
                    if item[1] in cv.active_pl_name.selected_items_row_index_list:
                        item[1] = item[1] + self.how_many_rows_passed_by

                    # MOVING A TRACK BELOW THE QUEUED TRACK
                    elif item[1] in range(cv.active_pl_name.selected_items_row_index_list[0], target_row_index + 1):
                        item[1] = item[1] - self.rows_amount

                    # MOVING A TRACK ABOVE THE QUEUED TRACK
                    elif item[1] in range(target_row_index, cv.active_pl_name.selected_items_row_index_list[0] + 1):
                        item[1] = item[1] + self.rows_amount