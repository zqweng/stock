#!usr/bin/python3
# -*- coding:utf-8 -*-
# author:SingWeek

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, time


class MyTable(QTableWidget):
    def __init__(self, parent=None):
        super(MyTable, self).__init__(parent)
        self.setWindowTitle("Test")  # 设置表格名称
        # self.resize(600, 200)  # 设置表格尺寸（整体大小）
        self.Config_Set = QGroupBox("Test")
        self.Text = QLineEdit("显示")
        self.CBtn = QPushButton("开始")
        self.Click = QPushButton("打印")
        self.NTime = QLineEdit("")
        layout = QGridLayout()
        layout.addWidget(self.CBtn, 1, 1)
        layout.addWidget(self.Text, 2, 1)
        layout.addWidget(self.Click, 3, 1)
        layout.addWidget(self.NTime, 4, 1)
        self.Config_Set.setLayout(layout)

        mainLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()
        hboxLayout.addStretch()
        hboxLayout.addWidget(self.Config_Set)  # 横向添加表格块
        mainLayout.addLayout(hboxLayout)
        self.setLayout(mainLayout)

        self.CBtn.clicked.connect(self.Btn)
        self.Click.clicked.connect(self.Print)

    def Print(self):
        self.NTime.setText("当前系统时间" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("当前系统时间" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def Btn(self):
        calcnum = 100000
        update_data_thread = UpdateData(calcnum)  #
        update_data_thread.update_date.connect(self.update_item_data)  # 链接信号
        update_data_thread.run()

    def update_item_data(self, data):
        """更新内容"""
        self.Text.setText(data)


class UpdateData(QThread):
    """界面和 运行相分离，通过信号与槽来进行参数传递"""
    update_date = pyqtSignal(str)  # pyqt5 支持python3的str，没有Qstring

    def __init__(self, data, parent=None):
        super(UpdateData, self).__init__(parent)
        self.data = data

    def run(self):
        calc(self.data, self.update_date)


def calc(data, update_date):
    """
    下面可以是其他相应的功能函数
    :param update_date:
    :return:
    """
    cnt = 0
    while True:
        cnt += 1
        update_date.emit(str(cnt))  # 发射信号
        # time.sleep(1)
        if cnt >= data:
            cnt = 0
        QApplication.processEvents()  # 刷新界面，避免卡顿


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    app.exit(app.exec_())

