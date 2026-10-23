#!/usr/bin/env python3
"""
Procedure 2: Server Program. Use Telnet / Netcat to Connect and Interact with it.
Objective: Implement a TCP server socket that binds to a port, listens for incoming connections,
           accepts a client connection, sends a welcome greeting, and closes the connection.
"""

import socket
import sys


def run_server(port=12345):
    # 1. Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Allow immediate socket reuse to prevent "Address already in use" errors
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 3. Bind to all interfaces ('') on the designated port
    s.bind(("", port))
    print(f"[+] Server successfully bound to port {port}")

    # 4. Listen for incoming connections (backlog queue of 5)
    s.listen(5)
    print(f"[+] Server is listening for connections on 0.0.0.0:{port}...")
    print("    (You can connect using: 'nc 127.0.0.1 12345' or 'telnet 127.0.0.1 12345' or 'python3 client.py')")
    print("    Press Ctrl+C to terminate the server.\n")

    try:
        while True:
            # 5. Accept client connection
            c, addr = s.accept()
            print(f"[+] Got connection from {addr}")

            # 6. Send greeting to client (encoded to bytes in Python 3)
            c.send(b"Thank you for connecting\n")

            # 7. Close client connection
            c.close()
            print(f"[-] Connection with {addr} closed.\n")
    except KeyboardInterrupt:
        print("\n[*] Server shutdown signal received (Ctrl+C). Closing server socket...")
    finally:
        s.close()
        print("[+] Server socket closed.")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    run_server(port=port_arg)
