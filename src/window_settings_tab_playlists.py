from PyQt6.QtWidgets import QLabel, QLineEdit, QScrollArea, QWidget

from .class_bridge import br
from .class_data import cv, settings, save_json
from .func_coll import clear_playlist_at_playlist_remove_action, inactive_track_font_style
from .message_box import MyMessageBoxError
from .window_settings_common import CommonTabValues
from .window_settings_tab_playlist_buttons import ButtonJumpToPlaylist, ButtonRemovePlaylistTitle



class PlaylistsTab(CommonTabValues):
    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.inner_window = QWidget()

        WIDGET_PL_POS_X = self.WIDGETS_POS_X
        widget_pl_pos_y = self.WIDGETS_POS_Y
        PL_LABEL_LINE_EDIT_POS_X_DIFF = 100
        PL_LINE_EDIT_WIDGET_LENGTH = 170
        PL_LINE_EDIT_BUTTON_POS_X_DIFF = 10
        BUTTON_POS_X = WIDGET_PL_POS_X + PL_LABEL_LINE_EDIT_POS_X_DIFF + \
                       PL_LINE_EDIT_WIDGET_LENGTH + PL_LINE_EDIT_BUTTON_POS_X_DIFF
        BUTTON_2ND_POS_X = BUTTON_POS_X + 25
        number_counter = 1

        # AT GENERAL AND HOTKEYS TAB THE LOWEST DIC. KAY-VALUE PAIR WERE ITERATED
        # AT PLAYLIST IT IS THE TOP / PLAYLIST TITLES
        for pl in cv.playlist_widget_dic:

            ''' LABEL '''
            number = QLabel(self.inner_window, text=f'Playlist #{number_counter}')
            number.setFont(inactive_track_font_style)

            if number_counter >= 10:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)
            else:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)

            ''' LINE EDIT '''
            cv.playlist_widget_dic[pl]['line_edit'] = QLineEdit(self.inner_window)
            line_edit_widget = cv.playlist_widget_dic[pl]['line_edit']

            line_edit_widget.setText(settings['playlists'][pl]['playlist_title'])
            line_edit_widget.setFont(inactive_track_font_style)
            line_edit_widget.setAlignment(self.LINE_EDIT_TEXT_ALIGNMENT)
            line_edit_widget.setGeometry(
                WIDGET_PL_POS_X + PL_LABEL_LINE_EDIT_POS_X_DIFF,
                widget_pl_pos_y,
                PL_LINE_EDIT_WIDGET_LENGTH,
                self.LINE_EDIT_HIGHT
                )

            ''' BUTTONS - REMOVE PLAYLIST TITLE '''
            cv.playlist_widget_dic[pl]['button_remove_playlist_title'] = ButtonRemovePlaylistTitle(
                self.inner_window,
                number_counter-1)
            cv.playlist_widget_dic[pl]['button_remove_playlist_title'].setGeometry(
                BUTTON_POS_X,
                widget_pl_pos_y,
                self.LINE_EDIT_HIGHT,
                self.LINE_EDIT_HIGHT
            )
            if not line_edit_widget.text():
                cv.playlist_widget_dic[pl]['button_remove_playlist_title'].setEnabled(False)


            ''' BUTTONS - JUMP TO PLAYLIST '''
            cv.playlist_widget_dic[pl]['button_jump_to_playlist'] = ButtonJumpToPlaylist(
                self.inner_window, number_counter-1)
            cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setGeometry(
                BUTTON_2ND_POS_X,
                widget_pl_pos_y,
                self.LINE_EDIT_HIGHT,
                self.LINE_EDIT_HIGHT
                )
            if not line_edit_widget.text():
                cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(False)

            number_counter += 1
            widget_pl_pos_y += self.WIDGETS_NEXT_LINE_POS_Y_DIFF

        self.last_widget_pos_y = widget_pl_pos_y + self.EXTRA_HEIGHT_VALUE_AFTER_LAST_WIDGET_POS_Y




    def playlist_fields_validation_at_least_one_playlist(self):
        """
        Avoid removing all the playlist titles
        Avoid saving playlist titles over 25 char.s
        """
        pl_list_with_title = []
        for pl in cv.playlist_widget_dic:
            playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
            if len(playlist_title) > 25:
                playlist_title = f'{playlist_title[0:23]}..'
                cv.playlist_widget_dic[pl]['line_edit'].setText(playlist_title)
                MyMessageBoxError(
                    'PLAYLISTS TAB',
                    f'The more than 25 characters long  \n titles will be truncated:\n\n"{playlist_title}"')
            if len(playlist_title) != 0:
                pl_list_with_title.append(pl)
        if len(pl_list_with_title) == 0:
            MyMessageBoxError('PLAYLISTS TAB', 'At least one playlist title needed!')
        return pl_list_with_title


    def playlist_fields_validation_playing_playlist(self, pass_validation = True):
        """ Avoid removing the playing playlist """
        for pl in cv.playlist_widget_dic:
            playlist_index = cv.playlist_list.index(pl)
            new_playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
            prev_playlist_title = settings['playlists'][pl]['playlist_title']

            if (
                not new_playlist_title and
                prev_playlist_title and
                playlist_index == cv.playing_playlist_index and
                br.av_player.is_playing_or_paused()
                ):
                    cv.playlist_widget_dic[pl]['line_edit'].setText(prev_playlist_title)
                    MyMessageBoxError(
                        'PLAYLISTS TAB',
                        f'Playing playlist can not be removed, Playlist #{playlist_index+1}:  {prev_playlist_title}')
                    pass_validation = False
        return pass_validation


    def playlist_fields_validation_queued_track(self, pass_validation = True):
        """ Avoid removing playlists with queued track """
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


    def playlists_fields_to_save(self, to_save = False):
        for pl in cv.playlist_widget_dic:
            playlist_index = cv.playlist_list.index(pl)
            new_playlist_title = cv.playlist_widget_dic[pl]['line_edit'].text().strip()
            prev_playlist_title = settings['playlists'][pl]['playlist_title']

            if new_playlist_title != prev_playlist_title:

                # NEW TITLE, PREV: EMPTY - INVISIBLE
                if new_playlist_title and not prev_playlist_title:
                    br.playlists_all.setTabVisible(playlist_index, 1)
                    cv.playlists_without_title_to_hide_index_list.remove(playlist_index)
                    cv.playlist_widget_dic[pl]['button_remove_playlist_title'].setEnabled(True)
                    cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(True)

                # NEW TITLE: EMPTY, PREV: TITLE - VISIBLE
                elif not new_playlist_title and prev_playlist_title:
                    br.playlists_all.setTabVisible(playlist_index, 0)
                    cv.playlists_without_title_to_hide_index_list.append(playlist_index)
                    cv.playlist_widget_dic[pl]['button_remove_playlist_title'].setEnabled(False)
                    cv.playlist_widget_dic[pl]['button_jump_to_playlist'].setEnabled(False)
                    if cv.clear_playlist_at_playlist_remove:
                        clear_playlist_at_playlist_remove_action(pl)

                br.playlists_all.setTabText(playlist_index, new_playlist_title)
                settings['playlists'][pl]['playlist_title'] = new_playlist_title
                cv.playlist_widget_dic[pl]['playlist_title'] = new_playlist_title
                to_save = True

        if to_save:
            save_json()