#!/usr/bin/env python3
"""
Procedure 4: Basic Turn-Based Chat Server
Objective: Server accepts a client connection and engages in turn-based chat.
           It waits for the client to send a message, prints it, then prompts
           the server user for a response. The loop terminates when either party says 'bye'.
"""

import socket
import sys


def run_chat_server(port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(("", port))
    s.listen(5)
    print(f"[+] Turn-Based Chat Server listening on port {port}...")
    print("    Type 'bye' to end conversation with client.\n")

    try:
        while True:
            c, addr = s.accept()
            print(f"[+] Got connection from {addr}")
            print("    Waiting for client to send the first message...\n")

            while True:
                # 1. Receive message from client
                data = c.recv(1024)
                if not data:
                    print("[-] Client disconnected unexpectedly.")
                    break

                buf = data.decode("utf-8", errors="replace")
                print(f"received: {buf}\n")

                if buf.strip().lower() == "bye":
                    print("[*] Client ended conversation with 'bye'.")
                    break

                # 2. Prompt server user for response
                try:
                    msg = input("Enter a msg: ")
                except EOFError:
                    msg = "bye"

                c.sendall(msg.encode("utf-8"))

                if msg.strip().lower() == "bye":
                    print("[*] You ended the conversation with 'bye'.")
                    break

            c.close()
            print(f"[-] Closed connection with {addr}.\n")
            print("[+] Waiting for next client...")
    except KeyboardInterrupt:
        print("\n[*] Server stopping...")
    finally:
        s.close()
        print("[+] Server socket closed.")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    run_chat_server(port=port_arg)
