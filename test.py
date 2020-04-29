#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we connect a signal
of a QSlider to a slot of a QLCDNumber.

Author: Jan Bodnar
Website: zetcode.com
Last edited: January 2017
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def printLabel(self, str):
        print(str)

    def logLabel(self, str):
        '''log to a file'''
        pass

    @QtCore.pyqtSlot(int)
    def on_sld_valueChanged(self, value):
        self.lcd.display(value)
        self.printLabel(value)
        self.logLabel(value)

    def initUI(self):

        self.lcd = QLCDNumber(self)
        self.sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.sld)

        self.setLayout(vbox)
        self.sld.valueChanged.connect(self.on_sld_valueChanged)


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')