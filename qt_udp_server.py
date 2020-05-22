
from PyQt5.QtCore import *
import socket
import pandas as pd
import pdb
from qt_pandas import *
import json

local_ip    = "127.0.0.1"

class QUdpServer(QThread):

    signal = pyqtSignal(str)

    def __init__(self, bind_port=20001, parent =None):
        super(QUdpServer, self).__init__(parent)

        self.socket_buffer_size = 1024000
        self.local_port = bind_port
        self.socket_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket_server.bind((local_ip, self.local_port))

    def run(self):
        #while (False):
        receive_tuple = self.socket_server.recvfrom(self.socket_buffer_size)
        print("receve something")
        message = receive_tuple[0]
        address = receive_tuple[1]

        self.signal.emit(message.decode("utf-8"))



