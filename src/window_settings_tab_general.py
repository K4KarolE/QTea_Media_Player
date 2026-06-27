from PyQt6.QtWidgets import QLabel, QLineEdit, QScrollArea, QWidget

from .class_data import cv, settings, save_json
from .func_coll import inactive_track_font_style
from .message_box import MyMessageBoxError
from .window_settings_common import CommonTabValues



class GeneralTab(CommonTabValues):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.inner_window = QWidget()
        self.last_widget_pos_y = 0

        WIDGET_GENERAL_POS_X = self.WIDGETS_POS_X
        widget_general_pos_y = self.WIDGETS_POS_Y
        GENERAL_LABEL_LINE_EDIT_POS_X_DIFF = 195
        LINE_BREAK_AFTER_LIST_GEN = [
            'play_at_startup',
            'big_jump',
            'window_auto_resize_to_video_resolution',
            'thumbnail_remove_older_than',
            'conf_msg_at_clear_playlist_with_playing_track']
        LINE_BREAK_SIZE_GEN = 20
        LINE_BREAK_SEPERATOR_GEN = "\n " + "_" * 34

        for gen_dic_key, dic_value in cv.general_settings_dic.items():

            item_text, item_value = self.get_dic_values_before_widget_creation(dic_value)

            ''' LABEL '''
            # Adding seperator to the line break
            # In the Settings window it looks like there is a separator below the field title
            # The field title and the separator are one QLabel object
            item_text_original = item_text
            if gen_dic_key in LINE_BREAK_AFTER_LIST_GEN:
                item_text += LINE_BREAK_SEPERATOR_GEN

            item_label = QLabel(self.inner_window, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_GENERAL_POS_X, widget_general_pos_y)

            ''' LINE EDIT '''
            cv.general_settings_dic[gen_dic_key]['line_edit_widget'] = QLineEdit(self.inner_window)
            line_edit_widget = cv.general_settings_dic[gen_dic_key]['line_edit_widget']

            # JUMP VALUES
            if 'jump' in item_text:
                line_edit_widget.setText(str(int(item_value / 1000)))
            # OTHER VALUES
            else:
                line_edit_widget.setText(str(item_value))

            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(self.LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_GENERAL_POS_X + GENERAL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_general_pos_y,
                100,
                self.LINE_EDIT_HIGHT
            )

            # Adding extra space after a multi line QLabel field title like:
            # "Automatically clear playlist
            #  when it is removed"
            lines_amount = item_text_original.count('\n') + 1  # line break in too long text - multiple lines
            if lines_amount != 1:
                multi_line_compensation = lines_amount * 12
            else:
                multi_line_compensation = 0

            widget_general_pos_y += int(self.WIDGETS_NEXT_LINE_POS_Y_DIFF + multi_line_compensation)

            # To make gap between different sections, item: 'always_on_top', 'continue_playback'
            if gen_dic_key in LINE_BREAK_AFTER_LIST_GEN:
                widget_general_pos_y += LINE_BREAK_SIZE_GEN

        self.last_widget_pos_y = widget_general_pos_y + self.EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y



    def general_fields_validation(self, pass_validation=True):
        """
        Screen values can be bigger than the display size:
            -> no over-reaching or error would occur
        Still feels good idea to cap the max window values
        """
        MAX_WINDOW_SIZE_XY = 4500
        for general_dic_key, general_dic_value in cv.general_settings_dic.items():

            item_text, item_value, line_edit_text = self.get_dic_values_after_widget_creation(general_dic_value)

            if item_text in cv.gen_sett_boolean_text_list:
                if line_edit_text not in ['True', 'T', 'False', 'F']:
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be one of the below:   \n'
                        '"True", "T", "False", "F"\n\n'
                        'It is not case sensitive.')
                    pass_validation = False

            elif item_text in cv.gen_sett_window_width_text_list:
                if (not line_edit_text.isdecimal() or
                        int(line_edit_text) < cv.window_min_width or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}.')
                    pass_validation = False

            elif item_text in cv.gen_sett_window_height_text_list:
                if (not line_edit_text.isdecimal() or
                        int(line_edit_text) < cv.window_min_height or
                        int(line_edit_text) > MAX_WINDOW_SIZE_XY):
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be an integer: {cv.window_min_width}=< X <={MAX_WINDOW_SIZE_XY}.')
                    pass_validation = False

            elif item_text in cv.gen_sett_string_text_list:
                if (text_length := len(line_edit_text)) > 20:
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError('GENERAL TAB',
                                      f'The "{item_text}" value should not be longer than 20 characters.\n\n'
                                      f'The current one is {text_length} characters long.')
                    pass_validation = False

            elif item_text == cv.general_settings_dic['thumbnail_img_size']['text']:
                if not line_edit_text.isdecimal() or int(line_edit_text) not in range(100, 501):
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be between 100 and 500.')
                    pass_validation = False

            elif item_text == cv.general_settings_dic['thumbnail_remove_older_than']['text']:
                if not line_edit_text.lstrip('-').isdecimal() or int(line_edit_text) not in range(-1, 365):
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be between -1 and 365.   \n'
                        '0 = clean up after every app closure.\n'
                        '-1 = no auto thumbnail removal.')
                    pass_validation = False

            else:
                if not line_edit_text.isdecimal():
                    item_text = item_text.replace('\n', ' ')
                    MyMessageBoxError(
                        'GENERAL TAB',
                        f'The "{item_text}" value should be a positive integer.')
                    pass_validation = False

        return pass_validation


    def general_fields_to_save(self, to_save=False):
        """
        Guide for the "item_text, item_value, line_edit_text" values:

        general_settings_dic = {        # generated in "src / class_data"
            'always_on_top': {
                'text': 'Always on top',    - item_text - displayed explanation text
                'value': always_on_top,     - item_value - variable - cv.always_on_top - the saved value
                'line_edit_widget': ''      - item_line_edit_widget.text() = current field value
            },
            {..}
        """
        for general_dic_key, general_dic_value in cv.general_settings_dic.items():

            item_text, item_value, line_edit_text = self.get_dic_values_after_widget_creation(general_dic_value)

            if item_text in cv.gen_sett_jump_text_list:
                time_to_jump = int(line_edit_text) * 1000
                if item_value != time_to_jump:
                    settings['general_settings'][general_dic_key] = time_to_jump
                    cv.general_settings_dic[general_dic_key]['value'] = time_to_jump
                    to_save = True

            elif item_text in cv.gen_sett_boolean_text_list:
                if len(line_edit_text) == 1:
                    # "f" >> "False", "T" >> "True"
                    line_edit_text = {'T': 'True', 'F': 'False'}[line_edit_text]
                    cv.general_settings_dic[general_dic_key]['line_edit_widget'].setText(line_edit_text)
                if item_value != eval(line_edit_text):
                    settings['general_settings'][general_dic_key] = eval(line_edit_text)  # "true"(str) -> bool
                    cv.general_settings_dic[general_dic_key]['value'] = eval(line_edit_text)
                    # True > false > False
                    cv.general_settings_dic[general_dic_key]['line_edit_widget'].setText(line_edit_text)
                    to_save = True

            elif item_text in cv.gen_sett_string_text_list:
                if item_value != line_edit_text:
                    settings['general_settings'][general_dic_key] = line_edit_text
                    cv.general_settings_dic[general_dic_key]['value'] = line_edit_text
                    to_save = True

            else:
                if item_value != int(line_edit_text):
                    settings['general_settings'][general_dic_key] = int(line_edit_text)
                    cv.general_settings_dic[general_dic_key]['value'] = int(line_edit_text)
                    to_save = True
        if to_save:
            save_json()
            self.update_real_time_used_variables()


    def update_real_time_used_variables(self):
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
        cv.add_dir_ignore_file_titles_including = sett_gen['add_dir_ignore_file_titles_including']
        cv.clear_playlist_at_playlist_remove = sett_gen['clear_playlist_at_playlist_remove']
        cv.conf_msg_at_clear_playlist_with_playing_track = sett_gen['conf_msg_at_clear_playlist_with_playing_track']
        cv.add_dir_ignored_file_titles_conf_msg = sett_gen['add_dir_ignored_file_titles_conf_msg']
