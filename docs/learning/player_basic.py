"""
The media file paths need to be added (self.path_1, self.path_2)

App freezing when trying to start a new media ("Play 1st" button >> "Play 2nd" button)
More info about the workaround in the "src / av_player"
"""

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget
)

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
        self.player.mediaStatusChanged.connect(self.media_status_changed_action)

        self.path_1 = str(Path("FILE PATH NEEDED"))
        self.path_2 = str(Path("FILE PATH NEEDED"))

    def play_media(self, media_path):
        self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(media_path))

    def media_status_changed_action(self):
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()



app = QApplication(sys.argv)

window = QWidget()
window.resize(500,500)
window.setWindowTitle("Basic Player")

av_player = AVPlayer()

button_1 = QPushButton("Play 1st")
button_1.clicked.connect(lambda: av_player.play_media(av_player.path_1))

button_2 = QPushButton("Play 2nd")
button_2.clicked.connect(lambda: av_player.play_media(av_player.path_2))

vboxLayout = QVBoxLayout(window)
vboxLayout.addWidget(av_player.video_output)
vboxLayout.addWidget(button_1)
vboxLayout.addWidget(button_2)

window.show()
sys.exit(app.exec())