from dataclasses import dataclass
from pathlib import Path
from json import load, dump
import sys

from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication

from .class_data import cv


def open_skin_json():
    with open(PATH_JSON_SETTINGS) as f:
        json_dic = load(f)
    return json_dic

def save_skin_json():
    with open(PATH_JSON_SETTINGS, 'w') as f:
        dump(skin_settings, f, indent=2)
    return

if cv.skin_selected != 'system':
    WORKING_DIRECTORY = Path().resolve()
    PATH_JSON_SETTINGS = Path(WORKING_DIRECTORY, 'skins', 'jsons', f'{cv.skin_selected}.json')
    skin_settings = open_skin_json()

palette_dic = {
    "text": QPalette.ColorRole.Text,
    "base": QPalette.ColorRole.Base,
    "alternate_base": QPalette.ColorRole.AlternateBase,
    "button": QPalette.ColorRole.Button,
    "button_text": QPalette.ColorRole.ButtonText,
    "highlight": QPalette.ColorRole.Highlight,
    "highlighted_text": QPalette.ColorRole.HighlightedText,
    "mid": QPalette.ColorRole.Mid,
    "mid_light": QPalette.ColorRole.Midlight,
    "light": QPalette.ColorRole.Light,
    "dark": QPalette.ColorRole.Dark,
    "shadow": QPalette.ColorRole.Shadow,
    "no_color_roles": QPalette.ColorRole.NColorRoles,
}


