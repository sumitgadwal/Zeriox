import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen, QImage
from PyQt5.QtCore import QTimer, QBuffer, QIODevice
from socket import socket, AF_INET, SOCK_STREAM
import struct

class ScreenSender:
    def __init__(self):
        # Create a socket object
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        # Connect to the server
        self.client_socket.connect(('172.26.136.52', 4444))  # Replace with the correct server IP and port

        # Create a QScreen object to capture the screen
        self.screen = QApplication.primaryScreen()

        # Timer to capture and send the screen image more frequently
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_screen)
        self.timer.start(100)  # Send every 100ms

    def send_screen(self):
        try:
            # Capture the screen
            screenshot = self.screen.grabWindow(0)
            image = screenshot.toImage()

            # Convert QImage to bytes using QBuffer
            buffer = QBuffer()
            buffer.open(QIODevice.ReadWrite)
            image.save(buffer, "JPEG", quality=50)  # Save as JPEG with reduced quality
            image_data = buffer.data()

            # First send the length of the data
            self.client_socket.sendall(struct.pack('>I', len(image_data)))

            # Then send the actual image data
            self.client_socket.sendall(image_data)
        except Exception as e:
            print(f"Error sending image: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = ScreenSender()
    sys.exit(app.exec_())
