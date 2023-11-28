from PyQt6.QtWidgets import QSlider, QStyle
from PyQt6.QtCore import Qt


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

    

# TODO: volume slider
# volume_slider = MySlider()
# volume_slider.setMinimum(0)
# volume_slider.setMaximum(100)
# volume_slider.resize(100, 20)
# # volume_slider.setParent(under_playlist_window)
# volume_slider.setGeometry(under_play_slider_window.width()-150, 0, 100, 20)