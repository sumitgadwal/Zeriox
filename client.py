# client_gui.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from vidstream import ScreenShareClient
import threading

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sender = None
        self.thread = None

    def initUI(self):
        self.setWindowTitle('Client Control')
        self.setGeometry(100, 100, 300, 100)

        self.start_btn = QPushButton('Start Client', self)
        self.start_btn.clicked.connect(self.start_client)

        self.stop_btn = QPushButton('Stop Client', self)
        self.stop_btn.clicked.connect(self.stop_client)
        self.stop_btn.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_client(self):
        self.sender = ScreenShareClient("192.168.200.27", 4525)
        self.thread = threading.Thread(target=self.sender.start_stream)
        self.thread.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_client(self):
        if self.sender:
            self.sender.stop_stream()
        self.thread.join()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientApp()
    ex.show()
    sys.exit(app.exec_())
