''' 
    LEARNED:
    - No key related eventFilter on the app(QApplication)
      otherwise: keyRelease --> multiple trigger
    - Not every eventfilter keys trigger action
      with both: full / non full screen video

    Below how the eventfilter was used in
    an early stage of the project

    This script is not runnable by itself
'''


from PyQt6.QtWidgets import  QWidget
from PyQt6.QtCore import Qt, QEvent



class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.installEventFilter(self) 

    def eventFilter(self, source, event):
        to_save_settings = False

        if event.type() == QEvent.Type.KeyRelease:
            # PAUSE
            if event.key() == Qt.Key.Key_Space:
                button_play_pause.button_play_pause_clicked()

            # VOLUME
            elif event.key() == Qt.Key.Key_Plus:
                new_volume = round(av_player.audio_output.volume() + 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            elif event.key() == Qt.Key.Key_Minus:
                new_volume = round(av_player.audio_output.volume() - 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            
            #JUMP - SMALL
            elif event.key() == Qt.Key.Key_Left:
                av_player.player.setPosition(av_player.player.position() - cv.small_jump)
            elif event.key() == Qt.Key.Key_Right:
                av_player.player.setPosition(av_player.player.position() + cv.small_jump)         
   
            # SPEAKER MUTED TOOGLE
            elif event.key() == Qt.Key.Key_M:
                button_speaker_clicked()

            # PLAY NEXT
            elif event.key() == Qt.Key.Key_N:
                button_next_track.button_next_track_clicked()

            # PLAY PREVIOUS
            elif event.key() == Qt.Key.Key_B:
                button_prev_track.button_prev_track_clicked()    

        if to_save_settings:
            save_volume_set_slider(new_volume, volume_slider)

        return super().eventFilter(source, event)