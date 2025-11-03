''' 
SETTINGS WINDOW displayed once the settings button
(cog icon) clicked under the playlists section

TERMINOLOGY
In the rest of the files the TABS(Playlists) has been referred as playlists, playlist_all, playlist_index, ..
In this file the TAB terminology is kept for the SETTINGS WINDOW tabs
'''
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QScrollBar,
    QTabWidget,
    QWidget
    )

from .class_bridge import br
from .class_data import (
    cv,
    settings,
    save_json
    )
from .func_coll import inactive_track_font_style, move_window_to_middle_of_current_screen
from .message_box import MyMessageBoxError
from .func_thumbnail import (
    msg_box_wrapper_for_remove_all_thumbnails_and_clear_history,
    switch_all_pl_to_standard_from_thumbnails_view
    )
from .logger import logger_runtime


class ButtonJumpToPlaylist(QPushButton):
    """ Used in the Settings Window / Playlists tab
        Class to be able to assign different actions
        through the buttons creation iteration
    """
    def __init__(self, parent, playlist_index):
        super().__init__()
        self.setParent(parent)
        self.playlist_index = playlist_index
        self.setText('>')
        self.setToolTip('Jump to playlist')
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.button_action)
        self.setStyleSheet("QPushButton"
                           "{"
                            "border: 1px solid #C2C2C2;"
                            "border-radius: 4px;"
                            "}"
                           "QPushButton::pressed"
                            "{"
                            "background-color: #C2C2C2;"
                            "}"
                           )

    def button_action(self):
        br.playlists_all.setCurrentIndex(self.playlist_index)


