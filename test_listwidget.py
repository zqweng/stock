# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ListWidget(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "你选择了: " + item.text())  # 显示出消息提示框


if __name__ == '__main__':
    app = QApplication(sys.argv)
    listWidget = ListWidget()  # 创建一个listWidget  实例
    listWidget.resize(300, 120)  # 定义尺寸大小
    listWidget.addItem("Item 1");  # 添加item
    listWidget.addItem("Item 2");
    listWidget.addItem("Item 3");
    listWidget.addItem("Item 4");
    listWidget.setWindowTitle('QListwidget 例子')  # 设置标题
    listWidget.itemClicked.connect(listWidget.clicked)  # 绑定点击事件
    listWidget.show()
    sys.exit(app.exec_())
