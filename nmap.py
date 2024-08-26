import socket
import argparse
import time

def scan_ports(target, port_range):
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write("\n".join(data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeriox Open Nmap - Ethical Port Scanning Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("port_range", help="Range of ports to scan (e.g., 1-1024)")
    parser.add_argument("output_file", help="Output file to save the results")

    args = parser.parse_args()

    print(r"""
       _____                 _                     
      |__  /___  _ __   __ _| | _____ _ __ ___  ___ 
        / // _ \| '_ \ / _` | |/ / _ \ '__/ __|/ _ \
       / /| (_) | | | | (_| |   <  __/ |  \__ \  __/
      /____\___/|_| |_|\__,_|_|\_\___|_|  |___/\___|
    """)
    time.sleep(2)

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
