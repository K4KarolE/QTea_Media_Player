from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from .class_bridge import br


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
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Warning - Queued track')
        self.setWindowIcon(br.icon.settings)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText('There is a queued track in the playlist!  ' + 
            'It will be removed from the queue list.\n\n' +
            'Do you want to clear the playlist?')
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.clicked_value = self.exec()

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
        self.exec()