import sys
from PyQt5.QtWidgets import *
from qt_qcompleter import *
from qt_pandas import *
import glob
import pandas


class SellDiagnoseWindow(QWidget):
    def __init__(self):
        super(SellDiagnoseWindow,self).__init__()

        title = "Info Table"
        top = 0
        left = 0
        width = 1200
        height = 1200

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.MyUI()

    def MyUI(self):

        self.textEdit = QTextEdit()

        QVBLayout = QVBoxLayout()

        QVBLayout.addWidget(self.textEdit)

        self.setLayout(QVBLayout)


        self.textEdit.setText("卖股票需要看从小时线上观察量， 是不是上涨有量，下跌无量，如果是就不要卖。\n"
                              "如果高位放量就要考虑要不要卖。 \n"
                              "从价格说，如果一直站在五小时线上，就不要卖。"
                              "紫光国微 金发科技 雅克科技 漫步者 中航高科 ")



if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=SellDiagnoseWindow()
    demo.show()
    sys.exit(app.exec_())

