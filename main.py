'''
TERMINOLOGY
-----------
Apart from the Window Settings TABS (src / window_settings.py)
the TABS has been referred as paylists, playlist_all, playlist_index, ..

Playing playlist = playlist where the current track is in the playing or paused state
                     / playlist where the last track was played
Active playlist = playlist which is currently selected / displayed
'''

import sys

from PyQt6.QtWidgets import QApplication

from src import (
    br,
    AVPlayer,
    MyIcon,
    MyImage,
    MyPlaylists,
    MyQueueWindow,
    MySettingsWindow,
    MySlider,
    MyVolumeSlider,
    MyWindow,
    PlaysFunc,
    TrackDuration,
    logger_basic,
    generate_buttons,
    generate_ui
    )


def main():
    logger_basic('App start')
    app = QApplication(sys.argv)

    br.icon = MyIcon()
    br.window = MyWindow()
    br.av_player = AVPlayer()
    br.av_player_duration = TrackDuration()   
    br.play_slider = MySlider()
    br.image_logo = MyImage('logo.png', 200)
    br.play_funcs = PlaysFunc()
    generate_buttons()
    br.playlists_all = MyPlaylists()
    br.window_queue = MyQueueWindow()
    br.window_settings = MySettingsWindow()
    br.volume_slider = MyVolumeSlider()
    generate_ui()

    br.window.show()
    logger_basic('Window displayed')

    sys.exit(app.exec())


if __name__ == "__main__":
    main()