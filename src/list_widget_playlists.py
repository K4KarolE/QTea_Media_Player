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
    get_multiple_selection_first_and_last_row_index,
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
        """
        if self.is_multi_selection_sync_needed():
            playlist_list_widgets_list = [cv.active_pl_name, cv.active_pl_queue, cv.active_pl_duration]
            playlist_list_widgets_list.remove(self)
            row_min, row_max = get_multiple_selection_first_and_last_row_index()
            for playlist_list_widget in playlist_list_widgets_list:
                for row in range(row_min, row_max + 1):
                    if list_widget_item := playlist_list_widget.item(row):
                        list_widget_item.setSelected(True)


    def is_multi_selection_sync_needed(self):
        return not cv.is_row_changed_sync_pl_in_action and is_track_selection_multiple()


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