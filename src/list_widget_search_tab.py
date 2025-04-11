'''
Class created to handle context menu (right click on 
the list items), in the Search tab result list
Used it in the src / window_queue_and_search.py
'''

from PyQt6.QtWidgets import  QListWidget, QMenu
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction


from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_queue_update_all_occurrences,
    get_playlist_details_from_search_tab_list,
    open_track_folder_via_context_menu,
    queue_tab_add_track_from_search_tab,
    queue_window_remove_track,
    play_track_with_default_player_via_context_menu,
    search_result_queue_number_update,
    update_dequeued_track_style_from_queue_window,
    update_queued_track_style_from_search_tab,
    update_queued_tracks_order_number
    )
from .message_box import MyMessageBoxError


class MySearchListWidget(QListWidget):
    def __init__(self, play_track):
        super().__init__()    
        self.play_track = play_track    # search_play_list_item()
        self.installEventFilter(self)
        
        self.context_menu_dic = { 
            'Play': {'icon': br.icon.start},
            'Queue / Dequeue': {'icon': br.icon.queue_blue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Jump to playlist': {'icon': br.icon.toggle_playlist},
            'Open item`s folder': {'icon': br.icon.folder},
            'Play track with default player': {'icon': br.icon.start_with_default_player}
            }   


    def eventFilter(self, source, event):
        '''
        event.type() == QEvent.Type.ContextMenu <-- right click
        self.itemAt(event.pos())    <-- clicked on listwidget item
        '''
        if event.type() == QEvent.Type.ContextMenu and self.itemAt(event.pos()):
            self.current_list_widget = self.itemAt(event.pos())
            menu = QMenu()
            for menu_title, menu_icon in self.context_menu_dic.items():
                icon = menu_icon['icon']
                menu.addAction(QAction(icon, menu_title, self))
            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        if cv.track_change_on_main_playlist_new_search_needed:
            MyMessageBoxError('New search needed', 'Playlists has been changed, please run the search again. ')

        else:
            # PLAY
            if q.text() == list(self.context_menu_dic)[0]:
                try:
                    self.play_track()   # search_play_list_item()
                except:
                    MyMessageBoxError('File location', 'The file or the file`s home folder has been renamed / removed. ')
            
            # QUEUE / DEQUEUE
            elif q.text() == list(self.context_menu_dic)[1]:
                try:
                    self.queue_dequeue_track()
                except:
                    MyMessageBoxError('Queue / Dequeue', 'Sorry, something went wrong.')
            
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
                    MyMessageBoxError('Finding playlist', 'Sorry, something went wrong.')

            # FOLDER
            elif q.text() == list(self.context_menu_dic)[4]:
                try:
                    playlist, playlist_index, track_index = get_playlist_details_from_search_tab_list(self.currentRow())
                    open_track_folder_via_context_menu(track_index, playlist)
                except:
                    MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')

            # PLAY TRACK WITH DEFAULT PLAYER
            elif q.text() == list(self.context_menu_dic)[5]:
                try:
                    playlist, playlist_index, track_index = get_playlist_details_from_search_tab_list(self.currentRow())
                    play_track_with_default_player_via_context_menu(track_index, playlist)
                except:
                    MyMessageBoxError('Not able to play the file',
                                      'The file`s home folder has been renamed / removed. ')


    def jump_to_playlist(self):
        current_row_index = self.currentRow()
        playlist, playlist_index, track_index = get_playlist_details_from_search_tab_list(current_row_index)
        br.playlists_all.setCurrentIndex(playlist_index)
    

    def queue_dequeue_track(self):
        current_row_index = self.currentRow()
        playlist, playlist_index, track_index = get_playlist_details_from_search_tab_list(current_row_index)
        queue_tracking_title = [playlist, track_index]

        # QUEUE
        if not queue_tracking_title in cv.queue_tracks_list:
            # TRACKING
            cv.queue_tracks_list.append(queue_tracking_title)
            cv.queue_playlists_list.append(playlist)
            queue_order_number = f'[{len(cv.queue_tracks_list)}]'
            
            # MOTHER PLAYLIST UPDATE 
            cv.playlist_widget_dic[playlist]['queue_list_widget'].item(track_index).setText(queue_order_number)
            # IF: AVOID CURRENTLY PLAYING TRACK STYLE UPDATE
            if queue_tracking_title != [cv.playing_db_table, cv.playing_pl_last_track_index]:

                update_queued_track_style_from_search_tab(playlist, track_index)

            # QUEUE TAB LIST UPDATE
            title = self.currentItem().text()
            queue_tab_add_track_from_search_tab(playlist, track_index, title)

            # SEARCH TAB - QUEUE LIST UPDATE
            for item in cv.search_result_dic:
                if (cv.search_result_dic[item]['playlist'] == playlist and 
                    cv.search_result_dic[item]['track_index'] == track_index):
                    cv.search_queue_list_widget.item(item).setText(queue_order_number)

        # DEQUEUE
        else:
            queue_window_list_index = cv.queue_tracks_list.index(queue_tracking_title)
            cv.queue_tracks_list.remove(queue_tracking_title)
            cv.queue_playlists_list.remove(playlist)
            cv.playlist_widget_dic[playlist]['queue_list_widget'].item(track_index).setText('')
            
            update_queued_tracks_order_number()
            queue_window_remove_track(queue_window_list_index)

            # IF: AVOID CURRENTLY PLAYING TRACK STYLE UPDATE
            if queue_tracking_title != [cv.playing_db_table, cv.playing_track_index]:
                update_dequeued_track_style_from_queue_window(playlist, track_index)
            
            # SEARCH TAB - QUEUE LIST UPDATE
            for item in cv.search_result_dic:
                if (cv.search_result_dic[item]['playlist'] == playlist and 
                    cv.search_result_dic[item]['track_index'] == track_index):
                    cv.search_queue_list_widget.item(item).setText('')
        search_result_queue_number_update()