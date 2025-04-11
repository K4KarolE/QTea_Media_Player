""" Window holding the thumbnail widgets """


from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QScrollArea,
    QScrollBar
    )

from .class_data import cv
from .class_bridge import br
from .func_thumbnail import thumbnail_widget_resize_and_move_to_pos


class ThumbnailMainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        # self.resize(cv.window_width, cv.window_height)
        self.setMinimumWidth(cv.thumbnail_width + cv.thumbnail_pos_base_x * 2 + cv.scroll_bar_size)
        # self.setWindowTitle("Thumbnails")
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.timer_action())
        self.scroll_bar_ver = QScrollBar()
        self.scroll_bar_ver.setStyleSheet(
            "QScrollBar::vertical"
            "{"
            f"width: {cv.scroll_bar_size}px;"
            "}"
            )
        self.setVerticalScrollBar(self.scroll_bar_ver)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setStyleSheet("background: grey;")
        self.widgets_window = QWidget() # holding all the thumbnail widgets
        self.widgets_window.resize(self.width(), self.height())
        self.setWidget(self.widgets_window)

    def timer_action(self):
        # Timer: For avoiding multiple trigger from resizeEvent
        thumbnail_widget_resize_and_move_to_pos()
        self.timer.stop()

    def resizeEvent(self, a0):
        if cv.thumbnail_main_window_width != self.width():
            cv.thumbnail_main_window_width = self.width()
            cv.thumbnail_main_window_height = self.height()
            self.timer.start(500)
        return super().resizeEvent(a0)
