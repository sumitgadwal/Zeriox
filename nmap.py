import socket
import argparse
import time
import sys

# Define common ports for specific services
COMMON_PORTS = {
    'TCP': [21, 22, 23, 25, 80, 443, 3306, 5432],
    'UDP': [53, 67, 68, 123, 161, 162],
    'FTP': [21]  # FTP is typically on port 21
}

def scan_ports(target, protocols):
    open_ports = {'TCP': [], 'UDP': [], 'FTP': []}
    start_time = time.time()
    
    for protocol in protocols:
        for port in COMMON_PORTS[protocol]:
            if protocol == 'TCP':
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.05)  # Timeout for quick scanning
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports['TCP'].append(port)
                    sock.close()
                except Exception as e:
                    pass

            elif protocol == 'UDP':
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(0.05)  # Timeout for quick scanning
                    sock.sendto(b'', (target, port))
                    try:
                        sock.recvfrom(1024)
                        open_ports['UDP'].append(port)
                    except socket.error:
                        pass
                    sock.close()
                except Exception as e:
                    pass

            elif protocol == 'FTP':
                # FTP is a TCP service, so it is included in TCP scan by default
                if port in open_ports['TCP']:
                    open_ports['FTP'].append(port)

            # Check if the scanning process is exceeding 10 seconds
            if time.time() - start_time > 10:
                break

    return open_ports

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        for protocol, ports in data.items():
            f.write(f"{protocol} Ports:\n")
            for port in ports:
                f.write(f"Port {port} is open\n")
            f.write("\n")

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

    args = parser.parse_args()

    display_title()
    show_animation()

    print(f"\n[*] Scanning {args.target} for open ports...\n")
    protocols = ['TCP', 'UDP', 'FTP']
    open_ports = scan_ports(args.target, protocols)

    for protocol, ports in open_ports.items():
        for port in ports:
            print(f"[+] {protocol} Port {port} is OPEN")
            time.sleep(0.1)
    
    print("\n[+] Scan complete. Saving results...\n")
    save_to_file(args.output_file, open_ports)
    
    print(f"[+] Results saved to {args.output_file}\n")
