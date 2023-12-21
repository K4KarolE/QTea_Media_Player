
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl, QEvent, Qt
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget

#TODO from .buttons import MyButtons

# TODO QGraphicsSceneWheelEvent, QGraphicsScene, QGraphicsView, QGraphicsItem

"""
PLAY EMPTY SOUND WORKAROUND
at least one music file need to be played from start to finish
before be able to switch tracks without crashing
"""
class AVPlayer(QWidget):

    def __init__(self, play_base=True, volume=0):
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
        # SETTINGS
        # self.player.setLoops(1) # -1=infinite
        self.audio_output.setVolume(volume)
        self.base_played = False
        self.paused = False
        self.playlist_visible = True
        self.video_area_visible = True
    
    
    def eventFilter(self, source, event):
        if source == self.video_output and event.type() == QEvent.Type.MouseButtonDblClick:
            self.vid_full_screen()
        # PAUSE/PLAY - IF PLAYER IS FULL SCREEN
        # IF NOT FULL SCREEN: SET UP IN 'MyApp class'
        elif event.type() == QEvent.Type.KeyRelease and event.key() == Qt.Key.Key_Space:
            self.pause_play_track()
        elif event.type() == QEvent.Type.KeyRelease and event.key() == Qt.Key.Key_Escape:
            self.video_output.setFullScreen(0)
        # TODO PLAY NEXT
        # elif event.type() == QEvent.Type.KeyRelease and event.key() == Qt.Key.Key_N:
        #     next_track = MyButtons('test', 'Test')
        #     next_track.button_next_track_clicked()
        # TODO elif source == self.video_output and event.type() == QEvent.Type.Wheel:
        #     # print(QEvent.Type.GraphicsSceneWheel)
        #     pass
        
        return super().eventFilter(source, event)


    def vid_full_screen(self):
        if self.video_output.isFullScreen():
            self.video_output.setFullScreen(0)
        else:
            self.video_output.setFullScreen(1)


    def pause_play_track(self):
        if self.player.isPlaying():
            self.player.pause()
            self.paused = True
        else:
            self.player.play()
            self.paused = False


""" 
    Only used for duration calculation -->
    Able to add new track(s) without interrupting 
    the current playing
"""
class TrackDuration(QWidget):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()