
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QPushButton
from PyQt6.QtWidgets import QFileDialog 
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QMovie, QIcon, QFont

# from PyQt6.QtWidgets import QTabWidget, QLabel
# from PyQt6.QtWidgets import QLineEdit
# from PyQt6.QtCore import QSize, QTimer, QTime

import sys

from player import Path
from player import Music
from player import open_json, save_json
from player import PATH_JSON_PLAYLIST


playlist = open_json(PATH_JSON_PLAYLIST)
music = Music()

app = QApplication(sys.argv)
window = QWidget()
listWidget = QListWidget(window)
window.setWindowTitle("Media Player")

def button_add_track_clicked():
    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select an MP3 file")
    dialog_add_track.setNameFilter("MP3 files (*.mp3)")
    dialog_add_track.exec()
    if dialog_add_track.exec and dialog_add_track.selectedFiles():
        track_name = Path(dialog_add_track.selectedFiles()[0]).stem
        QListWidgetItem(track_name, listWidget)
        playlist[track_name] = dialog_add_track.selectedFiles()[0]
        save_json(playlist, PATH_JSON_PLAYLIST)

button_add_track = QPushButton(window, text='Addd track')
# button_music_add.setGeometry(
#     SKIN_WIDGET_POS_X,
#     int(SKIN_WIDEGT_POS_Y + SKIN_WIDEGT_POS_Y_DIFF*3.5),
#     SKIN_WIDGET_WIDTH,
#     BUTTON_SKIN_HEIGHT
#     )
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.clicked.connect(button_add_track_clicked)
button_add_track.setFont(QFont('Times', 10, 600))


for item in playlist:
    QListWidgetItem(item, listWidget)


def list_action():
    track_path = playlist[listWidget.currentItem().text()]
    music.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
    music.audio_output.setVolume(0.5)
    music.player.play()
listWidget.itemDoubleClicked.connect(list_action)

    
window_layout = QVBoxLayout(window)
window_layout.addWidget(button_add_track)
window_layout.addWidget(listWidget)
window.setLayout(window_layout)

window.show()

sys.exit(app.exec())
