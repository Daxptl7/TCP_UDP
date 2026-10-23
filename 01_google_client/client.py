#!/usr/bin/env python3
"""
Procedure 1: Client Program that connects to Google.com
Objective: Study socket creation, DNS resolution, and TCP connection establishment to an external HTTP server.
"""

import socket
import sys


def main():
    print("=" * 60)
    print(" Procedure 1: TCP Socket Connection to Google.com")
    print("=" * 60)

    # 1. Create a TCP socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Socket successfully created.")
    except socket.error as err:
        print(f"[-] Socket creation failed with error: {err}")
        sys.exit(1)

    # 2. Resolve target domain name to IP address
    target_host = "www.google.com"
    target_port = 80  # Default HTTP port

    try:
        ip = socket.gethostbyname(target_host)
        print(f"[+] DNS Resolution: '{target_host}' resolved to IP address: {ip}")
    except socket.gaierror as err:
        print(f"[-] Could not resolve host '{target_host}': {err}")
        s.close()
        sys.exit(1)

    # 3. Connect to the remote server using the resolved IP and port
    try:
        print(f"[*] Attempting to connect to {target_host} ({ip}) on port {target_port}...")
        s.connect((ip, target_port))
        print("socket connected to google http server")
        print(f"[+] Local socket endpoint (IP, Port): {s.getsockname()}")
        print(f"[+] Remote socket endpoint (IP, Port): {s.getpeername()}")

        # 4. Send an HTTP HEAD/GET request to demonstrate bidirectional communication
        http_request = (
            f"HEAD / HTTP/1.1\r\n"
            f"Host: {target_host}\r\n"
            f"User-Agent: Antigravity-Python-Socket/1.0\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.sendall(http_request.encode("utf-8"))
        print("[+] Sent HTTP HEAD request to remote host.")

        # 5. Receive HTTP response headers
        response = s.recv(1024)
        print("\n[+] Response received from Google server (First 1024 bytes):")
        print("-" * 50)
        print(response.decode("utf-8", errors="replace").strip())
        print("-" * 50)

    except socket.error as err:
        print(f"[-] Connection failed with error: {err}")
    finally:
        # 6. Close the socket connection
        s.close()
        print("\n[+] Socket connection closed cleanly.")


if __name__ == "__main__":
    main()
