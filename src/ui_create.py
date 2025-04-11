from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QSplitter,
    QVBoxLayout
    )

from .class_bridge import br
from .class_data import cv


''' 
######################
        LAYOUTS                          
######################

LEARNED:
1,              
    Do not mix widgets and layouts in a layout
    Hiding the widget --> layout disapears too
2,
    Layout add to QFrame --> hiding QFrame hides the layout
    Not able to hide Layout by itself
3,
    Alignment should be in the widget
    Not in the Layout -->
    Made the av_player.video_output invisible

GUIDE:

  BASE
    LEFT      RIGHT  
    -----------------
    |       ||       |
    |       || PLIST |  TOP
    |  VID  ||_______|  
    |_______||___|___|
    |________________|  BOTTOM
    |________|_______|  
'''

def generate_ui():
    layout_base = QVBoxLayout(br.window)
    layout_base.setContentsMargins(0, 0, 0, 0)

    layout_hor_top = QHBoxLayout()
    layout_hor_top.setSpacing(0)

    layout_bottom_slider = QVBoxLayout()
    layout_bottom_slider.setContentsMargins(9, 0, 9, 0)

    layout_bottom_wrapper = QHBoxLayout()
    layout_bottom_wrapper.setContentsMargins(9, 0, 9, 0)

    layout_base.addLayout(layout_hor_top, 90)
    layout_base.addLayout(layout_bottom_slider, 5)
    layout_base.addLayout(layout_bottom_wrapper, 5)


    ''' SPLITTER - LEFT / RIGHT'''
    splitter_left_right = QSplitter(Qt.Orientation.Horizontal)
    layout_hor_top.addWidget(splitter_left_right)


    ''' TOP LEFT - VIDEO / QTEA LOGO '''
    layout_vert_left = QVBoxLayout() # here layout type is not relevant
    layout_vert_left.setContentsMargins(0, 0, 0, 0)
    br.layout_vert_left_qframe = QFrame()
    br.layout_vert_left_qframe.setLayout(layout_vert_left)

    ''' TOP RIGHT - PLAYLIST / BUTTONS / DURATION '''
    layout_vert_right = QVBoxLayout() # here layout type is not relevant
    layout_vert_right.setContentsMargins(5, 0, 4, 0)
    br.layout_vert_right_qframe = QFrame()
    br.layout_vert_right_qframe.setLayout(layout_vert_right)
    br.layout_vert_right_qframe.setMinimumWidth(cv.window_min_width-200)


    splitter_left_right.addWidget(br.layout_vert_left_qframe)
    splitter_left_right.addWidget(br.layout_vert_right_qframe)
    splitter_left_right.setStretchFactor(0, 3)
    splitter_left_right.setStretchFactor(1, 1)



    ''' TOP RIGHT 
    _____________
    |           |
    |   PLIST   |
    |___________|
    |_BU__|__DU_|

    '''

    # PLAYLIST
    layout_playlist = QVBoxLayout()
    layout_vert_right.addLayout(layout_playlist)

    # UNDER PLAYLIST
    layout_under_playlist_wrapper = QHBoxLayout()
    layout_under_playlist_wrapper.setContentsMargins(5, 0, 18, 0)

    layout_under_playlist_buttons = QHBoxLayout()

    layout_under_playlist_duration = QVBoxLayout()
    layout_under_playlist_duration.setAlignment(Qt.AlignmentFlag.AlignRight)

    layout_under_playlist_wrapper.addLayout(layout_under_playlist_buttons)
    layout_under_playlist_wrapper.addLayout(layout_under_playlist_duration)

    layout_vert_right.addLayout(layout_under_playlist_wrapper)


    ''' ADDING WIDGETS'''
    ''' TOP LEFT '''
    layout_vert_left.addWidget(br.av_player.video_output)
    br.av_player.video_output.hide()
    layout_vert_left.addWidget(br.image_logo)


    ''' TOP RIGHT '''
    # BUTTONS
    playlist_buttons_list_wrapper = QFrame()
    playlist_buttons_list_wrapper.setFixedSize(250, cv.PLIST_BUTTONS_HEIGHT+5)

    for button in br.playlist_buttons_list:
        button.setParent(playlist_buttons_list_wrapper)
        if button not in [br.button_settings, br.button_queue, br.button_thumbnail]:
            button.set_style_playlist_buttons()

    layout_under_playlist_buttons.addWidget(playlist_buttons_list_wrapper)

    # DURATION
    layout_under_playlist_duration.addWidget(br.duration_sum_widg)


    ''' PLAYLISTS '''
    layout_playlist.addWidget(br.playlists_all)


    ''' PLAY BUTTON ICON UPDATE '''
    if cv.play_at_startup and cv.active_pl_tracks_count > 0:
        br.button_play_pause.setIcon(br.icon.pause)


    ''' BOTTOM '''
    # SLIDER
    layout_bottom_slider.addWidget(br.play_slider)

    # LAYOUT BUTTONS / VOLUME
    layout_bottom_buttons = QVBoxLayout()
    layout_bottom_volume = QHBoxLayout()
    layout_bottom_volume.setAlignment(Qt.AlignmentFlag.AlignTop)

    layout_bottom_wrapper.addLayout(layout_bottom_buttons, 80)
    layout_bottom_wrapper.addLayout(layout_bottom_volume, 20)


    # BUTTONS WRAPPER
    play_buttons_list_wrapper= QFrame()
    play_buttons_list_wrapper.setFixedHeight(50)
    for button in br.play_buttons_list:
        button.setParent(play_buttons_list_wrapper)

    layout_bottom_buttons.addWidget(play_buttons_list_wrapper)
    layout_bottom_volume.addWidget(br.button_speaker, alignment=Qt.AlignmentFlag.AlignRight)
    layout_bottom_volume.addWidget(br.volume_slider)