@dataclass()
class Skins:

    if cv.skin_selected == 'system':
        """
        QApplication() has to be under the condition, otherwise the
        "QApplication.setDesktopSettingsAware(False)" will not work
        at the "src / application"
        """
        palette = QApplication(sys.argv).palette()

        def get_color_hex(dic_key, palette=palette):
            return (palette.color(palette_dic[dic_key])).name()

        text = get_color_hex('text')
        base = get_color_hex('base')
        alternate_base = get_color_hex('alternate_base')
        button = get_color_hex('button')
        button_text = get_color_hex('button_text')
        highlight = get_color_hex('highlight')
        highlighted_text = get_color_hex('highlighted_text')
        mid = get_color_hex('mid')
        mid_light = get_color_hex('mid_light')
        light = get_color_hex('light')
        dark = get_color_hex('dark')
        shadow = get_color_hex('shadow')
        no_color_roles = get_color_hex('no_color_roles')


        # DARK SYSTEM THEME
        if int(base.strip('#'), 16) <= 3355449:
            """ WINDOW - DARK """
            window = base

            """ THUMBNAIL - DARK """
            thumbnail_window = mid

            thumbnail_widget = mid
            thumbnail_widget_text = text
            thumbnail_widget_border = text

            thumbnail_widget_selected = text
            thumbnail_widget_selected_border = highlighted_text
            thumbnail_widget_selected_text = base

            thumbnail_widget_playing = highlight
            thumbnail_widget_playing_border = highlight
            thumbnail_widget_playing_text = highlighted_text

            thumbnail_widget_queue = text
            thumbnail_widget_queue_text = base

            """ PLAYLIST ROWS - DARK """
            row_inactive = mid
            row_inactive_text = text
            row_selected = text
            row_selected_text = base
            row_playing = highlight
            row_playing_text = highlighted_text
            row_queued = text
            row_queued_text = base

            """ SLIDERS - DARK """
            slider_duration_groove = alternate_base
            slider_duration_sub_page = highlight
            slider_duration_handle_pos_0_1 = alternate_base
            slider_duration_handle_pos_2 = alternate_base

            slider_volume_groove = alternate_base
            slider_volume_sub_page = highlight
            slider_volume_handle_pos_0_1 = alternate_base
            slider_volume_handle_pos_2 = alternate_base

            """ PLAYLIST TAB - DARK """
            tab_playlist_bg_1 = mid
            tab_playlist_bg_2 = mid
            tab_playlist_bg_3 = alternate_base
            tab_playlist_bg_4 = alternate_base
            tab_playlist_border = mid
            tab_playlist_font = text

            tab_playlist_selected_bg = highlight
            tab_playlist_selected_border = highlight
            tab_playlist_selected_font = highlighted_text


            """ PLAYING BUTTONS - UNDER THE VIDEO AREA - DARK """
            buttons_playing_bg_0 = mid
            buttons_playing_bg_1 = mid
            buttons_playing_bg_2 = alternate_base
            buttons_playing_bg_3 = alternate_base
            buttons_playing_border = no_color_roles
            buttons_playing_pressed_bg = highlight

            """ DURATION INFO BUTTON - UNDER THE VIDEO AREA - DARK """
            button_duration_info_text = no_color_roles

            """ DURATION SUM INFO BUTTON - UNDER PLAYLISTS - DARK """
            button_duration_sum_info_bg_0 = mid
            button_duration_sum_info_bg_1 = mid
            button_duration_sum_info_bg_2 = alternate_base
            button_duration_sum_info_bg_3 = alternate_base
            button_duration_sum_info_border = no_color_roles
            button_duration_sum_info_text = no_color_roles

            """ PLAYLIST BUTTONS - UNDER PLAYLISTS - DARK """
            buttons_settings_bg_0 = mid
            buttons_settings_bg_1 = mid
            buttons_settings_bg_2 = alternate_base
            buttons_settings_bg_3 = alternate_base
            buttons_settings_border = no_color_roles
            buttons_settings_font = text
            buttons_settings_pressed_bg = highlight

            """ SETTINGS BUTTONS - UNDER PLAYLISTS - DARK """
            buttons_playlist_bg_0 = mid
            buttons_playlist_bg_1 = mid
            buttons_playlist_bg_2 = alternate_base
            buttons_playlist_bg_3 = alternate_base
            buttons_playlist_border = no_color_roles
            buttons_playlist_font = text
            buttons_playlist_pressed_bg = highlight

            """ SETTINGS WINDOW - DARK """
            window_settings = base
            window_settings_inner_window = mid
            window_settings_inner_window_border = no_color_roles
            window_settings_line_edit = mid
            window_settings_line_edit_text = text
            window_settings_line_edit_border = text
            window_settings_button = button
            window_settings_button_border = text
            window_settings_button_text = text
            window_settings_button_pressed_bg = highlight
            window_settings_button_pressed_text = text
            window_settings_scrollbar = mid

            """ QUEUE AND SEARCH WINDOW - DARK """
            window_q_and_s = base

            window_q_and_s_search_button_bg_0 = mid
            window_q_and_s_search_button_bg_1 = mid
            window_q_and_s_search_button_bg_2 = alternate_base
            window_q_and_s_search_button_bg_3 = alternate_base
            window_q_and_s_search_button_border = highlight
            window_q_and_s_search_button_pressed = highlight

            window_q_and_s_search_line_edit = mid
            window_q_and_s_search_line_edit_text = text
            window_q_and_s_search_line_edit_border = highlight

            window_q_and_s_search_frame = alternate_base
            window_q_and_s_search_frame_border = highlight

            window_q_and_s_queue_header = highlight
            window_q_and_s_queue_header_text = highlighted_text

            window_q_and_s_queue_frame_border = highlight
            # no "window_q_and_s_queue_frame", the inner widget covers all the frame

        # BRIGHT SYSTEM THEME
        else:
            """ WINDOW - BRIGHT """
            window = alternate_base

            """ THUMBNAIL - BRIGHT """
            thumbnail_window = mid

            thumbnail_widget = mid
            thumbnail_widget_text = text
            thumbnail_widget_border = text

            thumbnail_widget_selected = text
            thumbnail_widget_selected_border = highlighted_text
            thumbnail_widget_selected_text = base

            thumbnail_widget_playing = highlight
            thumbnail_widget_playing_border = highlight
            thumbnail_widget_playing_text = highlighted_text

            thumbnail_widget_queue = text
            thumbnail_widget_queue_text = base

            """ PLAYLIST ROWS - BRIGHT """
            row_inactive = mid
            row_inactive_text = text
            row_selected = text
            row_selected_text = base
            row_playing = highlight
            row_playing_text = highlighted_text
            row_queued = text
            row_queued_text = base

            """ SLIDERS - BRIGHT """
            slider_duration_groove = dark
            slider_duration_sub_page = highlight
            slider_duration_handle_pos_0_1 = alternate_base
            slider_duration_handle_pos_2 = no_color_roles

            slider_volume_groove = dark
            slider_volume_sub_page = highlight
            slider_volume_handle_pos_0_1 = alternate_base
            slider_volume_handle_pos_2 = no_color_roles

            """ PLAYLIST TAB - BRIGHT """
            tab_playlist_bg_1 = mid
            tab_playlist_bg_2 = mid
            tab_playlist_bg_3 = alternate_base
            tab_playlist_bg_4 = alternate_base
            tab_playlist_border = dark
            tab_playlist_font = text

            tab_playlist_selected_bg = highlight
            tab_playlist_selected_border = highlight
            tab_playlist_selected_font = highlighted_text


            """ PLAYING BUTTONS - UNDER THE VIDEO AREA - BRIGHT """
            buttons_playing_bg_0 = mid
            buttons_playing_bg_1 = mid
            buttons_playing_bg_2 = dark
            buttons_playing_bg_3 = dark
            buttons_playing_border = no_color_roles
            buttons_playing_pressed_bg = highlight

            """ DURATION INFO BUTTON - UNDER THE VIDEO AREA - BRIGHT """
            button_duration_info_text = no_color_roles

            """ DURATION SUM INFO BUTTON - UNDER PLAYLISTS - BRIGHT """
            button_duration_sum_info_bg_0 = mid
            button_duration_sum_info_bg_1 = mid
            button_duration_sum_info_bg_2 = dark
            button_duration_sum_info_bg_3 = dark
            button_duration_sum_info_border = no_color_roles
            button_duration_sum_info_text = text

            """ PLAYLIST BUTTONS - UNDER PLAYLISTS - BRIGHT """
            buttons_settings_bg_0 = base
            buttons_settings_bg_1 = mid
            buttons_settings_bg_2 = dark
            buttons_settings_bg_3 = dark
            buttons_settings_border = no_color_roles
            buttons_settings_font = no_color_roles
            buttons_settings_pressed_bg = highlight

            """ SETTINGS BUTTONS - UNDER PLAYLISTS - BRIGHT """
            buttons_playlist_bg_0 = base
            buttons_playlist_bg_1 = mid
            buttons_playlist_bg_2 = dark
            buttons_playlist_bg_3 = dark
            buttons_playlist_border = no_color_roles
            buttons_playlist_font = no_color_roles
            buttons_playlist_pressed_bg = highlight

            """ SETTINGS WINDOW - BRIGHT """
            window_settings = base
            window_settings_inner_window = mid
            window_settings_inner_window_border = no_color_roles
            window_settings_line_edit = mid
            window_settings_line_edit_text = text
            window_settings_line_edit_border = text
            window_settings_button = button
            window_settings_button_border = text
            window_settings_button_text = text
            window_settings_button_pressed_bg = highlight
            window_settings_button_pressed_text = text
            window_settings_scrollbar = mid

            """ QUEUE AND SEARCH WINDOW - BRIGHT """
            window_q_and_s = base

            window_q_and_s_search_button_bg_0 = mid
            window_q_and_s_search_button_bg_1 = mid
            window_q_and_s_search_button_bg_2 = alternate_base
            window_q_and_s_search_button_bg_3 = alternate_base
            window_q_and_s_search_button_border = highlight
            window_q_and_s_search_button_pressed = highlight

            window_q_and_s_search_line_edit = mid
            window_q_and_s_search_line_edit_text = text
            window_q_and_s_search_line_edit_border = highlight

            window_q_and_s_search_frame = alternate_base
            window_q_and_s_search_frame_border = highlight

            window_q_and_s_queue_header = highlight
            window_q_and_s_queue_header_text = highlighted_text

            window_q_and_s_queue_frame_border = highlight
            # no "window_q_and_s_queue_frame", the inner widget covers all the frame

    # NON SYSTEM THEME
    else:
        """ WINDOW """
        window = skin_settings['window']

        """ THUMBNAIL """
        thumbnail_window = skin_settings['thumbnail_window']

        thumbnail_widget = skin_settings['thumbnail_widget']
        thumbnail_widget_text = skin_settings['thumbnail_widget_text']
        thumbnail_widget_border = skin_settings['thumbnail_widget_border']

        thumbnail_widget_selected = skin_settings['thumbnail_widget_selected']
        thumbnail_widget_selected_border = skin_settings['thumbnail_widget_selected_border']
        thumbnail_widget_selected_text = skin_settings['thumbnail_widget_selected_text']

        thumbnail_widget_playing = skin_settings['thumbnail_widget_playing']
        thumbnail_widget_playing_border = skin_settings['thumbnail_widget_playing_border']
        thumbnail_widget_playing_text = skin_settings['thumbnail_widget_playing_text']

        thumbnail_widget_queue = skin_settings['thumbnail_widget_queue']
        thumbnail_widget_queue_text = skin_settings['thumbnail_widget_queue_text']

        """ PLAYLIST ROWS """
        row_inactive = skin_settings['row_inactive']
        row_inactive_text = skin_settings['row_inactive_text']
        row_selected = skin_settings['row_selected']
        row_selected_text = skin_settings['row_selected_text']
        row_playing = skin_settings['row_playing']
        row_playing_text = skin_settings['row_playing_text']
        row_queued = skin_settings['row_queued']
        row_queued_text = skin_settings['row_queued_text']

        """ SLIDERS """
        slider_duration_groove = skin_settings['slider_duration_groove']
        slider_duration_sub_page = skin_settings['slider_duration_sub_page']
        slider_duration_handle_pos_0_1 = skin_settings['slider_duration_handle_pos_0_1']
        slider_duration_handle_pos_2 = skin_settings['slider_duration_handle_pos_2']

        slider_volume_groove = skin_settings['slider_volume_groove']
        slider_volume_sub_page = skin_settings['slider_volume_sub_page']
        slider_volume_handle_pos_0_1 = skin_settings['slider_volume_handle_pos_0_1']
        slider_volume_handle_pos_2 = skin_settings['slider_volume_handle_pos_2']

        """ PLAYLIST TAB """
        tab_playlist_bg_1 = skin_settings['tab_playlist_bg_1']
        tab_playlist_bg_2 = skin_settings['tab_playlist_bg_2']
        tab_playlist_bg_3 = skin_settings['tab_playlist_bg_3']
        tab_playlist_bg_4 = skin_settings['tab_playlist_bg_4']
        tab_playlist_border = skin_settings['tab_playlist_border']
        tab_playlist_font = skin_settings['tab_playlist_font']

        tab_playlist_selected_bg = skin_settings['tab_playlist_selected_bg']
        tab_playlist_selected_border = skin_settings['tab_playlist_selected_border']
        tab_playlist_selected_font = skin_settings['tab_playlist_selected_font']

        """ PLAYING BUTTONS - UNDER THE VIDEO AREA - BRIGHT """
        buttons_playing_bg_0 = skin_settings['buttons_playing_bg_0']
        buttons_playing_bg_1 = skin_settings['buttons_playing_bg_1']
        buttons_playing_bg_2 = skin_settings['buttons_playing_bg_2']
        buttons_playing_bg_3 = skin_settings['buttons_playing_bg_3']
        buttons_playing_border = skin_settings['buttons_playing_border']
        buttons_playing_pressed_bg = skin_settings['buttons_playing_pressed_bg']

        """ DURATION INFO BUTTON - UNDER THE VIDEO AREA """
        button_duration_info_text = skin_settings['button_duration_info_text']

        """ DURATION SUM INFO BUTTON - UNDER PLAYLISTS """
        button_duration_sum_info_bg_0 = skin_settings['button_duration_sum_info_bg_0']
        button_duration_sum_info_bg_1 = skin_settings['button_duration_sum_info_bg_1']
        button_duration_sum_info_bg_2 = skin_settings['button_duration_sum_info_bg_2']
        button_duration_sum_info_bg_3 = skin_settings['button_duration_sum_info_bg_3']
        button_duration_sum_info_border = skin_settings['button_duration_sum_info_border']
        button_duration_sum_info_text = skin_settings['button_duration_sum_info_text']

        """ PLAYLIST BUTTONS - UNDER PLAYLISTS """
        buttons_playlist_bg_0 = skin_settings['buttons_settings_bg_0']
        buttons_playlist_bg_1 = skin_settings['buttons_settings_bg_1']
        buttons_playlist_bg_2 = skin_settings['buttons_settings_bg_2']
        buttons_playlist_bg_3 = skin_settings['buttons_settings_bg_3']
        buttons_playlist_border = skin_settings['buttons_settings_border']
        buttons_playlist_font = skin_settings['buttons_settings_font']
        buttons_playlist_pressed_bg = skin_settings['buttons_settings_pressed_bg']

        """ SETTINGS BUTTONS - UNDER PLAYLISTS """
        buttons_settings_bg_0 = skin_settings['buttons_settings_bg_0']
        buttons_settings_bg_1 = skin_settings['buttons_settings_bg_1']
        buttons_settings_bg_2 = skin_settings['buttons_settings_bg_2']
        buttons_settings_bg_3 = skin_settings['buttons_settings_bg_3']
        buttons_settings_border = skin_settings['buttons_settings_border']
        buttons_settings_font = skin_settings['buttons_settings_font']
        buttons_settings_pressed_bg = skin_settings['buttons_settings_pressed_bg']

        """ SETTINGS WINDOW """
        window_settings = skin_settings['window_settings']
        window_settings_inner_window = skin_settings['window_settings_inner_window']
        window_settings_inner_window_border = skin_settings['window_settings_inner_window_border']
        window_settings_line_edit = skin_settings['window_settings_line_edit']
        window_settings_line_edit_text = skin_settings['window_settings_line_edit_text']
        window_settings_line_edit_border = skin_settings['window_settings_line_edit_border']
        window_settings_button = skin_settings['window_settings_button']
        window_settings_button_border = skin_settings['window_settings_button_border']
        window_settings_button_text = skin_settings['window_settings_button_text']
        window_settings_button_pressed_bg = skin_settings['window_settings_button_pressed_bg']
        window_settings_button_pressed_text = skin_settings['window_settings_button_pressed_text']
        window_settings_scrollbar = skin_settings['window_settings_scrollbar']

        """ QUEUE AND SEARCH WINDOW """
        window_q_and_s = skin_settings['window_q_and_s']

        window_q_and_s_search_button_bg_0 = skin_settings['window_q_and_s_search_button_bg_0']
        window_q_and_s_search_button_bg_1 = skin_settings['window_q_and_s_search_button_bg_1']
        window_q_and_s_search_button_bg_2 = skin_settings['window_q_and_s_search_button_bg_2']
        window_q_and_s_search_button_bg_3 = skin_settings['window_q_and_s_search_button_bg_3']
        window_q_and_s_search_button_border = skin_settings['window_q_and_s_search_button_border']
        window_q_and_s_search_button_pressed = skin_settings['window_q_and_s_search_button_pressed']

        window_q_and_s_search_line_edit = skin_settings['window_q_and_s_search_line_edit']
        window_q_and_s_search_line_edit_text = skin_settings['window_q_and_s_search_line_edit_text']
        window_q_and_s_search_line_edit_border = skin_settings['window_q_and_s_search_line_edit_border']

        window_q_and_s_search_frame = skin_settings['window_q_and_s_search_frame']
        window_q_and_s_search_frame_border = skin_settings['window_q_and_s_search_frame_border']

        window_q_and_s_queue_header = skin_settings['window_q_and_s_queue_header']
        window_q_and_s_queue_header_text = skin_settings['window_q_and_s_queue_header_text']

        window_q_and_s_queue_frame_border = skin_settings['window_q_and_s_queue_frame_border']
        # no "window_q_and_s_queue_frame", the inner widget covers all the frame

sk = Skins()