
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QFileDialog, QPushButton, QMainWindow
from PyQt6.QtWidgets import QFrame, QTabWidget, QScrollBar
from PyQt6.QtCore import QUrl, Qt, QEvent
from PyQt6.QtGui import QIcon, QFont

# from PyQt6.QtWidgets import QLineEdit, QLabel
# from PyQt6.QtCore import QSize, QTimer, QTime
import os
import sys
import random


from src import (
    active_utility,
    save_last_track_index,
    remove_record_db,
    get_path_db,
    get_duration_db,
    generate_track_list_detail,
    add_record_grouped_actions,
    add_new_list_item,
    cv, # data
    cur, # db
    connection, # db
    settings,   # json dic
    PATH_JSON_SETTINGS,
    inactive_track_font_style,  
    active_track_font_style,
    )
from src import Path
from src import AVPlayer, TrackDuration, MySlider
from src import save_json



''' APP '''
class MyApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
        self.installEventFilter(self) 

    def eventFilter(self, source, event):
        to_save_settings = False
        # PAUSE/PLAY - IF PLAYER IS NOT FULL SCREEN
        # IF FULL SCREEN: SET UP IN 'AVPlayer class'
        if event.type() == QEvent.Type.KeyRelease:
            # PAUSE
            if event.key() == Qt.Key.Key_Space:
                button_play_pause_clicked()
            # VOLUME
            elif event.key() == Qt.Key.Key_Plus:
                new_volume = round(av_player.audio_output.volume() + 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            elif event.key() == Qt.Key.Key_Minus:
                new_volume = round(av_player.audio_output.volume() - 0.01, 4)
                av_player.audio_output.setVolume(new_volume)
                to_save_settings = True
            # JUMP - SMALL
            elif event.key() == Qt.Key.Key_Left:
                av_player.player.setPosition(av_player.player.position() - 600)
            elif event.key() == Qt.Key.Key_Right:
                av_player.player.setPosition(av_player.player.position() + 600)
        if to_save_settings:
            settings['volume'] = new_volume
            save_json(settings, PATH_JSON_SETTINGS)
        return super().eventFilter(source, event)
    

''' APP '''
app = MyApp()

''' WINDOW '''
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 750
window = QWidget()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.setMinimumSize(400, 400)
window.setWindowIcon(QIcon(str(Path(Path(__file__).parent, 'skins/window_icon.png'))))
window.setWindowTitle("QTea media player")


''' PLAYER '''
av_player = AVPlayer(volume=cv.volume)

""" 
    av_player_duration
    -------------------
    only used for duration calculation -->
    able to add new track(s) without interrupting 
    the playing (av_player)
"""
av_player_duration = TrackDuration()   


''' 
#######################
        WINDOWS              
#######################
'''
# FOR BUTTONS: ADD TRACK, REMOVE TRACK, ..
under_playlist_window = QMainWindow()
under_playlist_window.setMinimumSize(400, 30)

# FOR BUTTONS: PLAY/STOP, PAUSE, ..
under_play_slider_window = QMainWindow()
under_play_slider_window.setFixedHeight(50)
under_play_slider_window.setMinimumSize(400, 50)


''' 
#######################
        BUTTONS              
#######################
'''
MEDIA_FILES = "Media files (*.mp3 *.wav *.flac *.midi *.aac *.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
AUDIO_FILES = "Audio files (*.mp3 *.wav *.flac *.midi *.aac)"
VIDEO_FILES = "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpg)"
FILE_TYPES_LIST = [MEDIA_FILES, AUDIO_FILES, VIDEO_FILES, 'All Files']

''' 
    PLAYLIST SECTION
'''
PLIST_BUTTONS_WIDTH = 32
PLIST_BUTTONS_HEIGHT = 30
PLIST_BUTTONS_X_DIFF = 4    # FOR SELECTING ADD AND REMOVE BUTTONS

def button_x_pos(num):
    return (PLIST_BUTTONS_WIDTH + 5) * num

''' BUTTON PLAYLIST - ADD TRACK '''
def button_add_track_clicked():
    dialog_add_track = QFileDialog()
    dialog_add_track.setWindowTitle("Select a media file")
    dialog_add_track.setNameFilters(FILE_TYPES_LIST)
    dialog_add_track.exec()
    if dialog_add_track.result():
        add_record_grouped_actions(dialog_add_track.selectedFiles()[0], av_player_duration)

button_add_track = QPushButton(under_playlist_window, text='AT')
button_add_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_track.setToolTip('Add track')
button_add_track.setToolTipDuration(2000)
button_add_track.setFont(QFont('Times', 10, 600))
button_add_track.setGeometry(5, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_track.clicked.connect(button_add_track_clicked)


''' BUTTON PLAYLIST - ADD DIRECTORY '''
def button_add_dir_clicked():
    track_path_list = []
    error_path_list = []
    dialog_add_dir = QFileDialog()
    dialog_add_dir.setWindowTitle("Select a directory")
    dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
    dialog_add_dir.exec()
    if dialog_add_dir.result():
        for dir_path, dir_names, file_names in os.walk(dialog_add_dir.selectedFiles()[0]):
            for file in file_names:
                if file[-4:] in MEDIA_FILES:
                    track_path_list.append(Path(dir_path, file))
        if len(track_path_list) > 0:
            for track_path in track_path_list:
                try:
                    add_record_grouped_actions(track_path, av_player_duration)
                except:
                    error_path_list.append(track_path)
            if error_path_list:
                for item in error_path_list:
                    print(f'ERROR - {item}')

button_add_dir = QPushButton(under_playlist_window, text='AD')
button_add_dir.setCursor(Qt.CursorShape.PointingHandCursor)
button_add_dir.setToolTip('Add directory')
button_add_dir.setToolTipDuration(2000)
button_add_dir.setFont(QFont('Times', 10, 600))
button_add_dir.setGeometry(button_x_pos(1)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_add_dir.clicked.connect(button_add_dir_clicked)



''' BUTTON PLAYLIST - REMOVE TRACK '''
def button_remove_track_clicked():
    # LAST TRACK INDEX
    if  cv.active_playlist.currentRow() < cv.last_track_index:
        cv.last_track_index = cv.last_track_index - 1
        settings[cv.active_db_table]['last_track_index'] = cv.last_track_index
        save_json(settings, PATH_JSON_SETTINGS)
    # DB
    row_id_db = cv.active_playlist.currentRow() + 1
    remove_record_db(row_id_db)
    # PLAYLIST
    cv.active_playlist.takeItem(cv.active_playlist.currentRow())
    cv.active_pl_duration.takeItem(cv.active_playlist.currentRow())
    rename_playlist(row_id_db)



def rename_playlist(row_id_db):
    cur.execute("SELECT * FROM {0} WHERE row_id >= ?".format(cv.active_db_table), (row_id_db,))
    playlist = cur.fetchall()
    for item in playlist:
        list_name, duration = generate_track_list_detail(item)
        cv.active_playlist.item(row_id_db-1).setText(list_name)
        row_id_db +=1

button_remove_track = QPushButton(under_playlist_window, text='RT')
button_remove_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_track.setToolTip('Remove track')
button_remove_track.setToolTipDuration(2000)
button_remove_track.setFont(QFont('Times', 10, 600))
button_remove_track.setGeometry(button_x_pos(2), 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_track.clicked.connect(button_remove_track_clicked)

''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
def button_remove_all_track_clicked():
    # DB
    cur.execute("DELETE FROM {0}".format(cv.active_db_table))
    connection.commit()
    # PLAYLIST
    cv.active_playlist.clear()
    cv.active_pl_duration.clear()

button_remove_all_track = QPushButton(under_playlist_window, text='CP')
button_remove_all_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_remove_all_track.setToolTip('Clear Playlist')
button_remove_all_track.setToolTipDuration(2000)
button_remove_all_track.setFont(QFont('Times', 10, 600))
button_remove_all_track.setGeometry(button_x_pos(3)-PLIST_BUTTONS_X_DIFF, 0, PLIST_BUTTONS_WIDTH, PLIST_BUTTONS_HEIGHT)
button_remove_all_track.clicked.connect(button_remove_all_track_clicked)


''' 
    PLAY SECTION
'''
PLAY_BUTTONS_WIDTH = 60
PLAY_BUTTONS_HEIGHT = 30

def play_buttons_x_pos(num):
    return (PLAY_BUTTONS_WIDTH + 3) * num


''' BUTTON PLAY SECTION - PLAY / PAUSE '''
def button_play_pause_clicked():

    if av_player.played_row == None:
        play_track()
    elif av_player.player.isPlaying():
        av_player.player.pause()
        av_player.paused = True
    elif av_player.paused:
        av_player.player.play()
        av_player.paused = False
    elif not av_player.player.isPlaying() and not av_player.paused:
        play_track()

button_play_pause = QPushButton(under_play_slider_window, text='PLAY/PAUSE')
button_play_pause.setCursor(Qt.CursorShape.PointingHandCursor)
button_play_pause.setFont(QFont('Times', 10, 600))
button_play_pause.clicked.connect(button_play_pause_clicked)


''' BUTTON PLAY SECTION - STOP '''
def button_stop_clicked():
    av_player.player.stop()
    av_player.paused = False
 
button_stop = QPushButton(under_play_slider_window, text='Stop')
button_stop.setCursor(Qt.CursorShape.PointingHandCursor)
button_stop.setFont(QFont('Times', 10, 600))
button_stop.setGeometry(play_buttons_x_pos(2), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_stop.clicked.connect(button_stop_clicked)


''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
def button_prev_track_clicked():
    if cv.active_playlist.count() > 0 and av_player.played_row != None:

        if cv.shuffle_playlist_on:
            cv.active_playlist.setCurrentRow(cv.last_track_index)
        elif cv.active_playlist.currentRow() != 0:
            cv.active_playlist.setCurrentRow(av_player.played_row - 1)
        else:
            cv.active_playlist.setCurrentRow(cv.active_playlist.count() - 1)
        play_track()

button_prev_track = QPushButton(under_play_slider_window, text='Prev')
button_prev_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_prev_track.setFont(QFont('Times', 10, 600))
button_prev_track.setGeometry(play_buttons_x_pos(3), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_prev_track.clicked.connect(button_prev_track_clicked)


''' BUTTON PLAY SECTION - NEXT TRACK '''
def button_next_track_clicked():
    if cv.active_playlist.count() > 0 and av_player.played_row != None:
        play_next_track()

button_next_track = QPushButton(under_play_slider_window, text='Next')
button_next_track.setCursor(Qt.CursorShape.PointingHandCursor)
button_next_track.setFont(QFont('Times', 10, 600))
button_next_track.setGeometry(play_buttons_x_pos(4), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_next_track.clicked.connect(button_next_track_clicked)


''' BUTTON PLAY SECTION - TOGGLE PLAYLIST '''
def button_toggle_playlist_clicked():

    if av_player.playlist_visible and av_player.video_area_visible:
        layout_vert_right_qframe.hide()
        layout_vert_middle_qframe.hide()
        av_player.playlist_visible = False
        button_toggle_video.setDisabled(1)
    else:
        layout_vert_right_qframe.show()
        layout_vert_middle_qframe.show()
        av_player.playlist_visible = True
        button_toggle_video.setDisabled(0)    
    
button_toggle_playlist = QPushButton(under_play_slider_window, text='Tog PL')
button_toggle_playlist.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_playlist.setFont(QFont('Times', 10, 600))
button_toggle_playlist.setGeometry(play_buttons_x_pos(5), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_playlist.clicked.connect(button_toggle_playlist_clicked)


''' BUTTON PLAY SECTION - TOGGLE VIDEO '''
def button_toggle_video_clicked():
    
    if av_player.playlist_visible and av_player.video_area_visible:
        layout_vert_left_qframe.hide()
        av_player.video_area_visible = False
        window.resize(int(WINDOW_WIDTH/3), window.geometry().height())
        button_toggle_playlist.setDisabled(1)
    else:
        window.resize(WINDOW_WIDTH, window.geometry().height())
        layout_vert_left_qframe.show()
        av_player.video_area_visible = True
        button_toggle_playlist.setDisabled(0)
    
button_toggle_video = QPushButton(under_play_slider_window, text='Tog Vid')
button_toggle_video.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_video.setFont(QFont('Times', 10, 600))
button_toggle_video.setGeometry(play_buttons_x_pos(6), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_video.clicked.connect(button_toggle_video_clicked)


''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
def button_toggle_repeat_pl_clicked():
    if cv.repeat_playlist_on:
        cv.repeat_playlist_on = False
        button_toggle_repeat_pl.setFlat(0)
    else:
        cv.repeat_playlist_on = True
        button_toggle_repeat_pl.setFlat(1)
    
    settings['repeat_playlist_on'] = cv.repeat_playlist_on
    save_json(settings, PATH_JSON_SETTINGS)
    
button_toggle_repeat_pl = QPushButton(under_play_slider_window, text='Tog Rep')
button_toggle_repeat_pl.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_repeat_pl.setFont(QFont('Times', 10, 600))
button_toggle_repeat_pl.setGeometry(play_buttons_x_pos(7), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_repeat_pl.clicked.connect(button_toggle_repeat_pl_clicked)


''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
def button_toggle_shuffle_pl_clicked():
    if cv.shuffle_playlist_on:
        cv.shuffle_playlist_on = False
        button_toggle_shuffle_pl.setFlat(0)
    else:
        cv.shuffle_playlist_on = True
        button_toggle_shuffle_pl.setFlat(1)
    
    settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
    save_json(settings, PATH_JSON_SETTINGS)
    
button_toggle_shuffle_pl = QPushButton(under_play_slider_window, text='Shu Rep')
button_toggle_shuffle_pl.setCursor(Qt.CursorShape.PointingHandCursor)
button_toggle_shuffle_pl.setFont(QFont('Times', 10, 600))
button_toggle_shuffle_pl.setGeometry(play_buttons_x_pos(8), 0, PLAY_BUTTONS_WIDTH, PLAY_BUTTONS_HEIGHT)
button_toggle_shuffle_pl.clicked.connect(button_toggle_shuffle_pl_clicked)


''' LIST ACTIONS '''
def play_track():
    
    try:  
        # FONT STYLE - PREV/NEW TRACK
        if av_player.played_row != None:

            try:
                cv.active_playlist.item(cv.last_track_index).setFont(inactive_track_font_style)
            except:
                print(f'ERROR in row: {cv.last_track_index}\n\n')

            cv.last_track_index = av_player.played_row

        cv.active_playlist.currentItem().setFont(active_track_font_style)
        save_last_track_index()
        # PATH / DURATION / SLIDER
        track_path = get_path_db()
        track_duration = get_duration_db()
        play_slider.setMaximum(track_duration)
        # PLAYER
        av_player.player.setSource(QUrl.fromLocalFile(str(Path(track_path))))
        av_player.player.play()
        # COUNTER
        av_player.played_row = cv.active_playlist.currentRow()
        # WINDOW TITLE
        window.setWindowTitle(f'{Path(track_path).stem} - QTea media player')

    except:
        play_next_track()


def play_next_track():
    # SHUFFLE
    if cv.shuffle_playlist_on and cv.active_playlist.count() > 1:
        next_track_index = random.randint(0, cv.active_playlist.count()-1)
        while next_track_index == cv.active_playlist.currentRow():
            next_track_index = random.randint(0, cv.active_playlist.count()-1)
        cv.active_playlist.setCurrentRow(next_track_index)
        play_track()
    # MORE TRACKS IN THE PLAYLIST
    elif cv.active_playlist.count() != cv.active_playlist.currentRow() + 1:
        cv.active_playlist.setCurrentRow(av_player.played_row + 1)
        play_track()
    # PLAYING THE LAST TRACK    
    elif (cv.active_playlist.count() == cv.active_playlist.currentRow() + 1 and
        cv.repeat_playlist_on):
            cv.active_playlist.setCurrentRow(0)
            play_track()
    # CURRENT TRACK BACK TO START         
    else:
        av_player.player.setPosition(0)


def auto_play_next_track():
    if av_player.base_played:   # avoiding the dummy song played when the class created
        if av_player.player.mediaStatus() == av_player.player.MediaStatus.EndOfMedia:

            play_next_track()
    else:
        av_player.base_played = True    
av_player.player.mediaStatusChanged.connect(auto_play_next_track)




''' 
######################
        SLIDER                          
######################
'''
play_slider = MySlider(av_player)



''' 
######################
        LAYOUTS                          
######################

LEARNED:
1,              
do not mix widgets and layouts in a layout
hiding the widget --> layout disapears too
2,
layout add to QFrame --> hiding QFrame hides the layout


GUIDE:

  BASE
    LEFT      RIGHT  
    -----------------
    |       ||       |
    |       || PLIST |  TOP
    |  VID  ||_______|  
    |_______||_______|
    |________________|  BOTTOM
    |________________|  
'''


layout_base = QVBoxLayout(window)
layout_base.setContentsMargins(0, 0, 0, 0)

layout_hor_top = QHBoxLayout()
layout_hor_top.setSpacing(0)
layout_ver_bottom = QVBoxLayout()
layout_ver_bottom.setContentsMargins(10, 0, 10, 0)

layout_base.addLayout(layout_hor_top, 90)
layout_base.addLayout(layout_ver_bottom, 10)


''' TABS - PLAYLIST '''
# TO AVOID THE tabs_playlist.currentChanged.connect(active_tab) SIGNAL
# TRIGGERED WHEN TAB ADDED TO tabs_playlist
tabs_created_at_first_run = False

def active_tab():
    if tabs_created_at_first_run:
        cv.active_tab = tabs_playlist.currentIndex()
        settings['last_used_tab'] = cv.active_tab
        save_json(settings, PATH_JSON_SETTINGS)
        active_utility()    # set the current lists(name, duration)

tabs_playlist = QTabWidget()
tabs_playlist.setFont(QFont('Times', 10, 500))
tabs_playlist.currentChanged.connect(active_tab)



'''
    CREATING FRAME, LAYOUT, LIST WIDGETS 
    LOADING TRACKS
'''
def name_list_to_duration_row_selection():
    cv.active_pl_duration.setCurrentRow(cv.active_playlist.currentRow())
    cv.active_pl_duration.setStyleSheet(
                        "QListWidget::item:selected"
                            "{"
                            "background: #CCE8FF;"
                            "color: red;"   # font
                            "}"
                        )

def duration_list_to_name_row_selection():
    cv.active_playlist.setCurrentRow(cv.active_pl_duration.currentRow())
    cv.active_playlist.setStyleSheet(
                        "QListWidget::item:selected"
                            "{"
                            "background: #CCE8FF;"
                            "color: red;"   # font
                            "}"
                        )

for pl in cv.paylist_widget_dic:
    if settings[pl]['tab_index'] != None:
        
        scroll_bar_name_ver = QScrollBar()
        scroll_bar_name_hor = QScrollBar()
        scroll_bar_duration_ver = QScrollBar()
        scroll_bar_duration_hor = QScrollBar()

        scroll_bar_name_ver.valueChanged.connect(scroll_bar_duration_ver.setValue)
        scroll_bar_duration_ver.valueChanged.connect(scroll_bar_name_ver.setValue)

        scroll_bar_name_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        scroll_bar_name_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
        
        scroll_bar_duration_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"               
                        )
        
        scroll_bar_duration_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
    
        cv.paylist_widget_dic[pl]['name_list_widget'] = QListWidget()
        cv.paylist_widget_dic[pl]['name_list_widget'].setVerticalScrollBar(scroll_bar_name_ver)
        cv.paylist_widget_dic[pl]['name_list_widget'].setHorizontalScrollBar(scroll_bar_name_hor)
        # cv.paylist_widget_dic[pl]['name_list_widget'].setAlternatingRowColors(True)
        cv.paylist_widget_dic[pl]['name_list_widget'].currentItemChanged.connect(name_list_to_duration_row_selection)

        cv.paylist_widget_dic[pl]['duration_list_widget'] = QListWidget()
        cv.paylist_widget_dic[pl]['duration_list_widget'].setVerticalScrollBar(scroll_bar_duration_ver)
        cv.paylist_widget_dic[pl]['duration_list_widget'].setHorizontalScrollBar(scroll_bar_duration_hor)
        # cv.paylist_widget_dic[pl]['duration_list_widget'].setAlternatingRowColors(True)
        cv.paylist_widget_dic[pl]['duration_list_widget'].setFixedWidth(70)
        cv.paylist_widget_dic[pl]['duration_list_widget'].currentItemChanged.connect(duration_list_to_name_row_selection)

        name_list_widget = cv.paylist_widget_dic[pl]['name_list_widget']
        name_list_widget.itemDoubleClicked.connect(play_track)
        duration_list_widget = cv.paylist_widget_dic[pl]['duration_list_widget']
        tab_title = settings[pl]['tab_title']
        

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(name_list_widget, 90)
        layout.addWidget(duration_list_widget, 10)

        frame = QFrame()
        frame.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame.setLayout(layout)

        tabs_playlist.addTab(frame, tab_title)

        ''' PLAYLIST DB --> LIST WIDGET '''
        cur.execute("SELECT * FROM {0}".format(pl))
        playlist = cur.fetchall()
        for item in playlist:
            track_name, duration = generate_track_list_detail(item)
            add_new_list_item(track_name, name_list_widget, 'left')
            add_new_list_item(duration, duration_list_widget, 'right')

    tabs_created_at_first_run = True 


# LOAD ACTIVE NAME and DURATION LIST WIDGETS
active_utility()
# SET THE LAST USED TAB ACTIVE
tabs_playlist.setCurrentIndex(cv.active_tab)
# SET LAST PLAYED TRACK
cv.active_playlist.setCurrentRow(cv.last_track_index)


''' TOP RIGHT '''
layout_vert_right = QVBoxLayout()
layout_vert_right.setContentsMargins(5, 0, 4, 0)
layout_vert_right_qframe = QFrame()
layout_vert_right_qframe.setLayout(layout_vert_right)

''' TOP LEFT '''
layout_vert_left = QVBoxLayout()
layout_vert_left.setContentsMargins(0, 0, 0, 0)
layout_vert_left_qframe = QFrame()
layout_vert_left_qframe.setLayout(layout_vert_left)

''' TOP MIDDLE '''
layout_vert_middle_qframe = QFrame()


layout_hor_top.addWidget(layout_vert_left_qframe, 65)
layout_hor_top.addWidget(layout_vert_middle_qframe, 0)
layout_hor_top.addWidget(layout_vert_right_qframe, 35)


''' ADDING WIDGETS TO LAYOUTS '''
layout_vert_left.addWidget(av_player.video_output)
layout_vert_right.addWidget(tabs_playlist, 95)
layout_vert_right.addWidget(under_playlist_window, 5)
layout_ver_bottom.addWidget(play_slider)
layout_ver_bottom.addWidget(under_play_slider_window)

# TODO: if music playing pic displayed? / av_player.video_output.hide()
# TODO: add/edit tabs, tabs_playlist.setTabVisible(2, 0)

window.show()

sys.exit(app.exec())