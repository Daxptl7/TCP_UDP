#!/usr/bin/env python3
"""
Procedure 2: Client Program to interact with Procedure 2 Server.
Useful on systems like modern macOS where 'telnet' is not installed by default.
"""

import socket
import sys


def run_client(host="127.0.0.1", port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"[*] Connecting to server at {host}:{port}...")
        s.connect((host, port))
        print("[+] Connected! Waiting for server greeting...")

        # Receive data from server
        data = s.recv(1024)
        print(f"[Server Response]: {data.decode('utf-8', errors='replace').rstrip()}")
    except ConnectionRefusedError:
        print(f"[-] Connection refused. Ensure server is running on {host}:{port}")
    except socket.error as err:
        print(f"[-] Socket error: {err}")
    finally:
        s.close()
        print("[+] Client socket closed.")


if __name__ == "__main__":
    host_arg = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    run_client(host=host_arg, port=port_arg)
