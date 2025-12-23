from PyQt6.QtCore import QThread, pyqtSignal
from .class_bridge import br

"""
    Used for separate the "style update" and "set source" functions
    Otherwise the style update of the name, queue and duration list widget items would
    be so slow/sluggish that style updates would look out of sync, not act as a single row

    play_track() / thread_play_track_set_source.start()
    >> played_and_queued_track_style_update() and result_ready.emit()
    >> result_ready_action() / br.av_player.player.setSource() >> play_track_second_part() 
"""
class ThreadPlayTrackSetSource(QThread):
    result_ready = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        br.play_funcs.played_and_queued_track_style_update()
        self.result_ready.emit()