import socket

# Set up the server to listen on a specific IP and port
def start_server():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 5002        # Port to listen on

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connection received from {addr}")

    while True:
        command = input("Shell> ")
        if command.lower() == 'quit':
            conn.send(command.encode('utf-8'))
            conn.close()
            break

        if command.strip():
            conn.send(command.encode('utf-8'))
            response = conn.recv(1024).decode('utf-8')
            print(response)

if __name__ == "__main__":
    start_server()
