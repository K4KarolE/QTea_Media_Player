from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton

from .buttons import MyButtons
from .class_bridge import br
from .class_data import cv
from .func_coll import inactive_track_font_style


''' Please note, the "button_speaker" and the "duration_sum_widg"
    buttons do not appear as classic buttons on the UI   
'''


def generate_buttons():
    '''
    ########################
        PLAYLIST SECTION
    ########################
    '''
    PLIST_BUTTONS_WIDTH = 32
    cv.PLIST_BUTTONS_HEIGHT = 30 # +used: in playlist_buttons_list_wrapper
    PLIST_BUTTONS_X_DIFF = 4    # FOR SELECTING ADD AND REMOVE BUTTONS
    PLIST_BUTTONS_X_BASE = 0
    PLIST_BUTTONS_Y = 3

    def button_x_pos(num):
        return int(PLIST_BUTTONS_X_BASE + (PLIST_BUTTONS_WIDTH + 6) * num)


    ''' BUTTON PLAYLIST - ADD TRACK '''
    br.button_add_track = MyButtons(
        'AT',
        'Add Track'
        )
    br.button_add_track.setGeometry(button_x_pos(0), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_add_track.clicked.connect(br.button_add_track.button_add_track_clicked)


    ''' BUTTON PLAYLIST - ADD DIRECTORY '''
    br.button_add_dir = MyButtons(
        'AD',
        'Add Directory',
        )
    br.button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_add_dir.clicked.connect(lambda: br.button_add_dir.button_add_dir_clicked())   # logger decorator on func. -> lambda needed


    ''' BUTTON PLAYLIST - REMOVE TRACK '''
    br.button_remove_track = MyButtons(
        'RT',
        'Remove track'
        )
    br.button_remove_track.setGeometry(button_x_pos(2), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_remove_track.clicked.connect(br.button_remove_track.button_remove_single_track)


    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    br.button_remove_all_track = MyButtons(
        'CP',
        'Clear Playlist'
        )
    br.button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_remove_all_track.clicked.connect(br.button_remove_all_track.button_remove_all_track)


    ''' BUTTON PLAYLIST - QUEUE '''
    br.button_queue = MyButtons(
        'Q',
        'Queue and Search window',
        br.icon.queue
        )
    br.button_queue.setGeometry(button_x_pos(4.3), PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_queue.clicked.connect(lambda: br.window_queue_and_search.show())
    br.button_queue.setIconSize(QSize(15, 15))


    ''' BUTTON PLAYLIST - SETTINGS '''
    br.button_settings = MyButtons(
        'SE',
        'Settings window',
        br.icon.settings
        )
    br.button_settings.setGeometry(button_x_pos(5.3)-PLIST_BUTTONS_X_DIFF - 6, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH, cv.PLIST_BUTTONS_HEIGHT)
    br.button_settings.clicked.connect(lambda: br.button_settings.button_settings_clicked())


    ''' BUTTON PLAYLIST - Thumbnail '''
    br.button_thumbnail = MyButtons(
        'T',
        'Thumbnail View',
        br.icon.thumbnail
    )
    br.button_thumbnail.setGeometry(button_x_pos(6.0) - PLIST_BUTTONS_X_DIFF - 6, PLIST_BUTTONS_Y, PLIST_BUTTONS_WIDTH,
                                   cv.PLIST_BUTTONS_HEIGHT)
    br.button_thumbnail.clicked.connect(lambda: br.button_thumbnail.button_thumbnail_clicked())
    if not cv.is_ffmpeg_installed:
        br.button_thumbnail.setDisabled(True)
        br.button_thumbnail.setToolTip("Thumbnail View / Disabled / FFmpeg needs to be installed")


    ''' 
        PLAYLIST BUTTONS LIST
        used to add widgets to the layout
        apart from button_queue and button_settings:
        buttons style applied in the LAYOUTS section
    '''
    br.playlist_buttons_list = [
        br.button_add_track,
        br.button_add_dir,
        br.button_remove_track,
        br.button_remove_all_track,
        br.button_queue,
        br.button_settings,
        br.button_thumbnail
        ]
    

    ''' DURATION SUM INFO - Not used as a button '''
    br.duration_sum_widg = QPushButton('DURATION')
    br.duration_sum_widg.setDisabled(1)
    br.duration_sum_widg.setFont(inactive_track_font_style)
    if cv.os_linux:
        br.duration_sum_widg.setStyleSheet("color: black;")




    '''
    ####################
        PLAY SECTION
    ####################
    '''
    PLAY_BUTTONS_WIDTH = 32
    PLAY_BUTTONS_HEIGHT = 32

    def play_buttons_x_pos(num):
        return int((PLAY_BUTTONS_WIDTH) * num)


    ''' 
    BUTTON PLAY SECTION - PLAY/PAUSE
    The button`s icon update at startup is declared after
    the playlists creation in main(playlists_all = MyPlaylists(..))
    '''
    br.button_play_pause = MyButtons(
        'PLAY/PAUSE',
        'Start/stop playing',
        br.icon.start,
        )
    br.button_play_pause.clicked.connect(br.button_play_pause.button_play_pause_clicked)
    br.button_play_pause.setGeometry(0, 0, PLAY_BUTTONS_WIDTH+4, PLAY_BUTTONS_HEIGHT+4)
    br.button_play_pause.setIconSize(QSize(cv.icon_size + 5, cv.icon_size + 5))


    ''' BUTTON PLAY SECTION - STOP '''
    br.button_stop = MyButtons(
        'Stop',
        'Stop playing',
        br.icon.stop
        )
    br.button_stop.setGeometry(play_buttons_x_pos(1.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_stop.clicked.connect(br.button_stop.button_stop_clicked)
    br.button_stop.setIconSize(QSize(cv.icon_size, cv.icon_size))


    ''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
    br.button_prev_track = MyButtons(
        'Prev',
        'Previous track',
        br.icon.previous
        )
    br.button_prev_track.setGeometry(play_buttons_x_pos(2.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_prev_track.clicked.connect(br.button_prev_track.button_prev_track_clicked)


    ''' BUTTON PLAY SECTION - NEXT TRACK '''
    br.button_next_track = MyButtons(
        'Next',
        'Next track',
        br.icon.next
        )
    br.button_next_track.setGeometry(play_buttons_x_pos(3.5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_next_track.clicked.connect(br.button_next_track.button_next_track_clicked)


    ''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
    br.button_toggle_repeat_pl = MyButtons(
        'Tog Rep PL',
        'Toggle Repeat Playlist',
        br.icon.repeat
        )
    br.button_toggle_repeat_pl.setGeometry(play_buttons_x_pos(5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_toggle_repeat_pl.clicked.connect(br.button_toggle_repeat_pl.button_toggle_repeat_pl_clicked)

    if cv.repeat_playlist == 2:
        br.button_toggle_repeat_pl.setFlat(True)
    elif cv.repeat_playlist == 0:
        br.button_toggle_repeat_pl.setFlat(True)
        br.button_toggle_repeat_pl.setIcon(br.icon.repeat_single)


    ''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
    br.button_toggle_shuffle_pl = MyButtons(
        'Shuffle PL',
        'Toggle Shuffle Playlist',
        br.icon.shuffle
        )
    br.button_toggle_shuffle_pl.setGeometry(play_buttons_x_pos(6), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_toggle_shuffle_pl.clicked.connect(br.button_toggle_shuffle_pl.button_toggle_shuffle_pl_clicked)
    if cv.shuffle_playlist_on:
        br.button_toggle_shuffle_pl.setFlat(True)


    ''' BUTTON PLAY SECTION - TOGGLE PLAYLIST '''
    br.button_toggle_playlist = MyButtons(
        'Shuffle PL',
        'Toggle Show Playlists',
        br.icon.toggle_playlist
        )
    br.button_toggle_playlist.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_toggle_playlist.clicked.connect(br.button_toggle_playlist.button_toggle_playlist_clicked)


    ''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
    br.button_toggle_video = MyButtons(
        'Shuffle PL',
        'Toggle Show Video Window',
        br.icon.toggle_video
        )
    br.button_toggle_video.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
    br.button_toggle_video.clicked.connect(br.button_toggle_video.button_toggle_video_clicked)


    ''' BUTTON PLAY SECTION - DURATION INFO '''
    def button_duration_info_clicked():
        """ 01:22 / 03:43 <--> -02:21 / 03:43 """
        if cv.track_full_duration_to_display:
            if cv.is_duration_to_display_straight:
                cv.is_duration_to_display_straight = False
                br.button_duration_info.setText(cv.duration_to_display_back)
            else:
                cv.is_duration_to_display_straight = True
                br.button_duration_info.setText(cv.duration_to_display_straight)
            
            br.button_duration_info.adjustSize()

    br.button_duration_info = MyButtons(
        '00:00 / 00:00',
        'Click to switch',
        )
    br.button_duration_info.move(play_buttons_x_pos(9.5), 0)
    br.button_duration_info.clicked.connect(button_duration_info_clicked)
    br.button_duration_info.set_style_duration_info_button()


    ''' 
        PLAY BUTTONS LIST
        used to add widgets to the layout
        the speaker/mute button is not
        part of the list
    '''
    br.play_buttons_list = [
        br.button_play_pause,
        br.button_stop,
        br.button_prev_track,
        br.button_next_track,
        br.button_toggle_repeat_pl,
        br.button_toggle_shuffle_pl,
        br.button_toggle_playlist,
        br.button_toggle_video,
        br.button_duration_info
        ]



    ''' BUTTON PLAY SECTION - SPEAKER/MUTE '''
    br.button_speaker = MyButtons(
        'Speaker',
        'Toggle Mute',
        icon = br.icon.speaker
        )
    br.button_speaker.setFlat(True)
    br.button_speaker.clicked.connect(br.button_speaker.button_speaker_clicked)
    if cv.is_speaker_muted:
        br.button_speaker.setIcon(br.icon.speaker_muted)
        br.av_player.audio_output.setVolume(0)