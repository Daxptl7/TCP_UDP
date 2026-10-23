#!/usr/bin/env python3
"""
Procedure 3: Echo Client (Single Message Exchange)
Objective: Client connects to Echo Server, prompts the user for a message,
           sends it to the server, and prints the echoed response.
"""

import socket
import sys


def run_echo_client(host="127.0.0.1", port=12345, default_msg=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))

        # Prompt user or use default_msg (useful for automated testing)
        if default_msg is not None:
            buf = default_msg
            print(f"Enter a message to send: {buf}")
        else:
            buf = input("Enter a message to send: ")

        # Send encoded bytes
        s.sendall(buf.encode("utf-8"))

        # Receive echo response
        response = s.recv(1024)
        print("Echo received from server:", response.decode("utf-8", errors="replace"))

    except ConnectionRefusedError:
        print(f"[-] Connection refused. Ensure Echo Server is running on {host}:{port}")
    except socket.error as err:
        print(f"[-] Socket error: {err}")
    finally:
        s.close()


if __name__ == "__main__":
    host_arg = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    msg_arg = sys.argv[3] if len(sys.argv) > 3 else None
    run_echo_client(host=host_arg, port=port_arg, default_msg=msg_arg)
