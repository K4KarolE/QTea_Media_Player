
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl, QEvent, Qt
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QAction, QIcon

import ctypes

from .cons_and_vars import cv


'''
DURATION INFO UPDATE
The positionChanged signal action declared in MAIN

PLAY EMPTY SOUND WORKAROUND
- At least one file needs to be played from start to finish
before be able to switch tracks without crashing:
    - At the AVPlayer class instance creation, dummy "song" loaded, played (<1s, no sound)
    - After the 1st dummy track played, no error while switching media
Tried to fix/test:
    - Created an "empty" script to exclude possible errors on my side, same behaviour
    - Checked online sources and GitHub repos, but the class creation steps look the same
'''
class AVPlayer(QWidget):

    def __init__(self, window, icon):
        super().__init__()
        self.window = window
        self.icon = icon

        self.player = QMediaPlayer()
        # VIDEO
        self.video_output = QVideoWidget()
        self.video_output.installEventFilter(self)
        self.player.setVideoOutput(self.video_output)
        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        # BASE PLAY
        self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
        self.player.play()
        # SETTINGS
        self.base_played = False    # 1st auto_play_next_track() run --> base_played = True
        self.audio_output.setVolume(cv.volume)
        self.paused = False
        self.playlist_visible = True
        self.video_area_visible = True
        self.context_menu_dic={ 
            'Play / Pause': self.icon.start,
            'Stop': self.icon.stop,
            'Previous': self.icon.previous,
            'Next': self.icon.next,
        }
    

    def eventFilter(self, source, event):

        if source == self.video_output:
            if event.type() == QEvent.Type.ContextMenu:
                
                menu = QMenu()

                for item in self.context_menu_dic:
                    menu.addAction(QAction(self.context_menu_dic[item], item, self))

                menu.triggered[QAction].connect(self.context_menu_clicked)
                
                menu.exec(event.globalPos())
      
            
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                self.full_screen_toggle()
            

        if event.type() == QEvent.Type.KeyRelease:
            print(66)

            # EXIT FULL SCREEN
            if event.key() == Qt.Key.Key_Escape:
                self.video_output.setFullScreen(0)
                
        return super().eventFilter(source, event)


    def context_menu_clicked(self, q):
        if q.text() == list(self.context_menu_dic)[0]:
            self.window.play_pause()
        elif q.text() == list(self.context_menu_dic)[1]:
            self.window.stop()
        elif q.text() == list(self.context_menu_dic)[2]:
            self.window.previous_track()
        elif q.text() == list(self.context_menu_dic)[3]:
            self.window.next_track()


    def full_screen_toggle(self):
        if self.video_output.isVisible():
            if self.video_output.isFullScreen():
                self.video_output.setFullScreen(0)
            else:
                self.video_output.setFullScreen(1)


    # SCREEN SAVER SETTINGS UPDATE
    # src / func_play_coll.py / play_track()
    # src / buttons / button_play_pause_clicked()
    # main / button_stop_clicked()    
    def screen_saver_on_off(self):
        # SCREEN SAVER OFF
        if self.video_output.isVisible() and self.player.isPlaying():
            self.screen_saver_off()
        # SCREEN SAVER ON
        else:
            self.screen_saver_on()

    def screen_saver_on(self):
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    
    def screen_saver_off(self):
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)



""" 
    Only used for duration calculation -->
    Adding small amount of new record/track:
        Able to add new tracks without interrupting the current playing
    Adding big amount of new record/track:
        Video frame lagging while the new tracks are loading
        No interruption in the sound / only audio media playing
"""
class TrackDuration(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()