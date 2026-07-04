"""
Switching there and back between the two media >> can increase the memory usage
It is the memory leak of the "QMediaPlayer().setSource()" function

Was trying to create a new AVPlayer class instance for every media play and remove the previous instance
>> The memory leak issue is still in place

For testing, do not forget to add media paths to the "path_1" , "path_2" variables
"""

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget
)

import sys
from pathlib import Path

path_1 = str(Path(""))
path_2 = str(Path(""))


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

    def play_media(self, media_path):
        self.player.setSource(QUrl.fromLocalFile(media_path))

    def media_status_changed_action(self):
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()



app = QApplication(sys.argv)

window = QWidget()
window.resize(500,500)
window.setWindowTitle("Basic Player")

av_player_list = [AVPlayer()]

button_1 = QPushButton("Play 1st")
button_1.clicked.connect(lambda: button_clicked(path_1))

button_2 = QPushButton("Play 2nd")
button_2.clicked.connect(lambda: button_clicked(path_2))


def button_clicked(file_path):
    # Remove previous player
    # No effect adding "sleep(0.5)" between ".stop()", ".deleteLater()", ".pop(0)"
    av_player_list[0].player.stop()
    av_player_list[0].player.deleteLater()
    av_player_list[0].video_output.deleteLater()
    av_player_list.pop(0)
    # Create new player and play media
    av_player_list.append(AVPlayer())
    vboxLayout.addWidget(av_player_list[0].video_output)
    av_player_list[0].play_media(file_path)


vboxLayout = QVBoxLayout(window)
vboxLayout.addWidget(button_1)
vboxLayout.addWidget(button_2)
vboxLayout.addWidget(av_player_list[0].video_output)

window.show()
sys.exit(app.exec())