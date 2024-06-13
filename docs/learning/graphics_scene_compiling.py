'''
The below is not used in this project - saving for later
Layout <- QGraphicsView() <- QGraphicsScene() <- QGraphicsVideoItem()
'''

from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView



class AVPlayer(QWidget):

    def __init__(self):
        super().__init__()
      
        self.player = QMediaPlayer()
        self.video_output = QGraphicsVideoItem()
        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()

        self.scene.addItem(self.video_output)
        self.graphicsView.setScene(self.scene)
        # self.graphicsView.fitInView(self.scene.sceneRect())   # could not see any difference        
        self.player.setVideoOutput(self.video_output)

        # AUDIO
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)


'''
layout_vert_left.addWidget(av_player.graphicsView)

text = QLabel("random text")
text.setStyleSheet("QLabel { background-color : red; color : white; }")
text.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)    # BG invisible
text.setGeometry(100, 100, 50, 50)

scene.addWidget(text)
'''
     