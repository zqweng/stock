import sys
from PyQt5.QtWidgets import *
from qt_qcompleter import *
from qt_pandas import *
import glob
import pandas

class ProfitTable(QTableWidget):
    def __init__(self):
        super(ProfitTable, self).__init__()
        self.setWindowTitle("自选股实时行情")  #

        column_name_list = [
            "每股现金收益",
            "主营收入",
            "同比增长",
            "净利润",
            "同比增长"
        ]

        self.setColumnCount(len(column_name_list))  # 设置列数
        self.setHorizontalHeaderLabels(column_name_list)  # 设置列名称

        self.setRowCount(1)  # 设置行数
        self.setVerticalHeaderLabels(["row1"])  # 设置行名称


class InfoTable(QWidget):
    def __init__(self):
        super(InfoTable,self).__init__()

        title = "Info Table"
        top = 0
        left = 0
        width = 1200
        height = 1200

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.MyUI()

    def MyUI(self):
        #self.profit_table = ProfitTable()
        self.textEdit = QTextEdit()
        self.vlayerout = QVBoxLayout()
        self.completer = StockCompleter(self)

        QVBLayout = QVBoxLayout()

        QVBLayout.addWidget(self.textEdit)
        QVBLayout.addLayout(self.vlayerout)
        QVBLayout.addWidget(self.completer)

        self.setLayout(QVBLayout)


        self.textEdit.setText("营业利润=营业收入-营业成本-税金及附加-销售费用-财务费用-研发费用-财务费用-资产减值损失"
                              "+其他收益+投资收益（-投资损失）+允价值变动收益（-变动损失）+资产处置收益（-处置损失）")

        hlayerout = QHBoxLayout()
        self.comBox = QComboBox()
        self.comBox.addItems(["研发收入比"])
        self.lineEdit = QLineEdit("10")

        # row 1
        hlayerout.addWidget(self.comBox)
        hlayerout.addWidget(QLabel("大于"))
        hlayerout.addWidget(self.lineEdit)

        # row 2
        button = QPushButton("开始搜索")
        button.clicked.connect(self.on_start_search)

        # add row 1/2
        self.vlayerout.addLayout(hlayerout)
        self.vlayerout.addWidget(button)


    def on_start_search(self):
        percentage = int(self.lineEdit.text())
        self.func_1(percentage)

    def func_1(self, per):

        for filepath in glob.iglob('财报/*.csv'):
            df = pandas.read_csv(filepath)

            if not "2020-03-31" in df.columns:
                continue

            invest = df.loc[df["报告日期"] == "研发费用(万元)"].iloc[0]["2020-03-31"]
            income = df.loc[df["报告日期"] == "营业总收入(万元)"].iloc[0]["2020-03-31"]
            pps = df.loc[df["报告日期"] == "基本每股收益"].iloc[0]["2020-03-31"]

            if (income == "--" or invest == "--" or pps == "--" or
                    float(pps) <=0.1 or float(income) == 0):
                continue

            ratio = float(invest)/float(income)
            if ratio >= per/100:
                print("{} has ration {} pps {}".format(filepath, ratio, float(pps)))


    def set_new_code(self, code, name):
        print(code)
        df = pd.read_csv("财报/{}.csv".format(code))
        self.widget = PandasWidget(df)
        self.widget.show()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=InfoTable()
    demo.show()
    sys.exit(app.exec_())

