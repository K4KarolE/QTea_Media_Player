'''
Class created to handle context menu (right click on 
the list items) in the main window playlists
Used it in the src / playlists.py 
'''
from pathlib import Path
import webbrowser

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import  QListWidget, QMenu

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    clear_queue_update_all_occurrences,
    get_path_db,
    queue_add_remove_track,
    remove_track_from_playlist,
    )
from .message_box import MyMessageBoxError


class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.play_track = br.button_play_pause.button_play_pause_via_list
        self.itemDoubleClicked.connect(self.play_track)
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
            'Queue / Dequeue': {'icon': br.icon.queue_blue},
            'Clear queue': {'icon': br.icon.clear_queue},
            'Remove': {'icon': br.icon.remove},
            'Open item`s folder': {'icon': br.icon.folder},
            }   


    def eventFilter(self, source, event):
        '''
        event.type() == QEvent.Type.ContextMenu <-- right click
        self.itemAt(event.pos())    <-- clicked on listwidget item
        '''
        if event.type() == QEvent.Type.ContextMenu and self.itemAt(event.pos()):

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
                    br.window.play_pause()
                else:
                    self.play_track()
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')
        
        # QUEUE
        elif q.text() == list(self.context_menu_dic)[1]:
            queue_add_remove_track()
        
        # CLEAR QUEUE
        elif q.text() == list(self.context_menu_dic)[2]:
            try:
                clear_queue_update_all_occurrences()
            except:
                MyMessageBoxError('Sorry, something went wrong.')
        
        # REMOVE TRACK
        elif q.text() == list(self.context_menu_dic)[3]:
            try:
                remove_track_from_playlist()
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')
        
        # FOLDER
        elif q.text() == list(self.context_menu_dic)[4]:
            try:
                file_path = get_path_db(self.currentRow(), cv.active_db_table)
                webbrowser.open(Path(file_path).parent)
            except:
                MyMessageBoxError('File location', 'The file`s home folder has been renamed / removed. ')