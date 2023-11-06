
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl

from pathlib import Path



class Music:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setLoops(-1) # -1=infinite
        self.audio_output.setVolume(0.6)


music = Music()
music_list = {
    'Mr.Kitty - After Dark': 'D:/Music/_DOWNLOADS/Mr.Kitty - After Dark [sVx1mJDeUjY].mp3',
    'Mood · Jane & The Boy': 'd:\Music\_DOWNLOADS\Mood · Jane & The Boy [mY_POb8U9mA].mp3'
    }


app = QApplication(sys.argv)
window = QWidget()
listWidget = QListWidget()
window.setWindowTitle("QListWidget")


for item in music_list:
    QListWidgetItem(item, listWidget)


def list_action():
    music.player
    track_path = music_list[listWidget.currentItem().text()]
    music.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    music.player.play()

    
listWidget.itemDoubleClicked.connect(list_action)

    
window_layout = QVBoxLayout(window)
window_layout.addWidget(listWidget)
window.setLayout(window_layout)

window.show()

sys.exit(app.exec())
