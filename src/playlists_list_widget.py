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
    list_item_style_update,
    inactive_track_font_style,  
    active_track_font_style
    )


class MyListWidget(QListWidget):

    def __init__(self, play_track, window):
        super().__init__()
        
        self.play_track = play_track
        self.window = window
        self.installEventFilter(self)
        
        icon = MyIcon()
        self.context_menu_dic = { 
            'Play / Pause': {'icon': icon.start},
            'Queue / Dequeue': {'icon': icon.queue},
            'Open item`s folder': {'icon': icon.folder},
            }   


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ContextMenu:

            menu = QMenu()

            for item in self.context_menu_dic:

                icon = self.context_menu_dic[item]['icon']
                menu.addAction(QAction(icon, item, self))
   
            menu.triggered[QAction].connect(self.context_menu_clicked)
            menu.exec(event.globalPos())

        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        # PLAY
        if q.text() == list(self.context_menu_dic)[0]:
            try:
                if self.currentRow() == cv.playing_track_index:
                    self.window.play_pause()
                else:
                    self.play_track()
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')
        
        # Folder
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                file_path = get_path_db(self.currentRow(), cv.active_db_table)
                webbrowser.open(Path(file_path).parent)
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')

        
        # QUEUE
        elif q.text() == list(self.context_menu_dic)[1]:
            
            current_track_index = self.currentRow()
            cv.queue_tracking_title = [cv.active_db_table, current_track_index]

            ''' QUEUED TRACK '''
            if not cv.queue_tracking_title in cv.queued_tracks_list:

                cv.queued_tracks_list.append(cv.queue_tracking_title)

                if current_track_index != cv.playing_pl_last_track_index:

                    self.update_queued_track_style(current_track_index)
                
                queue_order_number = f'[{cv.queued_tracks_list.index(cv.queue_tracking_title) + 1}]'
                cv.active_pl_queue.item(current_track_index).setText(queue_order_number)
            
            
                ''' DEQUEUE / STANDARD TRACK '''
            else:

                cv.queued_tracks_list.remove(cv.queue_tracking_title)
                cv.active_pl_queue.item(current_track_index).setText('')

                if current_track_index != cv.playing_pl_last_track_index:
                
                    self.update_dequeued_track_style(current_track_index)


    def update_queued_track_style(self, current_track_index):
        list_item_style_update(
            cv.active_pl_name.item(current_track_index), 
            inactive_track_font_style,
            'black',
            '#C2C2C2'
            )
        
        list_item_style_update(
            cv.active_pl_queue.item(current_track_index), 
            inactive_track_font_style,
            'black',
            '#C2C2C2'
            )

        list_item_style_update(
            cv.active_pl_duration.item(current_track_index),
            inactive_track_font_style,
            'black',
            '#C2C2C2'
            )


    def update_dequeued_track_style(self, current_track_index):
        list_item_style_update(
            cv.active_pl_name.item(current_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )

        list_item_style_update(
            cv.active_pl_queue.item(current_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )

        list_item_style_update(
            cv.active_pl_duration.item(current_track_index),
            inactive_track_font_style,
            'black',
            'white'
        )
                



