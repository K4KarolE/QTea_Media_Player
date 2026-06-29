from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from .class_bridge import br

"""
LEARNED:
It looks like the msg box can not handle text with a line break where 
the second line (any later in the text) is longer than the first one.

Example:
string_to_print = ('            random text'
                  '            longer random text')
                  
Adding "\n" line break at end of the first line does not fix the issue

Solution: 
- add extra whitespace at the end of the first line
    to make the msg box wider: 'random text      '
- truncate all the text following the first line if you think
    the length of the text can be greater than the first line
"""


class MyMessageBoxError(QMessageBox):
    def __init__(self, tab_title, message):
        super().__init__()
        self.setWindowTitle(f'ERROR - {tab_title}')
        self.setWindowIcon(br.icon.settings)
        self.setIcon(QMessageBox.Icon.Warning)
        # extra whitespace:
        # position the text more to the middle in the box
        self.setText(message + ' ' * 8) 
        self.setStandardButtons(QMessageBox.StandardButton.Close)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.exec()


class MyMessageBoxWarning(QMessageBox):
    def __init__(self, msg_type:str):
        super().__init__()
        if msg_type == 'queued':
            self.set_msg_box_queued_track_in_playlist()
        elif msg_type == 'played':
            self.set_msg_box_played_track_in_playlist()
        self.setWindowIcon(br.icon.settings)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.clicked_value = self.exec()

    def set_msg_box_queued_track_in_playlist(self):
        self.setWindowTitle('Warning - Queued track')
        self.setText('There is a queued track in the playlist!  ' +
                     'It will be removed from the queue list.\n\n' +
                     'Do you want to clear the playlist?')

    def set_msg_box_played_track_in_playlist(self):
        self.setWindowTitle('Warning - Played track')
        self.setText('There is a playing track in the playlist!  \n\n' +
                     'Do you want to clear the playlist?')

    def clicked_continue(self):
        if self.clicked_value == 16384: #Yes
            return True
        else:
            return False


class MyMessageBoxConfReq(QMessageBox):
    def __init__(self, question, function):
        super().__init__()
        self.setWindowTitle('Confirmation needed')
        self.setWindowIcon(br.icon.settings)
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(question)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.accepted.connect(function)
        self.exec()


class MyMessageBoxConfirmation(QMessageBox):
    def __init__(self, window_title, message):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setWindowIcon(br.icon.settings)
        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.exec()