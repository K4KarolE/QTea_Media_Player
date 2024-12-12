import sys

from src import (
    br,
    AVPlayer,
    MyApp,
    MyIcon,
    MyImage,
    MyPlaylists,
    MyQueueAndSearchWindow,
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
    logger_basic('App started')
    br.app = MyApp(sys.argv)

    br.icon = MyIcon()
    br.window = MyWindow()
    br.av_player = AVPlayer()
    br.av_player_duration = TrackDuration()   
    br.play_slider = MySlider()
    br.image_logo = MyImage('logo.png', 200)
    br.play_funcs = PlaysFunc()
    generate_buttons()
    br.playlists_all = MyPlaylists()
    br.window_queue_and_search = MyQueueAndSearchWindow()
    br.window_settings = MySettingsWindow()
    br.volume_slider = MyVolumeSlider()
    generate_ui()

    br.window.show()
    logger_basic('Window displayed')

    sys.exit(br.app.exec())


if __name__ == "__main__":
    main()