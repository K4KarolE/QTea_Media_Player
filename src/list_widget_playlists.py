"""
Class created to handle multi row selection and context menu (right-click on the list items) in the main window playlists
Used it in the "src / playlists "
"""

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QListWidget, QMenu, QAbstractItemView

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_multi_selection,
    clear_queue_update_all_occurrences,
    clear_queue_update_for_current_playlist,
    open_track_folder_via_context_menu,
    play_track_with_default_player_via_context_menu,
    queue_add_remove_track,
    remove_track_from_playlist,
    save_thumbnail_size_set_by_context_menu,
    stop_play_when_playing_track_removed
)
from .message_box import MyMessageBoxError


class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.play_track = br.button_play_pause.button_play_pause_via_list
        self.itemDoubleClicked.connect(lambda: self.play_track())
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.row_selection_sync_list_widgets_list = []
        self.is_multi_row_selection_sync_needed = False
        self.is_control_key_pressed: bool = False
        self.selected_items = []
        self.selected_items_row_index_list = []
        self.installEventFilter(self)
        self.setStyleSheet(
                            "QListWidget::item:selected"
                                "{"
                                "background: #CCE8FF;" 
                                "color: black;"   
                                "}"
                            )
        # CONTEXT MENU
        # The displayed value (self.context_menu_queue_title) for the "Temp_queue_dequeue_title" and "icon"
        # will be generated in the "eventFilter()" via "generate_queue_or_dequeue_context_menu_items()"
        # The title and icon depend on the selected track(s) is/are already queued or not
        # Similar behaviour for the "Play / Pause - (Temp_play_pause_title)" section, title and icon depend on
        # if the current track is playing or not
        self.context_menu_queue_title = ''
        self.context_menu_queue_icon = None
        self.thumbnail_image_size_string_list = [str(n) for n in range(100, cv.thumbnail_img_size_max + 1, 100)]
        self.dic_thumbnail_img_size_title = 'Thumbnail image size'
        self.context_menu_dic = {
            'Temp_play_pause_title': {'icon': None},
            'Temp_queue_dequeue_title': {'icon': None},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Clear queue for this playlist only': {'icon': br.icon.clear_queue_current_playlist},
            'Clear multi selection': {'icon': br.icon.clear_multi_selection},
            'Remove': {'icon': br.icon.remove},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player},
            f'{self.dic_thumbnail_img_size_title}': {
                'icon': None,
                'menu_sub': ''
                }
            }


    def generate_queue_or_dequeue_context_menu_items(self):
        queue_dequeue_decider_list = ['','']
        if len(self.selectedItems()) == 1:  # single selection
            queue_tracking_title = [cv.active_db_table, cv.current_track_index]
            if queue_tracking_title in cv.queue_tracks_list:
                queue_dequeue_decider_list[0] = 'to_dequeue'
            else:
                queue_dequeue_decider_list[1] = 'to_queue'
        else:   # multiple selection
            for row_index in self.selected_items_row_index_list:
                queue_tracking_title = [cv.active_db_table, row_index]
                if queue_tracking_title in cv.queue_tracks_list:
                    queue_dequeue_decider_list[0] = 'to_dequeue'
                else:
                    queue_dequeue_decider_list[1] = 'to_queue'
                if queue_dequeue_decider_list[0] and queue_dequeue_decider_list[1]:
                    break
        if queue_dequeue_decider_list[0] and queue_dequeue_decider_list[1]:
            self.context_menu_queue_title = f'Queue / Dequeue ({cv.queue_toggle})'
            self.context_menu_queue_icon = br.icon.queue_blue
        elif queue_dequeue_decider_list[0]:
            self.context_menu_queue_title = f'Dequeue ({cv.queue_toggle})'
            self.context_menu_queue_icon = br.icon.de_queue
        else:
            self.context_menu_queue_title = f'Queue ({cv.queue_toggle})'
            self.context_menu_queue_icon = br.icon.queue_blue


    def set_multi_selection_settings(self):
        """
        Applied once the playlist is created in src / playlists / playlists_creation()
        Used to sync the multi selected rows between the playlist columns (different playlist list widgets):
        active_pl_name, active_pl_queue, active_pl_duration
        """
        self.itemSelectionChanged.connect(lambda: self.selection_changed_multi_selection_action())


    def selection_changed_multi_selection_action(self):
        """
        In the used playlist column (one of list widgets: active_pl_name, active_pl_queue, active_pl_duration)
        the multi selection is automatically applied once the user using the SHIFT key and click combo
        This function is used to sync the multi selection between the rest of the playlist list widgets
        The "is_multi_row_selection_sync_needed" variable helps to avoid recursive selection

        Why not use only the "itemSelectionChanged" signal for row and selection change
        instead of the "src/playlists/currentRowChanged" + "self.itemSelectionChanged" + "self.clicked" signals?

        The "currentRowChanged" and "self.clicked" signals are way faster than the "itemSelectionChanged" signal:
        A,
        Clicking inside / outside an existing selection >> clears the selection apart from the current row by
        default, but the "self.selectedItems()" list still holds the selected list widgets this point
        B, Creating a selection >> triggers the "currentRowChanged" signal, but the "self.selectedItems()" list
        still NOT holds the selected list widgets at this point
        """
        if (self.is_multi_row_selection_sync_needed and len(self.selectedItems()) > 1 and
                not cv.is_multi_selected_drag_drop_in_action):

            self.selected_items = self.selectedItems()
            self.sort_selected_items_and_gen_row_index_list()

            for playlist_list_widget in self.row_selection_sync_list_widgets_list:
                playlist_list_widget.is_multi_row_selection_sync_needed = False

                for row in self.selected_items_row_index_list:
                    if list_widget_item := playlist_list_widget.item(row):
                        list_widget_item.setSelected(True)
                playlist_list_widget.selected_items = playlist_list_widget.selectedItems()
                playlist_list_widget.sort_selected_items_and_gen_row_index_list()

            self.is_multi_row_selection_sync_needed = False


    def sort_selected_items_and_gen_row_index_list(self):
        """
        The multi selection direction matters
        If the first selected list widget item`s row number smaller than the
        last selected item`s row number (selecting upwards), the first element
        of the "list_widget.selected_items" will not be in order:
        "list_widget.selected_items" by row number example: [13, 9, 10, 11, 12]
        """
        self.selected_items.sort(key=lambda x: self.row(x))
        self.selected_items_row_index_list = [self.row(n) for n in self.selected_items]


    def mouseReleaseEvent(self, event):
        """
        Once clicked outside a multi selection >> the multi selection will be
        reduced to a single row / single selection >> to make sure the support selection lists
        mirror this change / lists' values have been removed
        Otherwise when the current, single selected row in the previous multi row selection interval
        >> the row(name, queue, duration) style will not be synced via "playlists / row_changed_sync_pl()"
        """
        if self.currentRow() not in self.selected_items_row_index_list:
            cv.active_pl_name.selected_items_row_index_list = []
            cv.active_pl_queue.selected_items_row_index_list = []
            cv.active_pl_duration.selected_items_row_index_list = []


    """
    The "keyPressEvent" and "keyReleaseEvent" functions for avoid using
    non-continuous selection via "Control key" + "left click"
    Playlist actions like move, delete selected items are created for
    continuous selection only (for now)
    """
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.is_control_key_pressed = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
            self.is_control_key_pressed = False


    def is_current_track_playing(self):
        return (cv.active_db_table == cv.playing_db_table and
                cv.current_track_index == cv.playing_track_index and
                br.av_player.player.isPlaying())


    def eventFilter(self, source, event):
        """
        To compile the context menu, displayed once right-clicked on the non-empty playlist
        """
        if event.type() == QEvent.Type.ContextMenu and cv.active_pl_tracks_count:
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                # Play / Pause
                if menu_title == 'Temp_play_pause_title':
                    if self.is_current_track_playing():
                        menu_title = 'Pause'
                        icon = br.icon.pause
                    else:
                        menu_title = 'Play'
                        icon = br.icon.start

                # Queue / Dequeue
                elif menu_title == 'Temp_queue_dequeue_title':
                    self.generate_queue_or_dequeue_context_menu_items()
                    icon = self.context_menu_queue_icon
                    menu_title = self.context_menu_queue_title

                # Thumbnail image size
                elif menu_title == self.dic_thumbnail_img_size_title:
                    self.context_menu_dic[menu_title]['menu_sub'] = menu.addMenu(menu_title)
                    # When "thumbnail image size" set on the "Settings Window / General / free text field"
                    if str(cv.thumbnail_img_size) not in self.thumbnail_image_size_string_list:
                        self.thumbnail_image_size_string_list.append(str(cv.thumbnail_img_size))
                        self.thumbnail_image_size_string_list.sort()
                    for img_size in self.thumbnail_image_size_string_list:
                        if int(img_size) == cv.thumbnail_img_size:
                            qaction_to_add = QAction(br.icon.selected, img_size, self)
                        else:
                            qaction_to_add = QAction(img_size, self)
                        self.context_menu_dic[self.dic_thumbnail_img_size_title]['menu_sub'].addAction(qaction_to_add)
                else:
                    icon = menu_icon['icon']

                if menu_title != self.dic_thumbnail_img_size_title:
                    menu.addAction(QAction(icon, menu_title, self))
                    if menu_title == 'Play track with default player':
                        menu.addSeparator()

            # Disable "Clear queue" when there is no queued track at all
            if not cv.queue_playlists_list:
                menu.actions()[2].setEnabled(False)

            # Disable "Clear queue for this playlist only"
            # when there is no queued track in the current playlist
            if cv.active_db_table not in cv.queue_playlists_list:
                menu.actions()[3].setEnabled(False)

            # Disable "Clear multi selection" when there is no multi selection
            if not self.selected_items_row_index_list:
                menu.actions()[4].setEnabled(False)

            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        """
        Context menu displayed once right-clicked on the non-empty playlist

        Why not to use "match-case" statement instead of "if/elif q.text() == list(self.context_menu_dic)[1]":
        The match-case statement does not allow indexing, instead of simple value comparisons.

        ERROR:
        match q.text()
            case list(self.context_menu_dic)[1]:    # [1] >> issue
                to_do

        WORKING, but losing the "match-case" syntax simplicity:
        match q.text()
            case x if x == list(self.context_menu_dic)[1]:      # x if x ==
                to_do
        """
        # PLAY
        if q.text() in ['Play', 'Pause']:
            try:
                if self.is_current_track_playing():
                    br.button_play_pause.button_play_pause_clicked()
                else:
                    self.play_track()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )
        
        # QUEUE
        elif q.text() == self.context_menu_queue_title:
            queue_add_remove_track()
        
        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Error','Sorry, something went wrong.')

        # CLEAR QUEUE FOR THE CURRENT PLAYLIST ONLY
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                clear_queue_update_for_current_playlist()
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')

        # CLEAR MULTI SELECTION
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                clear_multi_selection()
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')


        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                stop_play_when_playing_track_removed(False)
                remove_track_from_playlist()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )
        
        # FOLDER
        elif q.text() == list(self.context_menu_dic)[6]:
            try:
                open_track_folder_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[7]:
            try:
                play_track_with_default_player_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'Not able to play the file',
                    'The file or the file`s home folder has been renamed / removed.  '
                    )

        # THUMBNAIL IMAGE SIZE - QUICK SETUP
        elif q.text() in self.thumbnail_image_size_string_list:
            if int(q.text()) != cv.thumbnail_img_size:
                save_thumbnail_size_set_by_context_menu(int(q.text()))