'''
    After placing test.mp4 file in the QTea_Media_Player
    folder* and running the python file
    --> the video should start automatically

    *= or edit the self.path(full path)
'''

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication

import sys
from pathlib import Path


class AVPlayer(QWidget):

    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer()

        self.video_output = QVideoWidget()
        self.player.setVideoOutput(self.video_output)
        
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(1)
        self.player.setAudioOutput(self.audio_output)
        
        # self.path = str(Path(r"D:\_DEV\Python\QTea_Media_Player\test.mp4"))
        self.path = "./test.mp4"
        self.player.setSource(QUrl.fromLocalFile(self.path))
        

app = QApplication(sys.argv)

window = QWidget()
window.resize(500,500)
window.setWindowTitle("Basic Player")

av_player = AVPlayer()
vboxLayout = QVBoxLayout(window)
vboxLayout.addWidget(av_player.video_output)
av_player.player.play()

window.show()
sys.exit(app.exec())