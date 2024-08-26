import socket
import argparse
import time
import sys

def scan_ports(target, port_range):
    open_ports = []
    start_time = time.time()
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.05)  # Reducing the timeout for faster scanning
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
        # Check if the scanning process is exceeding 10 seconds
        if time.time() - start_time > 10:
            break
    return open_ports

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write("\n".join(data))

def show_animation():
    animation = "|/-\\"
    for i in range(20):  # Simple loop to show an animation for ~2 seconds
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    sys.stdout.write("\r")  # Clear the animation line

def display_title():
    print(r"""
       _____                 _                     
      |__  /___  _ __   __ _| | _____ _ __ ___  ___ 
        / // _ \| '_ \ / _` | |/ / _ \ '__/ __|/ _ \
       / /| (_) | | | | (_| |   <  __/ |  \__ \  __/
      /____\___/|_| |_|\__,_|_|\_\___|_|  |___/\___|
       Zeriox Open Nmap - Ethical Port Scanning Tool
    """)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeriox Open Nmap - Ethical Port Scanning Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("output_file", help="Output file to save the results")
    parser.add_argument("--port_range", default="1-1024", help="Range of ports to scan (e.g., 1-1024). Defaults to 1-1024.")

    args = parser.parse_args()

    display_title()
    show_animation()

    print(f"\n[*] Scanning {args.target} for open ports...\n")
    port_range = tuple(map(int, args.port_range.split('-')))
    open_ports = scan_ports(args.target, port_range)

    for port in open_ports:
        print(f"[+] Port {port} is OPEN")
        time.sleep(0.1)
    
    print("\n[+] Scan complete. Saving results...\n")
    formatted_ports = [f"Port {port} is open" for port in open_ports]
    save_to_file(args.output_file, formatted_ports)
    
    print(f"[+] Results saved to {args.output_file}\n")
