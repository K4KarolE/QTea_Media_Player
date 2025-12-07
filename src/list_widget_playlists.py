"""
Class created to handle multi row selection and context menu (right-click on the list items) in the main window playlists
Used it in the src / playlists.py 
"""

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QListWidget, QMenu, QAbstractItemView

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_queue_update_all_occurrences,
    is_track_selection_multiple,
    open_track_folder_via_context_menu,
    play_track_with_default_player_via_context_menu,
    queue_add_remove_track,
    remove_track_from_playlist
)
from .message_box import MyMessageBoxError


class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.play_track = br.button_play_pause.button_play_pause_via_list
        self.itemDoubleClicked.connect(lambda: self.play_track())
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.multi_row_selection_sync_list_widgets_list = []
        self.is_multi_row_selection_sync_needed = False
        self.clicked.connect(lambda: self.clear_multi_row_selection())
        self.installEventFilter(self)
        self.setStyleSheet(
                            "QListWidget::item:selected"
                                "{"
                                "background: #CCE8FF;" 
                                "color: black;"   
                                "}"
                            )

        self.context_menu_dic = {
            'Play / Pause': {'icon': br.icon.start},
            f'Queue / Dequeue ({cv.queue_toggle})': {'icon': br.icon.queue_blue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Remove': {'icon': br.icon.remove},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player}
            }


    def clear_multi_row_selection(self):
        """
            Scenario: multiple rows are selected + clicked on the same / last row:
            >> the selection in the active column / list widget automatically cleared by default
            >> this function clears the other two list widgets` selection
        """
        if cv.current_track_index == cv.last_clicked_track_index and is_track_selection_multiple():
            for _ in self.multi_row_selection_sync_list_widgets_list:
                _.clearSelection()
                _.item(cv.current_track_index).setSelected(True)
        cv.last_clicked_track_index = cv.current_track_index


    def set_multi_selection_settings(self):
        """ Applied once the playlist is created in src / playlists / playlists_creation()
            Used to sync the multi selected rows between the playlist columns (different playlist list widgets):
            active_pl_name, active_pl_queue, active_pl_duration
        """
        self.itemSelectionChanged.connect(lambda: self.selection_changed_multi_selection_action())


    def selection_changed_multi_selection_action(self):
        """ In the used playlist column (one of active_pl_name, active_pl_queue, active_pl_duration)
            the multi selection is automatically applied once the user using the SHIFT key and click combo
            This function is used to sync the multi selection between the rest of the playlist list widgets
            The "is_multi_row_selection_sync_needed" variable helps to avoid recursive selection

            Why not use only the "itemSelectionChanged" signal for row and selection change
            instead of the "src/playlists/currentRowChanged" + "self.itemSelectionChanged" + "self.clicked" signals:
            The "currentRowChanged" signal is way faster, the "itemSelectionChanged" signal for the row change
            is way too slow, the 2nd and 3rd list columns/list widget update is visibly late
        """
        if self.is_multi_row_selection_sync_needed and len(self.selectedItems()) > 1:
            row_min, row_max = self.get_multiple_selection_first_and_last_row_index()
            for playlist_list_widget in self.multi_row_selection_sync_list_widgets_list:
                playlist_list_widget.is_multi_row_selection_sync_needed = False
                for row in range(row_min, row_max + 1):
                    if list_widget_item := playlist_list_widget.item(row):
                        list_widget_item.setSelected(True)
            self.is_multi_row_selection_sync_needed = False

    def get_multiple_selection_first_and_last_row_index(self):
        selected_row_number_list = [self.row(n) for n in self.selectedItems()]
        return min(selected_row_number_list), max(selected_row_number_list)


    def eventFilter(self, source, event):
        """ ContextMenu triggered by the right click
            on the list widget
        """
        if event.type() == QEvent.Type.ContextMenu:
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                icon = menu_icon['icon']
                menu.addAction(QAction(icon, menu_title, self))
            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        # PLAY
        if q.text() == list(self.context_menu_dic)[0]:
            try:
                if self.currentRow() == cv.playing_track_index:
                    br.button_play_pause.button_play_pause_clicked()
                else:
                    self.play_track()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )
        
        # QUEUE
        elif q.text() == list(self.context_menu_dic)[1]:
            queue_add_remove_track()
        
        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Error','Sorry, something went wrong.')
        
        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                remove_track_from_playlist()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )
        
        # FOLDER
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                open_track_folder_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                play_track_with_default_player_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'Not able to play the file',
                    'The file or the file`s home folder has been renamed / removed.  '
                    )