@logger_runtime
class MySettingsWindow(QWidget):
    """ No logging at startup
        It is created once the Settings button clicked
    """
    def __init__(self):
        super().__init__()

        '''
        ##############
            WINDOW          
        ##############
        '''
        WINDOW_WIDTH, WINDOW_HEIGHT = 400, 630
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.setWindowIcon(br.icon.settings)
        self.setWindowTitle("Settings")


        '''
        ############
            TABS         
        ############
        '''
        TABS_POS_X, TABS_POS_Y  = 12, 12
        EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y = 20

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Verdana', 10, 500))
        tabs.resize(WINDOW_WIDTH-TABS_POS_X*2, int(WINDOW_HEIGHT-TABS_POS_Y*5.5))
        tabs.move(TABS_POS_X, TABS_POS_Y)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background-color: #287DCC;" 
                            "color: white;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        "QTabBar::tab:!selected"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.3 white, stop: 0.8 #C9C9C9, stop: 1 #C2C2C2);"
                            "color: black;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        # border set up @ QScrollArea
                        "QTabWidget::pane"
                            "{" 
                            "position: absolute;"
                            "top: 0.3em;"
                            "}"
                        )

        tab_playlist_scroll_area = QScrollArea()
        tab_general_scroll_area = QScrollArea()
        tab_hotkey_scroll_area = QScrollArea()

        tab_playlist = QWidget()
        tab_general = QWidget()
        tab_hotkey = QWidget()


        LINE_EDIT_TEXT_ALIGNMENT = (Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        LINE_EDIT_HIGHT = 20
        WIDGETS_POS_X=25
        WIDGETS_POS_Y=20
        WIDGETS_NEXT_LINE_POS_Y_DIFF = 25


        def get_dic_values_before_widget_creation(dic_value):
            item_text = dic_value['text']
            item_value = dic_value['value']
            return item_text, item_value

        def get_dic_values_after_widget_creation(dic_value):
            item_text = dic_value['text']
            item_value = dic_value['value']
            line_edit_text = dic_value['line_edit_widget'].text()
            line_edit_text = line_edit_text.strip().title()
            return item_text, item_value, line_edit_text


        '''
        ######################
            TAB - HOTKEYS          
        ######################
        '''
        WIDGET_HOTKEY_POS_X = WIDGETS_POS_X
        widget_hotkey_pos_y = WIDGETS_POS_Y
        HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF = 180

        for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

            item_text, item_value = get_dic_values_before_widget_creation(hotkey_dic_value)

            ''' LABEL '''
            item_label = QLabel(tab_hotkey, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_HOTKEY_POS_X, widget_hotkey_pos_y)

            ''' LINE EDIT '''
            hotkey_dic_value['line_edit_widget'] = QLineEdit(tab_hotkey)
            line_edit_widget = hotkey_dic_value['line_edit_widget']

            line_edit_widget.setText(item_value)
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_HOTKEY_POS_X + HOTKEY_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_hotkey_pos_y,
                120,
                LINE_EDIT_HIGHT
                )

            lines_amount = item_text.count('\n') + 1  # line break in text - multiple lines
            if lines_amount != 1:
                lines_amount = lines_amount * 0.8

            widget_hotkey_pos_y += int(WIDGETS_NEXT_LINE_POS_Y_DIFF * lines_amount)

        cv.hotkey_settings_last_widget_pos_y = widget_hotkey_pos_y + EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y


        def hotkey_fields_validation(pass_validation = True):
            ''' EXPRESSION CHECK '''
            line_edit_text_all_values = []

            for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(hotkey_dic_value)

                if "|" in line_edit_text:   # multiple hotkeys for the same action
                    for line_edit_text in line_edit_text.split("|"):
                        line_edit_text = line_edit_text.strip()
                        line_edit_text_all_values.append(line_edit_text)
                else:
                    line_edit_text_all_values.append(line_edit_text)

                search_result = cv.search_regex.search(line_edit_text.title())
                if not search_result:
                    MyMessageBoxError('HOTKEYS TAB', f'The "{item_text}" value is not valid.\n\n' +
                    "Acceptable hotkey format examples:\n" +
                    "`M`, `m`, `Ctrl`, `ctRL`, `M+Ctrl`, `Ctrl++`, `Ctrl+-`, `M+Ctrl+Space`, `Shift+Left`, `M | P`, `M+Ctrl | P`")
                    pass_validation = False


            ''' DUPLICATE CHECK '''
            if pass_validation:
                for index, item in enumerate(line_edit_text_all_values):
                    for index_2, item_2 in enumerate(line_edit_text_all_values[(index+1):]):
                        if item == item_2 and item != '':
                            MyMessageBoxError('HOTKEYS TAB', f'The "{item}" hotkey value used more than once.')
                            pass_validation = False

            return pass_validation


        def hotkeys_fields_to_save(to_save = False):
            for hotkey_dic_key, hotkey_dic_value in cv.hotkey_settings_dic.items():

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(hotkey_dic_value)

                if item_value != line_edit_text:
                    settings['hotkey_settings'][hotkey_dic_key] = line_edit_text
                    cv.hotkey_settings_dic[hotkey_dic_key]['value'] = line_edit_text
                    to_save = True

            if to_save:
                save_json()


        '''
        ######################
            TAB - GENERAL          
        ######################
        '''
        WIDGET_GENERAL_POS_X = WIDGETS_POS_X
        widget_general_pos_y = WIDGETS_POS_Y
        GENERAL_LABEL_LINE_EDIT_POS_X_DIFF = 195

        for item, dic_value in cv.general_settings_dic.items():

            item_text, item_value = get_dic_values_before_widget_creation(dic_value)

            ''' LABEL '''
            item_label = QLabel(tab_general, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_GENERAL_POS_X, widget_general_pos_y)

            ''' LINE EDIT '''
            cv.general_settings_dic[item]['line_edit_widget'] = QLineEdit(tab_general)
            line_edit_widget = cv.general_settings_dic[item]['line_edit_widget']

            # JUMP VALUES
            if 'jump' in item_text:
                line_edit_widget.setText(str(int(item_value/1000)))
            # OTHER VALUES    
            else:
                line_edit_widget.setText(str(item_value))

            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_GENERAL_POS_X + GENERAL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_general_pos_y,
                100,
                LINE_EDIT_HIGHT
                )

            lines_amount = item_text.count('\n') + 1    # line break in text - multiple lines
            if lines_amount != 1:
                lines_amount = lines_amount * 0.8

            widget_general_pos_y += int(WIDGETS_NEXT_LINE_POS_Y_DIFF * lines_amount)

        cv.general_settings_last_widget_pos_y = widget_general_pos_y + EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y


        def general_fields_validation(pass_validation = True):
            ''' Screen values can be bigger than the display size:
                    -> no over-reaching or error would occur
                Still feels good idea to cap the max window values
            '''
            MAX_WINDOW_SIZE_XY = 4500
            for general_dic_key, general_dic_value in cv.general_settings_dic.items():

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(general_dic_value)

                if item_text in cv.gen_sett_boolean_text_list:
                    if line_edit_text not in ['True', 'False']:
                        MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be "True" or "False".')
                        pass_validation = False

                elif item_text in cv.gen_sett_window_width_text_list:
                    if (not line_edit_text.isdecimal() or
                        int(line_edit_text) < cv.window_min_width or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                            MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}.')
                            pass_validation = False

                elif item_text in cv.gen_sett_window_height_text_list:
                    if (not line_edit_text.isdecimal() or
                        int(line_edit_text) < cv.window_min_height or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                            MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}.')
                            pass_validation = False

                elif item_text == cv.general_settings_dic['thumbnail_img_size']['text']:
                    if not line_edit_text.isdecimal() or int(line_edit_text) not in range(100, 501):
                        MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be between 100 and 500.')
                        pass_validation = False

                elif item_text == cv.general_settings_dic['thumbnail_remove_older_than']['text']:
                    if not line_edit_text.lstrip('-').isdecimal() or int(line_edit_text) not in range(-1, 365):
                        MyMessageBoxError('GENERAL TAB',
                                          'The "Remove unused thumbnails" value should be between -1 and 365.   \n'
                                          '0 = clean up after every app closure.\n'
                                          '-1 = no auto thumbnail removal.')
                        pass_validation = False

                else:
                    if not line_edit_text.isdecimal():
                        MyMessageBoxError('GENERAL TAB', f'The "{item_text}" value should be a positive integer.')
                        pass_validation = False

            return pass_validation


        def general_fields_to_save(to_save = False):
            for general_dic_key, general_dic_value in cv.general_settings_dic.items():

                item_text, item_value, line_edit_text = get_dic_values_after_widget_creation(general_dic_value)

                if item_text in cv.gen_sett_jump_text_list:
                    time_to_jump = int(line_edit_text)*1000
                    if item_value != time_to_jump:
                        settings['general_settings'][general_dic_key] = time_to_jump
                        cv.general_settings_dic[general_dic_key]['value'] = time_to_jump
                        to_save = True

                elif item_text in cv.gen_sett_boolean_text_list:
                    if item_value != eval(line_edit_text):
                        settings['general_settings'][general_dic_key] = eval(line_edit_text)    # "true"(str) -> bool
                        cv.general_settings_dic[general_dic_key]['value'] = eval(line_edit_text)
                        to_save = True

                else:
                    if item_value != int(line_edit_text):
                        settings['general_settings'][general_dic_key] = int(line_edit_text)
                        cv.general_settings_dic[general_dic_key]['value'] = int(line_edit_text)
                        to_save = True
            if to_save:
                save_json()
                update_real_time_used_variables()


        def update_real_time_used_variables():
            """
                Update values which can be used after
                clicked on the "Save" button
                without restarting the app
            """
            # GENERAL
            sett_gen = settings['general_settings']
            cv.always_on_top = sett_gen['always_on_top']
            cv.continue_playback = sett_gen['continue_playback']
            cv.small_jump = sett_gen['small_jump']
            cv.medium_jump = sett_gen['medium_jump']
            cv.big_jump = sett_gen['big_jump']
            cv.window_width = sett_gen['window_width']
            cv.window_height = sett_gen['window_height']
            cv.window_alt_width = sett_gen['window_alt_width']
            cv.window_alt_height = sett_gen['window_alt_height']
            cv.window_second_alt_width = sett_gen['window_second_alt_width']
            cv.window_second_alt_height = sett_gen['window_second_alt_height']
            cv.window_alt_size_repositioning = sett_gen['window_alt_size_repositioning']
            cv.window_auto_resize_to_video_resolution = sett_gen['window_auto_resize_to_video_resolution']
            cv.default_audio_track = sett_gen['default_audio_track']
            cv.thumbnail_img_size = sett_gen['thumbnail_img_size']
            cv.thumbnail_width = cv.thumbnail_img_size + cv.widg_and_img_diff
            cv.thumbnail_height = cv.thumbnail_img_size + cv.widg_and_img_diff
            cv.thumbnail_remove_older_than = sett_gen['thumbnail_remove_older_than']
            cv.search_result_parent_dicts_size = sett_gen['search_result_parent_dicts_size']


        '''
        ######################
            TAB - PLAYLIST            
        ######################
        '''
        WIDGET_PL_POS_X = WIDGETS_POS_X
        widget_pl_pos_y = WIDGETS_POS_Y
        PL_LABEL_LINE_EDIT_POS_X_DIFF = 100
        PL_LINE_EDIT_WIDGET_LENGTH = 190
        PL_LINE_EDIT_BUTTON_POS_X_DIFF = 10
        BUTTON_POS_X = WIDGET_PL_POS_X + PL_LABEL_LINE_EDIT_POS_X_DIFF + PL_LINE_EDIT_WIDGET_LENGTH + PL_LINE_EDIT_BUTTON_POS_X_DIFF
        number_counter = 1

        # AT GENERAL AND HOTKEYS TAB THE LOWEST DIC. KAY-VALUE PAIR WERE ITERATED
        # AT PLAYLIST IT IS THE TOP / PLAYLIST TITLES
        for pl in cv.playlist_widget_dic:

            ''' LABEL '''
            number = QLabel(tab_playlist, text=f'Playlist #{number_counter}')
            number.setFont(inactive_track_font_style)

            if number_counter >= 10:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)
            else:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)

            ''' LINE EDIT '''
            cv.playlist_widget_dic[pl]['line_edit'] = QLineEdit(tab_playlist)
            line_edit_widget = cv.playlist_widget_dic[pl]['line_edit']

            line_edit_widget.setText(settings['playlists'][pl]['playlist_title'])
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_PL_POS_X + PL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_pl_pos_y,
                PL_LINE_EDIT_WIDGET_LENGTH,
                LINE_EDIT_HIGHT
                )

            ''' BUTTONS - JUMP TO PLAYLIST '''
            cv.playlist_widget_dic[pl]['button_jump_to_playlist'] = ButtonJumpToPlaylist(tab_playlist, number_counter-1)
            cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setGeometry(
                BUTTON_POS_X,
                widget_pl_pos_y,
                LINE_EDIT_HIGHT,
                LINE_EDIT_HIGHT
                )
            if not line_edit_widget.text():
                cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(False)

            number_counter += 1
            widget_pl_pos_y += WIDGETS_NEXT_LINE_POS_Y_DIFF

        cv.playlist_settings_last_widget_pos_y = widget_pl_pos_y + EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y


        def playlist_fields_validation_at_least_one_playlist():
            ''' 
                Avoid removing all the playlist titles
                Avoid saving playlist titles over 25 char.s
            '''
            pl_list_with_title = []
            for pl in cv.playlist_widget_dic:
                playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
                if len(playlist_title) > 25:
                    playlist_title = f'{playlist_title[0:23]}..'
                    cv.playlist_widget_dic[pl]['line_edit'].setText(playlist_title)
                    MyMessageBoxError('PLAYLISTS TAB', f'The more than 25 char.s long  \n titles will be truncated:\n\n"{playlist_title}"')
                if len(playlist_title) != 0:
                    pl_list_with_title.append(pl)
            if len(pl_list_with_title) == 0:
                MyMessageBoxError('PLAYLISTS TAB', 'At least one playlist title needed!')
            return pl_list_with_title


        def playlist_fields_validation_playing_playlist(pass_validation = True):
            ''' Avoid removing the playing playlist '''
            for pl in cv.playlist_widget_dic:
                playlist_index = cv.playlist_list.index(pl)
                new_playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
                prev_playlist_title = settings['playlists'][pl]['playlist_title']

                if (
                    not new_playlist_title and
                    prev_playlist_title and
                    playlist_index == cv.playing_playlist_index and
                    (br.av_player.player.isPlaying() or br.av_player.paused)
                    ):
                        cv.playlist_widget_dic[pl]['line_edit'].setText(prev_playlist_title)
                        MyMessageBoxError(
                                        'PLAYLISTS TAB',
                                        f'Playing playlist can not be removed, Playlist #{playlist_index+1}:  {prev_playlist_title}')
                        pass_validation = False
            return pass_validation


        def playlist_fields_validation_queued_track(pass_validation = True):
            ''' Avoid removing playlists with queued track '''
            if cv.queue_playlists_list:
                for pl in cv.playlist_widget_dic:
                    playlist_index = cv.playlist_list.index(pl)
                    new_playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
                    prev_playlist_title = settings['playlists'][pl]['playlist_title']

                    if (
                        not new_playlist_title and
                        prev_playlist_title and
                        pl in cv.queue_playlists_list
                        ):
                            cv.playlist_widget_dic[pl]['line_edit'].setText(prev_playlist_title)
                            MyMessageBoxError(
                                            'PLAYLISTS TAB',
                                            f'Playlist with queued track can not be removed, Playlist #{playlist_index+1}:  {prev_playlist_title}')
                            pass_validation = False
            return pass_validation


        def playlists_fields_to_save(to_save = False):
            for pl in cv.playlist_widget_dic:
                playlist_index = cv.playlist_list.index(pl)
                new_playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
                prev_playlist_title = settings['playlists'][pl]['playlist_title']

                if new_playlist_title != prev_playlist_title:

                    # NEW TITLE, PREV: EMPTY - INVISIBLE
                    if new_playlist_title and not prev_playlist_title:
                        br.playlists_all.setTabVisible(playlist_index, 1)
                        cv.playlists_without_title_to_hide_index_list.remove(playlist_index)
                        cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(True)

                    # NEW TITLE: EMPTY, PREV: TITLE - VISIBLE
                    elif not new_playlist_title and prev_playlist_title:
                        br.playlists_all.setTabVisible(playlist_index, 0)
                        cv.playlists_without_title_to_hide_index_list.append(playlist_index)
                        cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(False)

                    br.playlists_all.setTabText(playlist_index, new_playlist_title)
                    settings['playlists'][pl]['playlist_title'] = new_playlist_title
                    cv.playlist_widget_dic[pl]['playlist_title'] = new_playlist_title
                    to_save = True

            if to_save:
                save_json()


        ''' 
        #####################
            TABS COMPILING     
        #####################
        
        WIDGETS_WINDOW and SCROLL_AREA background color is the same
        --> if WIDGETS_WINDOW size < SCROLL_AREA --> still looks like one window
        '''
        def set_widgets_window_style(widgets_window):
            widgets_window.setStyleSheet(
                            "QWidget"
                                "{"
                                "background-color: #F9F9F9;"
                                "}"
                            "QLineEdit"
                                "{"
                                "background-color: white;"
                                "}"
                                )


        def set_scroll_area_style(scroll_area):
            scroll_area.setStyleSheet(
                                "QScrollArea"
                                    "{"
                                    "background-color: #F9F9F9;" 
                                    "border: 1px solid #C2C2C2;"
                                    "border-radius: 2px;"
                                    "}"
                                )


        def set_scroll_bar_style(scroll_bar):
            scroll_bar.setStyleSheet(
                                    "QScrollBar::vertical"
                                        "{"
                                        "width: 10px;"
                                        "}"
                                    "QScrollBar::horizontal"
                                        "{"
                                        "width: 0px;"
                                        "}"
                                    )

        tabs_dic = {
            'Playlists': {
                'text': 'Playlists',
                'scroll_area': tab_playlist_scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_playlist,
                'widgets_window_height': cv.playlist_settings_last_widget_pos_y
            },
            'General': {
                'text': 'General',
                'scroll_area': tab_general_scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_general,
                'widgets_window_height': cv.general_settings_last_widget_pos_y
            },
            'Hotkeys': {
                'text': 'Hotkeys',
                'scroll_area': tab_hotkey_scroll_area,
                'scroll_bar_ver': '',
                'scroll_bar_hor': '',
                'widgets_window': tab_hotkey,
                'widgets_window_height': cv.hotkey_settings_last_widget_pos_y
            }
        }


        '''
        WIDGET RESIZE 
            - If widget size > tab size -> scroll bar visible
            - resize(WINDOW_WIDTH-50,.. -> no horizontal scroll bar
            - widget amount -> vertical scroll bar visible / invisible
            - more info: docs / learning / set_scrollbar_to_tab_widget.py 
        '''
        for tab in tabs_dic:
            tabs_dic[tab]['widgets_window'].resize(WINDOW_WIDTH, tabs_dic[tab]['widgets_window_height'])
            set_widgets_window_style(tabs_dic[tab]['widgets_window'])

            tabs_dic[tab]['scroll_bar_ver'] = QScrollBar()
            set_scroll_bar_style(tabs_dic[tab]['scroll_bar_ver'])
            tabs_dic[tab]['scroll_bar_hor'] = QScrollBar()
            set_scroll_bar_style(tabs_dic[tab]['scroll_bar_hor'])

            tabs_dic[tab]['scroll_area'].setVerticalScrollBar(tabs_dic[tab]['scroll_bar_ver'])
            tabs_dic[tab]['scroll_area'].setHorizontalScrollBar(tabs_dic[tab]['scroll_bar_hor'])
            set_scroll_area_style(tabs_dic[tab]['scroll_area'])

            tabs_dic[tab]['scroll_area'].setWidget(tabs_dic[tab]['widgets_window'])
            tabs.addTab(tabs_dic[tab]['scroll_area'], tabs_dic[tab]['text'])


        '''
        ####################
            BUTTON - SAVE      
        ####################
        '''
        BUTTON_SAVE_WIDTH = 50
        BUTTON_SAVE_HEIGHT = 25
        BUTTON_SAVE_POS_X = WINDOW_WIDTH - TABS_POS_X - BUTTON_SAVE_WIDTH
        BUTTON_SAVE_POS_Y = WINDOW_HEIGHT - TABS_POS_Y - BUTTON_SAVE_HEIGHT


        def button_save_clicked():
            pl_list_with_title = playlist_fields_validation_at_least_one_playlist()

            if (pl_list_with_title and
                playlist_fields_validation_playing_playlist() and
                playlist_fields_validation_queued_track() and
                general_fields_validation() and
                hotkey_fields_validation()):

                ''' GENERAL TAB FIELDS '''
                hotkeys_fields_to_save()

                ''' GENERAL TAB FIELDS '''
                general_fields_to_save()

                ''' PLAYLISTS TAB FIELDS '''
                switch_all_pl_to_standard_from_thumbnails_view()
                playlists_fields_to_save()


                ''' 
                    If the last used playlist removed 
                    at next start the new last playlist will active / displayed
                '''
                if  len(settings['playlists'][cv.playlist_list[cv.active_playlist_index]]['playlist_title']) == 0:
                    cv.active_playlist_index = settings['playlists'][pl_list_with_title[-1]]['playlist_index']
                    settings['last_used_playlist'] = cv.active_playlist_index
                    save_json()

                self.hide()


        button_save = QPushButton(self, text='Save')
        button_save.setGeometry(BUTTON_SAVE_POS_X, BUTTON_SAVE_POS_Y, BUTTON_SAVE_WIDTH, BUTTON_SAVE_HEIGHT)
        button_save.clicked.connect(button_save_clicked)


        '''
        #################################
            BUTTON - PURGE THUMBNAILS     
        #################################
        '''
        BUTTON_PURGE_THUMBNAILS_WIDTH = 130
        BUTTON_PURGE_THUMBNAILS_HEIGHT = BUTTON_SAVE_HEIGHT
        BUTTON_PURGE_THUMBNAILS_POS_X = BUTTON_SAVE_POS_X - BUTTON_PURGE_THUMBNAILS_WIDTH - 5
        BUTTONP_PURGE_THUMBNAILS_POS_Y = BUTTON_SAVE_POS_Y

        button_purge_thumbnails = QPushButton(self, text='Purge Thumbnails')
        button_purge_thumbnails.setGeometry(
            BUTTON_PURGE_THUMBNAILS_POS_X,
            BUTTONP_PURGE_THUMBNAILS_POS_Y,
            BUTTON_PURGE_THUMBNAILS_WIDTH,
            BUTTON_PURGE_THUMBNAILS_HEIGHT
            )
        button_purge_thumbnails.clicked.connect(
            msg_box_wrapper_for_remove_all_thumbnails_and_clear_history
            )

    def reposition_window_to_middle(self):
        move_window_to_middle_of_current_screen(self)