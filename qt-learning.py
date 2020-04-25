from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pdb


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Matplotlib Embeding In PyQt5"
        top = 400
        left = 400
        width = 900
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.MyUI()

    def MyUI(self):
        self.canvas = Canvas(self, width=8, height=4)
        self.canvas.move(0, 0)

        button = QPushButton("向前", self)
        button.move(100, 450)
        button.clicked.connect(self.slot_method)

        button2 = QPushButton("向后", self)
        button2.move(250, 450)

    def slot_method(self):
        self.canvas.clear_fig()
        self.canvas.plot_next()
        self.canvas.draw()

class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axe = self.fig.subplots()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.plot()

    def plot(self):
        x = np.array([50, 30, 40])
        labels = ["Apples", "Bananas", "Melons"]
        self.axe.pie(x, labels=labels)

    def plot_next(self):
        x = np.array([5, 3, 40])
        labels = ["Apples", "Bananas", "Meeeeeeee"]
        self.axe.pie(x, labels=labels)

    def clear_fig(self):
        self.fig.clf()
        self.axe = self.fig.subplots()


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()