
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem
from PyQt6.QtCore import QUrl

from pathlib import Path
import sys

from player import Music


music = Music()

music_list = {
    'Mr.Kitty - After Dark': 'D:\Music\_DOWNLOADS\Mr.Kitty - After Dark [sVx1mJDeUjY].mp3',
    'Mood · Jane & The Boy': 'D:\Music\_DOWNLOADS\Mood · Jane & The Boy [mY_POb8U9mA].mp3'
    }

app = QApplication(sys.argv)
window = QWidget()
listWidget = QListWidget()
window.setWindowTitle("QListWidget")


for item in music_list:
    QListWidgetItem(item, listWidget)


def list_action():
    track_path = music_list[listWidget.currentItem().text()]
    music.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    music.audio_output.setVolume(0.5)
    music.player.play()


listWidget.itemDoubleClicked.connect(list_action)

    
window_layout = QVBoxLayout(window)
window_layout.addWidget(listWidget)
window.setLayout(window_layout)

window.show()

sys.exit(app.exec())
