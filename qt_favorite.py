# code:utf-8
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from qt_qcompleter import StockCompleter
import pandas as pd
from qt_realtime_thread import QRealTimeTread
import json
import pdb


class FavoriteTable(QTableWidget):
    def __init__(self, parent=None):
        super(FavoriteTable, self).__init__(parent)

        self.row_name = self.get_favorite_list()
        self.name2row_map = {i[1]: i[0] for i in enumerate(self.row_name)}
        self.setRowCount(len(self.row_name))  # 设置行数

        # self.setColumnWidth(0, 200)  # 设置列宽(第几列， 宽度)
        # self.setRowHeight(0, 100)  # 设置行高(第几行， 行高)
        self.col_map = {"open": 4, "name": 0, "pre_close": 5, "price": 3, "time": 7, "code": 1, "volume": 6, "p_change": 2 }
        column_name = [
            '名称',
            '代码',
            '涨幅',
            '现价',
            '开盘',
            '昨收盘',
            '成交量',
            '时间'

        ]
        self.setColumnCount(len(column_name))  # 设置列数

        self.setHorizontalHeaderLabels(column_name)  # 设置列名称
        self.setVerticalHeaderLabels([str(i[0]) for i in enumerate(self.row_name)])  # 设置行名称


        #header = self.horizontalHeader()
        #for i in range(0,len(column_name)):
            #header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.thread = QRealTimeTread()
        self.thread.signal.connect(self.update_stock_data)
        self.thread.start()

    def update_item_data(self, data):
        """更新内容"""
        self.setItem(0, 0, QTableWidgetItem(data))  # 设置表格内容(行， 列) 文字

    def update_stock_data(self, data):
        """更新内容"""
        dic = json.loads(data)
        #print(data)
        self.setSortingEnabled(False)

        for index, values in dic.items():
            row = int(self.name2row_map[values["name"]])
            col = 0
            for colname, value in values.items():
                col = self.col_map[colname]
                nameItem = QTableWidgetItem()
                if type(value) == int or type(value) == float:
                    nameItem.setData(Qt.DisplayRole, value)
                else:
                    nameItem.setText(value)
                self.setItem(row, col, nameItem)
                #del nameItem #不要忘了释放内存

        self.sortByColumn(2, Qt.DescendingOrder)

    def get_favorite_list(self):
        df = pd.read_csv("mystocklist_detail.csv", converters={"code": lambda x: str(x)})
        return df["name"].to_list()

    def __del__(self):
        print('Destructor called, Employee deleted.')
        self.thread.stop()



class FavoriteWindow(QWidget):
    def __init__(self, parent=None):
        super(FavoriteWindow, self).__init__(parent)

        top = 0
        left = 0
        width = 1000
        height = 1000

        self.setGeometry(top, left, width, height)

        self.table = FavoriteTable()
        self.OpenBtn = QPushButton("添加")

        QVBLayout = QVBoxLayout()
        QVBLayout.addWidget(self.table)
        QVBLayout.addWidget(self.OpenBtn)

        self.setLayout(QVBLayout)

        self.OpenBtn.clicked.connect(self.Connect)
        self.setWindowTitle("Favorite")


    def Connect(self):
        self.stockCompleter = StockCompleter(self)
        self.stockCompleter.show()
        #self.stockCompleter.switchSig.connect(self.table.update_stock_data)


if __name__ == '__main__':
    # 实例化表格
    app = QApplication(sys.argv)
    myTable = MyTable()
    # 启动更新线程
    update_data_thread = UpdateData()
    update_data_thread.update_date.connect(myTable.update_item_data)  # 链接信号
    update_data_thread.start()

    # 显示在屏幕中央
    desktop = QApplication.desktop()  # 获取坐标
    x = (desktop.width() - myTable.width()) // 2
    y = (desktop.height() - myTable.height()) // 2
    myTable.move(x, y)  # 移动

    # 显示表格
    myTable.show()
    app.exit(app.exec_())
