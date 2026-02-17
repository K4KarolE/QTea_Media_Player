""" Cheers all!
    https://www.geeksforgeeks.org/python/pyqt5-qtablewidget/
    https://www.qtcentre.org/threads/25952-Select-entire-row-in-QTableWidget-programmatically
"""

import sys
from PyQt6.QtWidgets import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 - QTableWidget'
        self.left = 800
        self.top = 500
        self.width = 300
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.show()


    def createTable(self):
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(4)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())