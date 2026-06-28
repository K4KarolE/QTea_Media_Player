from PyQt6.QtCore import QThread, pyqtSignal

from .class_data import cv, save_thumbnail_history_json
from .func_thumbnail import create_thumbnails_and_update_widgets


class ThreadThumbnail(QThread):
    result_ready = pyqtSignal(int, str)

    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist
        self.is_thumbnail_thread_stopped = False

    def run(self):
        """
        Triggered by the "Thumbnail button" under the playlists

        save_thumbnail_history_json():
        Values generated for the "thumbnail history json" in "create_thumbnails_and_update_widgets()"
        """
        cv.thumbnail_active_threads_playlists.append(self.playlist)
        thumbnail_widgets_dic = cv.playlist_widget_dic[self.playlist]['thumbnail_widgets_dic']
        thumbnail_window_validation = cv.playlist_widget_dic[self.playlist]['thumbnail_window_validation']
        thumbnail_window_validation['thumbnail_generation_needed'] = True   # un-completed thumbnail thread
        if thumbnail_widgets_dic:
            for index in thumbnail_widgets_dic:
                if not self.is_thumbnail_thread_stopped:
                    # result = "audio" / "failed" / thumbnail img path
                    result = create_thumbnails_and_update_widgets(self.playlist, index)
                    if result:
                        self.result_ready.emit(index, result)
                    # Safety saving the "thumbnail history json" after every 100 media
                    if index > 0 and index % 100 == 0:
                        save_thumbnail_history_json()
                else:
                    return
            save_thumbnail_history_json()
            thumbnail_window_validation['thumbnail_generation_needed'] = False  # completed thumbnail thread

            if self.playlist in cv.thumbnail_active_threads_playlists:
                cv.thumbnail_active_threads_playlists.remove(self.playlist)

    def set_is_thumbnail_thread_stopped(self, value:bool):
        self.is_thumbnail_thread_stopped = value