import sys

from PySide.QtCore import *
from PySide.QtGui import *

class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()

        self.table = Table(self)
        self.change = QPushButton('Change')

        layout = QHBoxLayout(self)

        layout.addWidget(self.table)
        layout.addWidget(self.change)

        self.change.clicked.connect(self.table.updateCell)

class Table(QTableWidget):

    def __init__(self, parent=None):
        super(Table, self).__init__(2, 2, parent)
        self.setItem(1, 0, QTableWidgetItem('test'))
        self.setItem(1, 1, QTableWidgetItem('False'))

    def updateCell(self):

        item, = self.findItems('test', Qt.MatchExactly)
        new = repr(not eval(self.item(item.row(), 1).text()))
        self.item(row, 1).setText(new)


app = QApplication([])
main = Main()
main.show()
app.exec_()