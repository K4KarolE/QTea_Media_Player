import sys

from src import (
    br,
    AVPlayer,
    MyApp,
    MyIcon,
    MyImage,
    MyPlaylists,
    MyQueueAndSearchWindow,
    MySlider,
    MyVolumeSlider,
    MyWindow,
    PlaysFunc,
    TrackDuration,
    generate_buttons,
    generate_ui,
    logger_sum
    )


def main():
    logger_sum('App started')

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
    br.volume_slider = MyVolumeSlider()
    generate_ui()
    br.window.show()

    sys.exit(br.app.exec())


if __name__ == "__main__":
    main()