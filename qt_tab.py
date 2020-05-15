import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_work_thread import QWorkerTread
from qt_search_cmd import *
import threading
import json
import pdb
import gzip
import pickle

price_list = ["close","ma20","upper"]
type_list = ["day","60","30"]

class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)

        hlayout = QHBoxLayout()
        self.cbOffsetFrom = QComboBox()
        self.cbOffsetFrom.addItems([str(i) for i in range(0, 50)])
        self.cbOffsetTo = QComboBox()
        self.cbOffsetTo.addItems([str(i) for i in range(0, 50)])

        self.cbCmpDataType = QComboBox()
        self.cbCmpDataType.addItems([type for type in type_list])

        self.cbCmpData1 = QComboBox()
        self.cbCmpData1.addItems([price for price in price_list])

        self.cbCmpData2 = QComboBox()
        self.cbCmpData2.addItems([price for price in price_list])
        self.cbCmpData2.setEditable(True)

        self.cbOffsetFrom.setCurrentIndex(-1)
        self.cbOffsetTo.setCurrentIndex(-1)

        #
        hlayout.addWidget(QLabel(" From offset"))
        hlayout.addWidget(self.cbOffsetFrom)
        hlayout.addWidget(QLabel(" To offset"))
        hlayout.addWidget(self.cbOffsetTo)
        hlayout.addWidget(self.cbCmpDataType)
        hlayout.addWidget(self.cbCmpData1)
        hlayout.addWidget(QLabel("大于"))
        hlayout.addWidget(self.cbCmpData2)
        self.setLayout(hlayout)

    def get_command_list(self):
        if (self.cbOffsetFrom.currentIndex() != -1 and
            self.cbOffsetTo.currentIndex() != -1):
            #
            start_day_off = int(self.cbOffsetFrom.currentText())
            end_day_off = int(self.cbOffsetTo.currentText())
            command_dic = {
                "start_offset": start_day_off,
                "end_offset": end_day_off,
                "cross_over": (self.cbCmpData1.currentText(), self.cbCmpData2.currentText()),
                "period_type": self.cbCmpDataType.currentText()
            }

            return command_dic
        else:
            return None

    def set_values(self, dict):

        self.cbOffsetFrom.setCurrentText(str(dict["start_offset"]))
        self.cbOffsetTo.setCurrentText(str(dict["end_offset"]))
        self.cbCmpData1.setCurrentText(str(dict["cross_over"][0]))
        self.cbCmpData2.setCurrentText(str(dict["cross_over"][1]))
        self.cbCmpDataType.setCurrentText(str(dict["period_type"]))



class TabSearch(QTabWidget):
    def __init__(self,parent=None):
        super(TabSearch, self).__init__(parent)


        #创建3个选项卡小控件窗口
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()

        #将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        #每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        #表单布局
        layout=QFormLayout()

        #
        self.comBox1 = QComboBox()
        self.comBox1.addItems([str(i) for i in range(3,20)])
        layout.addRow('突破前整理天数大于',self.comBox1)

        day_range = QHBoxLayout()

        self.comBox2 = QComboBox()
        self.comBox2.addItems([str(i) for i in range(0, 50)])
        self.comBox3 = QComboBox()
        self.comBox3.addItems([str(i) for i in range(0, 50)])
        day_range.addWidget(self.comBox2)
        day_range.addWidget(QLabel("到", alignment=Qt.AlignCenter))
        day_range.addWidget(self.comBox3)
        #self.label.setAlignment(Qt.AlignCenter)

        layout.addRow('时间从：',day_range)
        #设置选项卡的小标题与布局方式
        self.setTabText(0,'突破布林上轨')
        self.tab1.setLayout(layout)

    def tab2UI(self):

        self.searchWidgetList = []
        self.searchWidgetNum = 3

        for i in range(self.searchWidgetNum):
            self.searchWidgetList.append(SearchWidget())

        vlayout = QVBoxLayout()

        for widget in self.searchWidgetList:
            vlayout.addWidget(widget)

        # 设置选项卡的小标题与布局方式
        self.setTabText(1, '通用')
        self.tab2.setLayout(vlayout)

    def tab3UI(self):
        #水平布局
        layout=QHBoxLayout()

        #添加控件到布局中
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        #设置小标题与布局方式
        self.setTabText(2,'教育程度')
        self.tab3.setLayout(layout)

