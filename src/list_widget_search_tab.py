'''
Class created to handle context menu (right click on 
the list items), in the Search tab playlist
Used it in the src / window_queue_and_search.py
'''

from PyQt6.QtWidgets import  QListWidget, QMenu
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction

import webbrowser
from pathlib import Path

from .icons import *
from .cons_and_vars import cv
from .message_box import MyMessageBoxError
from .func_coll import (
    get_path_db,
    update_queued_tracks_order_number,
    update_dequeued_track_style_from_queue_window,
    queue_window_remove_track,
    get_playlist_details_from_seacrh_tab_list,
    update_queued_track_style_from_search_tab,
    queue_tab_add_track_from_search_tab,
    search_result_queue_number_update,
    clear_queue_update_all_occurrences
    )


class MySearchListWidget(QListWidget):

    def __init__(self, play_track, playlists_all):
        super().__init__()
        
        self.play_track = play_track    # search_play_list_item()
        self.playlists_all = playlists_all
        self.installEventFilter(self)
        
        icon = MyIcon()
        self.context_menu_dic = { 
            'Play': {'icon': icon.start},
            'Queue / Dequeue': {'icon': icon.queue_blue},
            'Clear queue': {'icon': icon.clear_queue},
            'Jump to playlist': {'icon': icon.toggle_playlist},
            'Open item`s folder': {'icon': icon.folder},
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
                # try:
                self.queue_dequeue_track()
                # except:
                #     MyMessageBoxError('Queue / Dequeue', 'Sorry, something went wrong.')
            

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
                    self.open_track_folder()
                except:
                    MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')
    

    def jump_to_playlist(self):
        current_row_index = self.currentRow()
        playlist, playlist_index, track_index = get_playlist_details_from_seacrh_tab_list(current_row_index)
        self.playlists_all.setCurrentIndex(playlist_index)
    

    def queue_dequeue_track(self):
        current_row_index = self.currentRow()
        playlist, playlist_index, track_index = get_playlist_details_from_seacrh_tab_list(current_row_index)
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

    
    def open_track_folder(self):
        current_row_index = self.currentRow()
        playlist, playlist_index, track_index = get_playlist_details_from_seacrh_tab_list(current_row_index)
        file_path = get_path_db(current_row_index, playlist)
        webbrowser.open(Path(file_path).parent)