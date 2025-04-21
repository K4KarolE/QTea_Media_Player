from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
    )

from .class_data import cv
from .class_bridge import br
from .func_coll import active_track_font_style, inactive_track_font_style


class ThumbnailWidget(QWidget):
    def __init__(self, file_name, index):
        super().__init__()
        self.index = index
        self.thumbnail_type = None
        self.setParent(cv.playlist_widget_dic[cv.active_db_table]["thumbnail_window"].widgets_window)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(cv.thumbnail_width)
        self.layout = QVBoxLayout()

        self.label_image = QLabel()
        self.label_image.setPixmap(br.icon.thumbnail_default)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_text = f'{index + 1}.{file_name}'
        self.text = QLabel(label_text)
        self.text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.layout.addWidget(self.label_image, 95)
        self.layout.addWidget(self.text, 5)
        self.setLayout(self.layout)
        self.set_default_thumbnail_style()
        self.show()

    def mousePressEvent(self, a0):
        cv.active_pl_name.setCurrentRow(self.index)

    def mouseDoubleClickEvent(self, a0):
        """ mousePressEvent() / setCurrentRow() + mouseDoubleClickEvent()
            >> using the standard playlist to play the track via thumbnail
        """
        br.button_play_pause.button_play_pause_via_list()

    def update_img(self, img_file_path):
        self.label_image.setPixmap(QPixmap(img_file_path))

    def update_to_default_video_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_default_video)

    def update_to_playing_video_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_playing_video)

    def update_to_default_audio_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_default_audio)

    def update_to_playing_audio_img(self):
        self.label_image.setPixmap(br.icon.thumbnail_playing_audio)


    def set_default_thumbnail_style(self):
        self.set_default_thumbnail_img()

        self.setStyleSheet(
            "background-color: white;"
            "border: 1px solid grey;"
            "border-radius: 2px;"
        )
        self.label_image.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
        )
        self.text.setFont(inactive_track_font_style)
        self.text.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
        )


    def set_selected_thumbnail_style(self):
        self.set_default_thumbnail_img()

        self.setStyleSheet(
            "background-color: #CCE8FF;"
            "border: 1px solid grey;"
            "border-radius: 2px;"
        )
        self.label_image.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
        )
        self.text.setFont(inactive_track_font_style)
        self.text.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
        )


    def set_playing_thumbnail_style(self):
        self.set_playing_thumbnail_img()

        self.setStyleSheet(
            "background-color: #287DCC;"
            "border: 2px solid grey;"
            "border-radius: 2px;"
        )
        self.label_image.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
        )
        self.text.setFont(active_track_font_style)
        self.text.setStyleSheet(
            "border: 0px;"
            "border-radius: 0px;"
            "color: white;"
        )


    def set_default_thumbnail_img(self):
        if self.thumbnail_type == "audio":
            self.update_to_default_audio_img()
        elif self.thumbnail_type == "video_failed":
            self.update_to_default_video_img()

    def set_playing_thumbnail_img(self):
        if self.thumbnail_type == "audio":
            self.update_to_playing_audio_img()
        elif self.thumbnail_type == "video_failed":
            self.update_to_playing_video_img()
