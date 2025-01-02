''' DURATION SLIDER AND VOLUME SLIDER CLASSES '''

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QStyle

from .class_bridge import br
from .class_data import cv
from .func_coll import save_volume_slider_value, update_and_save_volume_slider_value 


class MySlider(QSlider):
    ''' Duration slider '''
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(30)
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
                            f"border-radius: 8px;"
                            "background: QLinearGradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2C2C2, stop:1 #E8E8E8);"
                            "width: 15px;"
                            f"margin: -3 px;  /* if <0: expand outside the groove */"
                            "}"

                        "QSlider::sub-page"
                            "{"
                            "background: #287DCC;"
                            "border-radius: 4px;"
                            "}"
                        )
        br.av_player.player.positionChanged.connect(self.play_slider_set_value)
    


    def play_slider_set_value(self):
        ''' PLAYER/DURATION --> SLIDER POSITION '''
        if br.av_player.base_played:
            self.setValue(br.av_player.player.position())


    def mousePressEvent(self, event):
        ''' CLICK SLIDER --> CHANGE SLIDER AND PLAYER POSITION '''
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        br.av_player.player.setPosition(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
     

    def mouseMoveEvent(self, event):
        ''' MOVE SLIDER --> CHANGE SLIDER AND PLAYER POSITION ''' 
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))
        br.av_player.player.setPosition(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width()))

    

class MyVolumeSlider(QSlider):
    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(100)
        self.setFixedSize(100,30)
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
    

    def mousePressEvent(self, event):
        ''' CLICK SLIDER --> CHANGE SLIDER AND PLAYER POSITION '''
        cv.volume_slider_value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())
        self.setValue(cv.volume_slider_value)
        update_and_save_volume_slider_value(cv.volume_slider_value/100)


    def mouseMoveEvent(self, event):
        ''' MOVE SLIDER --> CHANGE SLIDER AND PLAYER POSITION '''
        cv.volume_slider_value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())
        self.setValue(cv.volume_slider_value)
        update_and_save_volume_slider_value(cv.volume_slider_value/100)


    def update_volume(self):
        ''' 
            VOLUME CHANGE CAN BE TRIGGERED BY:
            - Shortcut key
            - Volume slider
            - Scroll wheel over video screen when available
            >> which will update the volume slider
            >> which will update the volume
            --------------------------------------

            TO DISPLAY THE VOLUME CHANGE ON THE VIDEO SCREEN:
            When volume is already 0 or 100 and user tries
            to go beyond:
                volume_up_action() / volume_down_action()
            
            When volume in (0< <100), below:
            br.av_player.text_display_on_video() 
        '''
        br.av_player.audio_output.setVolume(self.sliderPosition()/100)
        save_volume_slider_value(self.sliderPosition()/100)
        br.button_speaker.button_speaker_update() # if muted -> unmuted
        # DISPLAY VOLUME ON VIDEO SCREEN WHEN NO ACTIVE SUBTITLE
        # AND VOLUME CHANGE IS BETWEEN 0< <100
        br.av_player.text_display_on_video(1000, f"Volume:  {str(int(cv.volume*100))}%")
