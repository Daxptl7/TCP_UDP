#!/usr/bin/env python3
"""
Procedure 3: Echo Server (Single Message Exchange)
Objective: Server receives a single message from the client, logs it, echoes it back, and closes the connection.
"""

import socket
import sys


def run_echo_server(port=12345):
    # 1. Create TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind and listen
    s.bind(("", port))
    s.listen(5)
    print(f"[+] Echo Server running on port {port}. Waiting for connections...")

    try:
        while True:
            c, addr = s.accept()
            print(f"[+] Got connection from {addr}")

            # 3. Receive message from client
            buf = c.recv(1024)
            if not buf:
                print("[-] Received empty buffer (client disconnected).")
                c.close()
                continue

            decoded_msg = buf.decode("utf-8", errors="replace")
            print(f"received {decoded_msg}\n")
            print("echoing it back\n")

            # 4. Echo the exact message back to the client
            c.sendall(buf)

            # 5. Close client connection
            c.close()
            print(f"[-] Connection with {addr} closed.")
    except KeyboardInterrupt:
        print("\n[*] Server shutdown signal received (Ctrl+C).")
    finally:
        s.close()
        print("[+] Echo Server closed.")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    run_echo_server(port=port_arg)
