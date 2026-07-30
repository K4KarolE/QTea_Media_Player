"""
Source: https://www.pythonguis.com/faq/setstylesheet-get-colour-from-default-scheme/

Cheers Martin!
"""


import sys

from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Palette Colors")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QLineEdit styled with the system's AlternateBase color.
        palette = self.palette()
        alt_base = palette.color(QPalette.ColorRole.AlternateBase).name()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(
            f"Background set to AlternateBase ({alt_base})"
        )
        self.line_edit.setStyleSheet(
            f"QLineEdit {{ background: {alt_base}; }}"
        )
        layout.addWidget(self.line_edit)

        # Show a reference of current palette colors.
        form = QFormLayout()
        layout.addLayout(form)

        roles = {
            "Window": QPalette.ColorRole.Window,
            "WindowText": QPalette.ColorRole.WindowText,
            "Text": QPalette.ColorRole.Text,
            "Base": QPalette.ColorRole.Base,
            "AlternateBase": QPalette.ColorRole.AlternateBase,
            "Button": QPalette.ColorRole.Button,
            "ButtonText": QPalette.ColorRole.ButtonText,
            "Highlight": QPalette.ColorRole.Highlight,
            "HighlightedText": QPalette.ColorRole.HighlightedText,
            "Accent": QPalette.ColorRole.Accent,
            "Mid": QPalette.ColorRole.Mid,
            "MidLight": QPalette.ColorRole.Midlight
        }

        for name, role in roles.items():
            color = palette.color(role)
            color_hex = color.name()
            swatch = QLabel(f"  {color_hex}  ")
            swatch.setStyleSheet(
                f"background: {color_hex}; "
                f"color: {'white' if color.lightness() < 128 else 'black'}; "
                f"padding: 4px; "
                f"border: 1px solid gray;"
            )
            form.addRow(name, swatch)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())