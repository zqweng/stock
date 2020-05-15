
from PyQt5.QtCore import *
import pdb
from qt_search_cmd import *
import json

cmd_dict = {"counting_break_upper_band_after_n": counting_break_upper_band_after_n}

class QWorkerTread(QThread):

    signal = pyqtSignal(str)

    def __init__(self, command_list =[], parent =None):
        super(QWorkerTread, self).__init__(parent)

        self.cmd_list = command_list

    def run(self):
        for command_dic in self.cmd_list:
            command_string = command_dic["command"]
            print("start exec {}".format(command_string))
            del command_dic["command"]
            df = cmd_dict[command_string](self.signal, **command_dic)
            self.signal.emit(df.to_string())
            #exec(cmd)



