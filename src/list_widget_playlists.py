"""
Class created to handle multi row selection and context menu (right-click on the list items) in the main window playlists
Used it in the src / playlists.py
"""

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QListWidget, QMenu, QAbstractItemView

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_queue_update_all_occurrences,
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

        self.context_menu_dic = {
            'Play / Pause': {'icon': br.icon.start},
            f'Queue / Dequeue ({cv.queue_toggle})': {'icon': br.icon.queue_blue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Clear multi selection': {'icon': br.icon.clear_multi_selection},
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
        """ In the used playlist column (one of list widgets: active_pl_name, active_pl_queue, active_pl_duration)
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
        """ The multi selection direction matters
            If the first selected list widget item`s row number smaller than the
            last selected item`s row number (selecting upwards), the first element
            of the "list_widget.selected_items" will not be in order:
            "list_widget.selected_items" by row number example: [13, 9, 10, 11, 12]
       """
        self.selected_items.sort(key=lambda x: self.row(x))
        self.selected_items_row_index_list = [self.row(n) for n in self.selected_items]


    def mouseReleaseEvent(self, event):
        """ Once clicked outside a multi selection >> the multi selection will be
            reduced to a single row / single selection >> to make sure the support selection lists
            mirror this change / lists' values have been removed
            Otherwise when the current, single selected row in the previous multi row selection interval
            >> the row(name, queue, duration) style will not be synced via "playlists / row_changed_sync_pl()"
        """
        if self.currentRow() not in self.selected_items_row_index_list:
            cv.active_pl_name.selected_items_row_index_list = []
            cv.active_pl_queue.selected_items_row_index_list = []
            cv.active_pl_duration.selected_items_row_index_list = []


    """ The "keyPressEvent" and "keyReleaseEvent" functions for avoid using
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


    def eventFilter(self, source, event):
        """ ContextMenu triggered by the right click
            on the list widget
        """
        if event.type() == QEvent.Type.ContextMenu:
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                icon = menu_icon['icon']
                menu.addAction(QAction(icon, menu_title, self))
            # Disable "Clear multi selection" when there is no multi selection
            if not self.selected_items_row_index_list:
                menu.actions()[3].setEnabled(False)
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


        # CLEAR SELECTION
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                if cv.active_pl_name.selected_items_row_index_list:
                    cv.active_pl_name.clearSelection()
                    cv.active_pl_duration.clearSelection()
                    cv.active_pl_queue.clearSelection()
                    cv.active_pl_name.selected_items_row_index_list = []
                    cv.active_pl_queue.selected_items_row_index_list = []
                    cv.active_pl_duration.selected_items_row_index_list = []
                    cv.active_pl_name.setCurrentRow(cv.current_track_index)
                    cv.active_pl_duration.setCurrentRow(cv.current_track_index)
                    cv.active_pl_queue.setCurrentRow(cv.current_track_index)
                    cv.row_change_action_counter = 3
            except:
                MyMessageBoxError('Error', 'Sorry, something went wrong.')


        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                remove_track_from_playlist()
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )
        
        # FOLDER
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                open_track_folder_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'File location',
                    'The file or the file`s home folder has been renamed / removed. '
                    )

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[6]:
            try:
                play_track_with_default_player_via_context_menu(self.currentRow(), cv.active_db_table)
            except:
                MyMessageBoxError(
                    'Not able to play the file',
                    'The file or the file`s home folder has been renamed / removed.  '
                    )