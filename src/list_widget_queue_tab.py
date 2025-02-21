'''
Class created to handle context menu (right click on 
the list items), in the Queue tab tracklist
Used it in the src / window_queue_and_search.py
'''

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import  QListWidget, QMenu

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_queue_update_all_occurrences,
    get_playlist_details_from_queue_tab_list,
    open_track_folder_via_context_menu,
    play_track_with_default_player_via_context_menu,
    queue_window_remove_track,
    search_result_queue_number_update,
    update_dequeued_track_style_from_queue_window,
    update_queued_tracks_order_number
    )
from .message_box import MyMessageBoxError


class MyQueueListWidget(QListWidget):
    def __init__(self, play_track):
        super().__init__()
        self.play_track = play_track    # queue_play_list_item()
        self.installEventFilter(self)
        
        self.context_menu_dic = { 
            'Play': {'icon': br.icon.start},
            'Dequeue': {'icon': br.icon.de_queue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Jump to playlist': {'icon': br.icon.toggle_playlist},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player}
            }   


    def eventFilter(self, source, event):
        '''
        event.type() == QEvent.Type.ContextMenu <-- right click
        self.itemAt(event.pos())    <-- clicked on listwidget item
        self.currentRow() !=0   <-- avoid the first / title row
        '''
        if event.type() == QEvent.Type.ContextMenu and self.itemAt(event.pos()) and self.currentRow() !=0:
            
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
                self.play_track()   # queue_play_list_item()
            except:
                MyMessageBoxError('File location', 'The file or the file`s home folder has been renamed / removed. ')
        
        # DEQUEUE
        elif q.text() == list(self.context_menu_dic)[1]:
            try:
                self.dequeue_track()
            except:
                MyMessageBoxError('Sorry, something went wrong.')

        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Sorry, something went wrong.')
        
        # JUMP TO PLAYLIST
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                self.jump_to_playlist()
            except:
                MyMessageBoxError('Sorry, something went wrong.')

        # FOLDER
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                current_row_index = self.currentRow() - 1
                playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_tab_list(
                    current_row_index)
                open_track_folder_via_context_menu(track_index, playlist)
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')

        # PLAY TRACK WITH DEFAULT PLAYER
        elif q.text() == list(self.context_menu_dic)[5]:
            try:
                current_row_index = self.currentRow() - 1
                playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_tab_list(
                    current_row_index)
                play_track_with_default_player_via_context_menu(track_index, playlist)
            except:
                MyMessageBoxError('Not able to play the file', 'The file`s home folder has been renamed / removed. ')

    def jump_to_playlist(self):
        current_row_index = self.currentRow() - 1
        playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_tab_list(current_row_index)
        br.playlists_all.setCurrentIndex(playlist_index)
    

    def dequeue_track(self):
        current_row_index = self.currentRow() - 1
        playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_tab_list(current_row_index)
        
        cv.queue_tracks_list.remove(queue_tracking_title)
        cv.queue_playlists_list.remove(playlist)
        cv.playlist_widget_dic[playlist]['queue_list_widget'].item(track_index).setText('')
        
        queue_window_remove_track(current_row_index)
        update_queued_tracks_order_number()
        search_result_queue_number_update()

        ''' Avoid currently playing track style update '''
        if queue_tracking_title != [cv.playing_db_table, cv.playing_track_index]:
            update_dequeued_track_style_from_queue_window(playlist, track_index)