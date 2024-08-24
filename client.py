import socket
import tkinter as tk
from PIL import ImageGrab
import io

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Client - Screen Sender')

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.200.27', 9999))

        self.start_button = tk.Button(master, text='Start Sharing', command=self.start_sharing)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text='Stop Sharing', command=self.stop_sharing)
        self.stop_button.pack()
        self.stop_button.config(state='disabled')

        self.sending = False

    def start_sharing(self):
        self.sending = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.send_screen()

    def send_screen(self):
        if self.sending:
            # Capture the screen
            screen = ImageGrab.grab()
            buffer = io.BytesIO()
            screen.save(buffer, format='JPEG')
            image_data = buffer.getvalue()

            # Send the size of the image
            self.client_socket.send(len(image_data).to_bytes(4, 'big'))
            # Send the actual image data
            self.client_socket.sendall(image_data)

            # Continuously send the screen data every 100ms for a smoother live stream
            self.master.after(100, self.send_screen)

    def stop_sharing(self):
        self.sending = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

        self.client_socket.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
