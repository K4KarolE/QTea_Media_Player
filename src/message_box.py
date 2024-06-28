from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from .icons import MyIcon


class MyMessageBoxError(QMessageBox):
    def __init__(self, tab_title, message):
        super().__init__()
        self.setWindowTitle(f'ERROR - {tab_title}')
        self.setWindowIcon(MyIcon().settings)
        self.setIcon(QMessageBox.Icon.Warning)
        # extra whitespace:
        # position the text more to the middle in the box
        self.setText(message + ' ' * 8) 
        self.setStandardButtons(QMessageBox.StandardButton.Close)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.exec()