class SearchWindow(QWidget):
    def __init__(self, parent=None):
        super(SearchWindow, self).__init__(parent)

        top = 0
        left = 0
        width = 1000
        height = 1000

        self.setGeometry(top, left, width, height)
        self.setWindowTitle("Search")

        self.pickle_data = []

        QVBLayout = QVBoxLayout()

        self.tab = TabSearch()
        hlayout = QHBoxLayout()
        self.listWidget = QListWidget()
        self.textEdit = QTextEdit()

        self.buttonStart = QPushButton('开始')
        self.buttonSave = QPushButton('存盘')
        self.buttonLoad = QPushButton('加载')
        self.buttonDelete = QPushButton('删除')
        hlayout.addWidget(self.buttonStart)
        hlayout.addWidget(self.buttonSave)
        hlayout.addWidget(self.buttonLoad)
        hlayout.addWidget(self.buttonDelete)

        QVBLayout.addWidget(self.tab)
        QVBLayout.addLayout(hlayout)
        QVBLayout.addWidget(self.listWidget)
        QVBLayout.addWidget(self.textEdit)

        self.setLayout(QVBLayout)

        self.buttonStart.clicked.connect(self.on_search)
        self.buttonSave.clicked.connect(self.on_save)
        self.buttonLoad.clicked.connect(self.on_load)
        self.buttonDelete.clicked.connect(self.on_delete)

        if os.path.isfile("search.pkl"):
            self.pickle_data = self.load_pickle("search.pkl")
            for item in self.pickle_data:
                self.listWidget.addItem(item[0])

    def load_pickle(self, filename):
        # open a file, where you stored the pickled data
        file = open(filename, 'rb')

        # dump information to that file
        data = pickle.load(file)

        # close the file
        file.close()

        return data

    def save_pickle(self, filename, data):
        # open a file, where you ant to store the data
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(data, file)

        # close the file
        file.close()

    def on_delete(self):
        index = self.listWidget.currentRow()

        if index == -1:
            return

        del self.pickle_data[index]
        item = self.listWidget.takeItem(index)
        del item
        self.save_pickle("search.pkl", self.pickle_data)

    def on_load(self):
        index = self.listWidget.currentRow()
        if index == -1:
            return
        command_list_tuple = self.pickle_data[index]
        for index, command_dict in enumerate(command_list_tuple[1]):
            print("index {}, comand {}".format(index, command_dict))
            self.tab.searchWidgetList[index].set_values(command_dict)



    def on_save(self):
        text, okPressed = QInputDialog.getText(self, "save search","search name:", QLineEdit.Normal, "30min_day_with_20ma")
        if okPressed and text != '':

            list =  self.listWidget.findItems(text, Qt.MatchExactly)
            if len(list) == 0:
                self.listWidget.addItem(text)
                search_list = self.get_search_list()
                self.pickle_data.append((text, search_list))

                self.save_pickle("search.pkl", self.pickle_data)

            else:
                QMessageBox.question(self, 'PyQt5 message', "search exist!", QMessageBox.Yes)



    def get_search_list(self):
        command_list = []
        for widget in self.tab.searchWidgetList:
            command_dic = widget.get_command_list()
            if command_dic != None:
                command_list.append(command_dic)

        return command_list

    def on_search(self):
        index = self.tab.currentIndex()

        if index == 0:
            self.on_tab1()
        elif index == 1:
            command_list = self.get_search_list()

            if len(command_list) > 0:
                thread = threading.Thread(target=search_func, args=(command_list,))
                thread.start()
            else:
                print("empty command")

    def on_tab1(self):
        preburst_day_count = int(self.tab.comBox1.currentText())
        start_day_off = int(self.tab.comBox2.currentText())
        end_day_off = int(self.tab.comBox3.currentText())
        exec_string = """ """
        self.textEdit.setText("pre {} from {} to {}".format(preburst_day_count, start_day_off, end_day_off))
        command_dic = {
                   "command": "counting_break_upper_band_after_n",
                   "start_offset": start_day_off,
                   "end_offset": end_day_off,
                   "num":  preburst_day_count
        }

        thread = QWorkerTread(command_list = [command_dic])
        thread.signal.connect(self.log_search)
        thread.run()


    def log_search(self, string):
        self.textEdit.setText(string)

    def closeEvent(self, event):
        print("X is clicked")


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=SearchWindow()
    demo.show()
    sys.exit(app.exec_())
