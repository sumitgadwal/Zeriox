import socket
import io
from PIL import ImageGrab
import time

def send_screen(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    while True:
        try:
            # Capture the screen
            screen = ImageGrab.grab()
            buffer = io.BytesIO()
            screen.save(buffer, format="PNG")
            image_data = buffer.getvalue()
            image_size = len(image_data)

            # Send the image size first
            client_socket.sendall(image_size.to_bytes(4, byteorder='big'))

            # Send the image data
            client_socket.sendall(image_data)

            # Sleep for a short period to control the frame rate
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    send_screen("192.168.200.27", 65432)
