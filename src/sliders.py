''' DURATION SLIDER AND VOLUME SLIDER CLASSES '''

from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtWidgets import QSlider, QStyle, QLabel
from PyQt6.QtGui import QHoverEvent, QFont

from .class_bridge import br
from .class_data import cv
from .func_coll import (
    generate_duration_to_display,
    save_volume_slider_value,
    update_and_save_volume_slider_value
    )
from .logger import logger_runtime

@logger_runtime
class MySlider(QSlider):
    ''' Duration slider '''
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(30)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.pressed = False
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

        self.hover_over_duration_info_label = QLabel(self)
        self.hover_over_duration_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hover_over_duration_info_label.setParent(br.window)
        self.hover_over_duration_info_label.setFont(QFont('Arial', 8, 600))
        self.hover_over_duration_info_label.hide()
        self.hover_over_duration_info_label.setStyleSheet(
                                                        "QLabel"
                                                        "{"
                                                        "background: #C2C2C2;"
                                                        "border-radius: 5px;"
                                                        "color: black;"
                                                        "}"
                                                        )


    def play_slider_set_value(self):
        ''' PLAYER/DURATION --> SLIDER POSITION '''
        if br.av_player.base_played_end_of_media_signal_ignored:
            self.setValue(br.av_player.player.position())


    def eventFilter(self, source, event):

        if br.av_player.is_playing_or_paused():
            if event.type() == QEvent.Type.MouseButtonPress:
                self.pressed = True
                self.set_slider_value(event)

            if event.type() == QEvent.Type.MouseButtonRelease:
                self.pressed = False

            if event.type() == QHoverEvent.Type.HoverEnter:
                if br.av_player.player.isPlaying() or br.av_player.paused:
                    self.hover_over_duration_info_label.show()

            if event.type() == QHoverEvent.Type.HoverLeave:
                self.hover_over_duration_info_label.hide()

            if event.type() == QEvent.Type.MouseMove:
                duration_to_display = generate_duration_to_display(self.generate_value_from_slider(event))
                self.hover_over_duration_info_label.setText(duration_to_display)
                self.adjust_size_hover_over_duration_info()
                self.hover_over_duration_info_label.move(
                    QPoint(self.get_hover_over_duration_info_pos_x(event), self.pos().y()-8))
                if self.pressed:
                    self.set_slider_value(event)

        return super().eventFilter(source, event)


    def set_slider_value(self, event):
        br.av_player.player.setPosition(self.generate_value_from_slider(event))


    def generate_value_from_slider(self, event):
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.pos().x(), self.width())


    def get_hover_over_duration_info_pos_x(self, event):
        # RIGHT
        if event.pos().x() >= self.width() - self.hover_over_duration_info_label.width():
            return self.width() - self.hover_over_duration_info_label.width() + 9
        # LEFT
        elif event.pos().x() <= self.hover_over_duration_info_label.width() / 2:
            return int(self.hover_over_duration_info_label.width() / 2) - 13
        # MIDDLE
        else: return event.pos().x()


    def adjust_size_hover_over_duration_info(self):
        text_length = len(self.hover_over_duration_info_label.text())
        if text_length > 5:
            self.hover_over_duration_info_label.setFixedSize(text_length*8, 14)
        else: self.hover_over_duration_info_label.setFixedSize(text_length*9, 14)




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
