from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout, QListWidget, QPushButton, QGridLayout
import sys
from qt_monitor import RealTimeDataTread


class MonitorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Monitor Window"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        """
        vbox = QVBoxLayout()
        plainText = QPlainTextEdit()
        plainText.setPlaceholderText("This is some text for our plaintextedit")

        plainText.setReadOnly(True)

        text = "Please subscribe the channel and like the videos"

        plainText.appendPlainText(text)

        plainText.setUndoRedoEnabled(False)

        vbox.addWidget(plainText)

        self.setLayout(vbox)
        """

        self.thread = RealTimeDataTread()
        self.listFile = QListWidget()
        self.btnStart = QPushButton("start")
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)
        self.btnStart.clicked.connect(self.slotStart)
        self.thread.signal.connect(self.slotAdd)

    def slotStart(self):
        self.btnStart.setEnabled(False)
        self.thread.start()

    def slotAdd(self,file_inf):
        self.listFile.addItem(file_inf)



