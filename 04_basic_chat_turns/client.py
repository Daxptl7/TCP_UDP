#!/usr/bin/env python3
"""
Procedure 4: Basic Turn-Based Chat Client
Objective: Client connects to Server and engages in turn-based chat.
           It sends a message first, then waits for the server's reply.
           Ends when either party sends 'bye'.
"""

import socket
import sys


def run_chat_client(host="127.0.0.1", port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print(f"[+] Connected to Chat Server at {host}:{port}")
        print("    Type 'bye' to exit the chat.\n")

        while True:
            # 1. Prompt and send message
            try:
                buf = input("Enter a message to send: ")
            except EOFError:
                buf = "bye"

            s.sendall(buf.encode("utf-8"))

            if buf.strip().lower() == "bye":
                print("[*] You ended the conversation.")
                break

            # 2. Wait for server response
            data = s.recv(1024)
            if not data:
                print("[-] Server disconnected.")
                break

            msg = data.decode("utf-8", errors="replace")
            print("received: " + msg)

            if msg.strip().lower() == "bye":
                print("[*] Server ended the conversation.")
                break

    except ConnectionRefusedError:
        print(f"[-] Connection refused. Ensure server is running on {host}:{port}")
    except socket.error as err:
        print(f"[-] Socket error: {err}")
    finally:
        s.close()
        print("[+] Chat client closed.")


if __name__ == "__main__":
    host_arg = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    run_chat_client(host=host_arg, port=port_arg)
