import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        #zhu表单布局，次水平布局
        layout=QFormLayout()
        sex=QHBoxLayout()

        #水平布局添加单选按钮
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))

        #表单布局添加控件
        layout.addRow(QLabel('性别'),sex)
        layout.addRow('生日',QLineEdit())

        #设置标题与布局
        self.setTabText(1,'个人详细信息')
        self.tab2.setLayout(layout)

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

        QVBLayout = QVBoxLayout()

        self.tab = TabSearch()
        self.textEdit = QTextEdit()
        self.button = QPushButton('开始')
        QVBLayout.addWidget(self.tab)
        QVBLayout.addWidget(self.button)
        QVBLayout.addWidget(self.textEdit)

        self.setLayout(QVBLayout)

        self.button.clicked.connect(self.start_search)

    def start_search(self):
        preburst_day_count = self.tab.comBox1.currentText()
        start_day_off = self.tab.comBox2.currentText()
        end_day_off = self.tab.comBox3.currentText()
        self.textEdit.setText("pre {} from {} to {}".format(preburst_day_count, start_day_off, end_day_off))
        return



if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=SearchWindow()
    demo.show()
    sys.exit(app.exec_())
