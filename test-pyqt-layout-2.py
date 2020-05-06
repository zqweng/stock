#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:SingWeek
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class prowler(QWidget):
    switchSig = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(prowler, self).__init__(parent)

        self.sendData = {"first": "I", "second": "Love", "third": "You"}

        self.SendBtn = QPushButton("向父界面传值1")
        self.SendEdit = QLineEdit()
        self.SendBtn1 = QPushButton("向父界面传值2")
        self.SendEdit1 = QLineEdit()

        layout = QGridLayout()
        layout.addWidget(self.SendBtn, 0, 0)
        layout.addWidget(self.SendEdit, 0, 1)
        layout.addWidget(self.SendBtn1, 1, 0)
        layout.addWidget(self.SendEdit1, 1, 1)

        QHBLayout = QHBoxLayout()
        QVBLayout = QVBoxLayout()

        QHBLayout.addLayout(layout)
        QVBLayout.addLayout(QHBLayout)
        #QVBLayout.addLayout(layout)

        self.setLayout(QVBLayout)
        self.SendBtn.clicked.connect(self.SendData)
        self.SendBtn1.clicked.connect(self.SendData1)

        self.setWindowTitle("Son")

    def SendData(self):
        tmp = self.SendEdit.text()
        print("向父界面发送的值", tmp)
        self.sendData["first"] = tmp
        print("向父界面发送的字典", self.sendData)
        self.switchSig.emit(self.sendData)

    def SendData1(self):
        tmp = self.SendEdit1.text()
        print("向父界面发送的值", tmp)
        self.sendData["second"] = tmp
        print("向父界面发送的字典", self.sendData)
        self.switchSig.emit(self.sendData)


class main(QWidget):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)

        self.sendData = {"first": "I", "second": "Love", "third": "You"}

        self.OpenBtn = QPushButton("呼唤子界面")
        self.OpenEdit = QLineEdit()
        self.ShowBtn = QPushButton("显示")
        self.ShowEdit = QLineEdit()
        self.ShowBtn1 = QPushButton("显示1")
        self.ShowEdit1 = QLineEdit()

        layout = QGridLayout()
        layout.addWidget(self.OpenBtn, 0, 0)
        layout.addWidget(self.OpenEdit, 0, 1)
        layout.addWidget(self.ShowBtn, 1, 0)
        layout.addWidget(self.ShowEdit, 1, 1)
        layout.addWidget(self.ShowBtn1, 2, 0)
        layout.addWidget(self.ShowEdit1, 2, 1)

        QHBLayout = QHBoxLayout()
        QVBLayout = QVBoxLayout()

        QHBLayout.addLayout(layout)
        QVBLayout.addLayout(QHBLayout)

        self.setLayout(QVBLayout)

        self.OpenBtn.clicked.connect(self.Connect)
        self.setWindowTitle("Father")

    def Connect(self):
        self.widget = prowler()
        self.widget.show()
        self.widget.switchSig.connect(self.reaction)

    def reaction(self, string):
        print("父界面接收到的字典", string)
        self.sondata = string
        tmp = self.sondata["first"]
        print("父界面接收到的值", tmp)
        self.ShowEdit.setText(tmp)
        tmp1 = self.sondata["second"]
        print("父界面接收到的值1", tmp1)
        self.ShowEdit1.setText(tmp1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Jenney = main()
    Jenney.show()
    sys.exit(app.exec_())
