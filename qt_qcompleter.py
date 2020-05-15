import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import pdb
################################################

df = pd.read_csv("basic-no3.csv", converters={"code": lambda x :str(x)})
#items_list = df["name"].to_list()
df_favorite = pd.read_csv("mystocklist_detail.csv", converters={"code": lambda x :str(x)})

df_new_all = pd.read_csv("new_stock_list.csv", converters={"code": lambda x :str(x)})

items_list = df["name"].to_list()

df_name = df.set_index("name")

list_list = ["所有股票", "自选股"]

################################################
class StockCompleter(QWidget):
    def __init__(self, canvas, *args, **kwargs):
        super(StockCompleter, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        self.stock_combobox = QComboBox(self, minimumWidth=200)
        self.stock_combobox.setEditable(True)

        self.list_combobox = QComboBox(self, minimumWidth=200)
        self.list_combobox.setEditable(True)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QLabel("名单选项", self))
        layout.addWidget(self.list_combobox)
        layout.addWidget(QLabel("股票名单", self))
        layout.addWidget(self.stock_combobox)

        #初始化combobox
        self.init_combobox()

        #增加选中事件
        self.stock_combobox.activated.connect(self.on_stock_combobox_Activate)
        self.list_combobox.activated.connect(self.on_list_combobox_Activate)

        self.canvas = canvas

    def init_combobox(self):
        # 增加选项元素
        for i in range(len(items_list)):
            self.stock_combobox.addItem(items_list[i])
        self.stock_combobox.setCurrentIndex(-1)

        for i in range(len(list_list)):
            self.list_combobox.addItem(list_list[i])
        self.list_combobox.setCurrentIndex(-1)

        # 增加自动补全
        completer = QCompleter(items_list)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.stock_combobox.setCompleter(completer)
        self.curindex_stock_combobox = self.stock_combobox.currentIndex()

        completer = QCompleter(list_list)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.list_combobox.setCompleter(completer)
        self.curindex_list_combobox = self.list_combobox.currentIndex()


    def on_stock_combobox_Activate(self, index):
        print(self.stock_combobox.count())
        print(self.stock_combobox.currentIndex())
        print(self.stock_combobox.currentText())
        print(self.stock_combobox.currentData())
        print(self.stock_combobox.itemData(self.stock_combobox.currentIndex()))
        print(self.stock_combobox.itemText(self.stock_combobox.currentIndex()))
        print(self.stock_combobox.itemText(index))

        name = self.stock_combobox.currentText()
        code = df_name.loc[name].code
        self.canvas.set_new_code(code, name)

    def on_list_combobox_Activate(self, index):
        print(self.list_combobox.count())
        print(self.list_combobox.currentIndex())
        print(self.list_combobox.currentText())
        print(self.list_combobox.currentData())
        print(self.list_combobox.itemData(self.list_combobox.currentIndex()))
        print(self.list_combobox.itemText(self.list_combobox.currentIndex()))
        print(self.list_combobox.itemText(index))

        """
        curidx = self.list_combobox.currentIndex()
        if self.curindex_list_combobox != curidx:
            pdb.set_trace()
            if curidx == 0:
                completer = QCompleter(items_list)
                completer.setFilterMode(Qt.MatchContains)
                completer.setCompletionMode(QCompleter.PopupCompletion)
                self.stock_combobox.setCompleter(completer)
            else:
                completer = QCompleter(favor_list)
                completer.setFilterMode(Qt.MatchContains)
                completer.setCompletionMode(QCompleter.PopupCompletion)
                self.stock_combobox.setCompleter(completer)

            self.curindex_list_combobox = curidx

        
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StockCompleter()
    w.show()
    sys.exit(app.exec_())
