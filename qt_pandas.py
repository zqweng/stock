import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt


df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class PandasTable(QTableView):

    def __init__(self, data):
        super().__init__()
        model = PandasModel(data)
        self.setModel(model)


class PandasWidget(QWidget):

    def __init__(self, data):
        super().__init__()

        title = "Pandas Table"
        top = 0
        left = 0
        width = 1200
        height = 1200

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        table = PandasTable(data)

        layout = QVBoxLayout()

        layout.addWidget(table)
        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = PandasWidget(df)
    table.resize(800, 600)
    table.show()
    sys.exit(app.exec_())