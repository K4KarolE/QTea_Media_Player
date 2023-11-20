
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QVideoFrame
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget

from pathlib import Path

'''
PLAY EMPTY SOUND WORKAROUND
at least one music file need to be played from start to finish
before be able to switch tracks without crashing
'''
class MTPlayer:

    def __init__(self, play_base=True):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.video_output = QVideoWidget()
        self.player.setVideoOutput(self.video_output)
        # self.player.setLoops(1) # -1=infinite
        # self.audio_output.setVolume(0)
        if play_base:
            self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
            self.player.play()
        self.played_row = None
        self.base_played = False

