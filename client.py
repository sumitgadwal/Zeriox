# client_gui.py

import sys
import cv2
import numpy as np
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = QTimer()

    def initUI(self):
        self.setWindowTitle('Client - Screen Sender')
        self.setGeometry(100, 100, 300, 100)

        self.start_btn = QPushButton('Start Sharing', self)
        self.start_btn.clicked.connect(self.start_sharing)

        self.stop_btn = QPushButton('Stop Sharing', self)
        self.stop_btn.clicked.connect(self.stop_sharing)
        self.stop_btn.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_sharing(self):
        self.timer.timeout.connect(self.send_screen)
        self.timer.start(30)  # Send a frame every 30ms

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def send_screen(self):
        screen = np.array(cv2.cvtColor(np.array(cv2.VideoCapture(0).read()[1]), cv2.COLOR_BGR2RGB))
        _, buffer = cv2.imencode('.jpg', screen, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        self.client_socket.sendto(buffer, ('192.168.200.27', 9999))

    def stop_sharing(self):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientApp()
    ex.show()
    sys.exit(app.exec_())
