from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton

from .class_bridge import br
from .class_data import cv


class ButtonJumpToPlaylist(QPushButton):
    """ Used in the PlaylistsTab class """
    def __init__(self, parent, playlist_index):
        super().__init__()
        self.setParent(parent)
        self.playlist_index = playlist_index
        self.setText('>')
        self.setToolTip('Jump to playlist')
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.button_action)
        self.setStyleSheet("QPushButton"
                           "{"
                            "border: 1px solid #C2C2C2;"
                            "border-radius: 4px;"
                            "}"
                           "QPushButton::pressed"
                            "{"
                            "background-color: #C2C2C2;"
                            "}"
                           )

    def button_action(self):
        br.playlists_all.setCurrentIndex(self.playlist_index)



class ButtonRemovePlaylistTitle(ButtonJumpToPlaylist):
    """ Used in the PlaylistsTab class """
    def __init__(self, parent, playlist_index):
        super().__init__(parent, playlist_index)
        self.setText('r')
        self.setToolTip('Remove playlist title')
        self.clicked.connect(self.button_action)

    def button_action(self):
        playlist_title = cv.playlist_list[self.playlist_index]
        cv.playlist_widget_dic[playlist_title]['line_edit'].setText('')
