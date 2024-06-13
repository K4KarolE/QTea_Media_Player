from PyQt6.QtWidgets import QSlider, QStyle
from PyQt6.QtCore import Qt

from .cons_and_vars import cv
from .func_coll import update_and_save_volume_slider_value, save_volume_slider_value



class MySlider(QSlider):

    def __init__(self, av_player):
        super().__init__()
        self.av_player = av_player
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
                        "QSlider::groove"
                            "{"
                            "background: #C2C2C2;"
                            "height: 10px;"
                            "border-radius: 4px;"
                            "}"

                        "QSlider::handle"
                            "{"
                            "border: 1px solid grey;"
                            "border-radius: 8px;"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2C2C2, stop:1 #E8E8E8);"
                            "width: 15px;"
                            "margin: -3 px;  /* expand outside the groove */"
                            "}"

                        "QSlider::sub-page"
                            "{"
                            "background: #287DCC;"
                            "border-radius: 4px;"
                            "}"
                        )
        av_player.player.positionChanged.connect(self.play_slider_set_value)
    

    ''' PLAYER --> SLIDER '''
    def play_slider_set_value(self):
        if self.av_player.base_played:
            self.setValue(self.av_player.player.position())


    ''' CLICK, MOVE SLIDER --> CHANGE SLIDER AND PLAYER POSITION '''
    def mousePressEvent(self, event):
        # JUMP TO CLICK POSITION
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        self.av_player.player.setPosition(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
     
     
    def mouseMoveEvent(self, event):
        # JUMP TO POINTER POSITION WHILE MOVING
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        self.av_player.player.setPosition(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))

    


class MyVolumeSlider(QSlider):

    def __init__(self, av_player, button_speaker_update):
        super().__init__()
        self.av_player = av_player
        self.button_speaker_update = button_speaker_update

        self.setMinimum(0)
        self.setMaximum(100)
        self.resize(120, 20)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSliderPosition(int(cv.volume*100))
        self.valueChanged.connect(self.update_volume)
        self.setStyleSheet(
                        "QSlider::groove"
                            "{"
                            "background: #C2C2C2;"
                            "height: 8px;"
                            "border-radius: 3px;"
                            "}"

                        "QSlider::handle"
                            "{"
                            "border: 1px solid grey;"
                            "border-radius: 2px;"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2C2C2, stop:1 #E8E8E8);"
                            "width: 15px;"
                            "margin: 0 px;  /* expand outside the groove */"
                            "}"

                        "QSlider::sub-page"
                            "{"
                            "background: #287DCC;"
                            "border-radius: 4px;"
                            "}"
                        )
    

    ''' CLICK, MOVE SLIDER --> CHANGE SLIDER AND PLAYER POSITION '''
    def mousePressEvent(self, event):
        # JUMP TO CLICK POSITION
        cv.volume_slider_value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())
        self.setValue(cv.volume_slider_value)
        update_and_save_volume_slider_value(cv.volume_slider_value/100, self)


    def mouseMoveEvent(self, event):
        # JUMP TO POINTER POSITION WHILE MOVING
        cv.volume_slider_value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())
        self.setValue(cv.volume_slider_value)
        update_and_save_volume_slider_value(cv.volume_slider_value/100, self)


    def update_volume(self):
        self.av_player.audio_output.setVolume(self.sliderPosition()/100)
        save_volume_slider_value(self.sliderPosition()/100)
        self.button_speaker_update() # if muted -> unmuted
        # DISPLAY VOLUME ON VIDEO SCREEN WHEN NO ACTIVE SUBTITLE
        self.av_player.text_display_on_video(1000, f"Volume:  {str(int(cv.volume*100))}%")
