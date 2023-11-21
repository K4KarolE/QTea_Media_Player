
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl, QEvent, Qt
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget

"""
PLAY EMPTY SOUND WORKAROUND
at least one music file need to be played from start to finish
before be able to switch tracks without crashing
"""
class MTPlayer(QWidget):

    def __init__(self, play_base=True):
        super().__init__()
        self.player = QMediaPlayer()
        # VIDEO
        self.video_output = QVideoWidget()
        self.video_output.installEventFilter(self)
        self.player.setVideoOutput(self.video_output)
        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        if play_base:
            self.player.setSource(QUrl.fromLocalFile('skins/base.mp3'))
            self.player.play()
        self.played_row = None
        self.base_played = False
        # SETTINGS
        # self.player.setLoops(1) # -1=infinite
        self.audio_output.setVolume(1)
    
    
    def eventFilter(self, source, event):
        if source == self.video_output and event.type() == QEvent.Type.MouseButtonDblClick:
            self.vid_full_screen()
        if source == self.video_output and event.type() == QEvent.Type.MouseButtonPress:
            self.pause_play_track()
        # if source == self.video_output and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Space:
            # self.pause_play_track()
        return super().eventFilter(source, event)


    def vid_full_screen(self):
        if self.video_output.isFullScreen():
            self.video_output.setFullScreen(0)
        else:
            self.video_output.setFullScreen(1)
    
    
    def pause_play_track(self):
        if self.player.isPlaying():
            self.player.pause()
        else:
            if self.played_row:
                self.player.play()