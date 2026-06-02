"""
    To understand how can we mimic the playlists creation in the media player with
    empty playlists/tabs and fill it later with some content

    So we can optimize the startup time by:
    > create an empty tab for all the playlists but fill the content only for the last used playlist
    which will be displayed at startup and fill the rest if the playlists after the app is running
    >> faster start time
    >> it will make the start time playlists' amount independent
"""

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QTabWidget,
    QWidget, QFrame, QHBoxLayout,
)

import sys

''' APP '''
app = QApplication(sys.argv)


''' MAIN WINDOW '''
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 300
window_main = QWidget()
window_main.setGeometry(400, 400, WINDOW_WIDTH, WINDOW_HEIGHT)


""" Add empty tabs with the shell QFrame to the QTabWidget """
tabs_number = 5
tabs_qframe_dic = {}
tab_widget = QTabWidget()
for _ in range(tabs_number):
    tabs_qframe_dic[_] = QFrame()
    tab_widget.addTab(tabs_qframe_dic[_], f'Test - {_}')
tab_widget.setGeometry(20, 50, WINDOW_WIDTH-50, WINDOW_HEIGHT-70)


'''
    BUTTON
    Fill the empty tabs with dummy content after the main window creation
'''
button = QPushButton("Add content to the tabs", window_main)
button.setGeometry(20,10,250,30)
button.clicked.connect(lambda: tab_widget_action())

def tab_widget_action():
    for _ in  tabs_qframe_dic:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 0, 30, 0)
        layout.addWidget(QLabel('Left widget'), 84)
        layout.addWidget(QLabel('Right widget'), 6)
        tabs_qframe_dic[_].setLayout(layout)


''' MAIN WINDOW <-- TAB WIDGET '''
tab_widget.setParent(window_main)

window_main.show()

sys.exit(app.exec())