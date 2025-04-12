from PyQt6.QtCore import QThread, pyqtSignal

from .class_data import cv, save_thumbnail_history_json
from .func_thumbnail import create_thumbnails_and_update_widgets


class ThreadThumbnail(QThread):
    result_ready = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

    def run(self):
        thumbnail_widgets_dic = cv.playlist_widget_dic[cv.active_db_table]['thumbnail_widgets_dic']
        if thumbnail_widgets_dic:
            for index in thumbnail_widgets_dic:
                # result = "audio" / "failed" / thumbnail img path
                result = create_thumbnails_and_update_widgets(index)
                self.result_ready.emit(index, result)
            save_thumbnail_history_json()