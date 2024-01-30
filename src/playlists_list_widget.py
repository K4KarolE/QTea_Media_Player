from PyQt6.QtWidgets import  QListWidget, QMenu
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction

import webbrowser
from pathlib import Path

from .icons import *
from .cons_and_vars import cv
from .func_coll import get_path_db
from .message_box import MyMessageBoxError


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
        # Play
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


