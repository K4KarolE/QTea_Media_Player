from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel,
    QScrollArea,
    QWidget, QVBoxLayout, QHBoxLayout
)

from .class_bridge import br
from .func_coll import inactive_track_font_style
from .window_settings_common import CommonTabValues


class AboutTab(CommonTabValues):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.inner_window = QWidget()
        self.last_widget_pos_y = 550    # 524 >> covers the BG without scroll bar
        current_app_version = ' 0.2.0 Butch'

        """
        BASE
         _______________
        | LFT  |  RI   |    TOP
        |______|_______|
        |              |
        |   BOTTOM     |
        |______________|
        
        TOP LEFT: image
        TOP RIGHT: app title and version
        BOTTOM: text
        """

        # BASE / TOP / BOTTOM
        base_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        bottom_layout.setContentsMargins(15, 20, 10, 0)

        base_layout.addLayout(top_layout, 5)
        base_layout.addLayout(bottom_layout, 95)

        # TOP LEFT
        dist_from_top = 30
        top_layout_left = QVBoxLayout()
        top_layout_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout_left.setContentsMargins(0, dist_from_top, 0, 0)

        # TOP RIGHT
        top_layout_right = QVBoxLayout()
        top_layout_right.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter)
        top_layout_right.setContentsMargins(0, dist_from_top, 0, 0)

        top_layout.addLayout(top_layout_left, 20)
        top_layout.addLayout(top_layout_right, 80)

        self.inner_window.setLayout(base_layout)

        # IMAGE - TOP LEFT
        logo_img_label = QLabel()
        logo_img_label.setPixmap(br.icon.thumbnail_default)

        # TITLE, VERSION - TOP RIGHT
        title_label = QLabel('QTea media player')
        title_label.setFont(QFont('Arial', 20, 600))
        version_label = QLabel(current_app_version)
        version_label.setFont(QFont('Arial', 14, 500))

        top_layout_left.addWidget(logo_img_label)
        top_layout_right.addWidget(title_label,50)
        top_layout_right.addWidget(version_label,50)

        # TEXT - BOTTOM
        text_label = QLabel()
        text_label.setFont(inactive_track_font_style)
        text_label.setOpenExternalLinks(True)
        text_label.setTextFormat(Qt.TextFormat.RichText)
        bottom_layout.addWidget(text_label)
        text_label_content = """
        QTea media player is a free and open source<br>
        media player created by Karoly Egyed.
        <br>
        <br>
        QTea uses <b>PyQt`s</b> internal codecs and works<br> with all the popular media formats.
        <br><br><br>
        <b>LICENSE</b>
        <br><br>
        QTea created under the <a href="https://github.com/K4KarolE/QTea_Media_Player/blob/main/LICENSE">MIT</a> license.
        <br><br>
        Please note, the <b>PyQt, OpenCV</b> libraries used<br> in the development, have different licenses.<br>
        <br>
        For more, please visit:       
        <a href="https://pypi.org/project/PyQt6/">PyQt</a>, 
        <a href="https://opencv.org/license/">OpenCV</a>
        <br><br><br>
        
        <b>CONTACT</b>
        <br><br>
        Email: k4karole@duck.com
        <br>
        GitHub: <a href="https://github.com/K4KarolE">https://github.com/K4KarolE</a>
        <br>
        YouTube: <a href="https://www.youtube.com/@K4KarolE">https://www.youtube.com/@K4KarolE</a>
        <br>
        X / Twitter: <a href="https://x.com/K4KarolE_X">https://x.com/K4KarolE_X</a>
        <br>
        Instagram: <a href="https://www.instagram.com/k4karole">https://www.instagram.com/k4karole</a>
        """
        text_label.setText(text_label_content)