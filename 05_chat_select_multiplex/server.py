#!/usr/bin/env python3
"""
Procedure 5: Chat Server Permitting Multiple Message Send/Receive (I/O Multiplexing with select)
Objective: Allow asynchronous sending and receiving without rigid turn-taking by multiplexing
           stdin and the client socket using select.select().
"""

import socket
import select
import sys


def run_server(port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("", port))
    server.listen(5)
    print(f"[+] Multiplexed Chat Server listening on port {port}...")
    print("    Both you and the client can send multiple messages at any time!")
    print("    Type 'bye' to close current client connection.\n")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[+] {addr[0]} connected (Port: {addr[1]})")

            active = True
            while active:
                # Maintain list of readable input streams
                input_streams = [sys.stdin, conn]

                try:
                    read_sockets, _, _ = select.select(input_streams, [], [])
                except (ValueError, select.error):
                    break

                for socks in read_sockets:
                    if socks == conn:
                        # Data incoming from the client socket
                        data = socks.recv(2048)
                        if not data:
                            print("\n[-] Client closed the connection.")
                            active = False
                            break

                        message = data.decode("utf-8", errors="replace")
                        print(f"<received> {message.rstrip()}")
                        if message.strip().lower() == "bye":
                            print("[*] Client signaled 'bye'.")
                            active = False
                            break
                    else:
                        # User typed on the server terminal (sys.stdin)
                        line = sys.stdin.readline()
                        if not line:
                            # End of standard input (EOF)
                            active = False
                            break

                        message = line.rstrip("\r\n")
                        conn.sendall((message + "\n").encode("utf-8"))
                        print(f"<You> {message}")

                        if message.strip().lower() == "bye":
                            print("[*] You signaled 'bye'. Closing client connection.")
                            active = False
                            break

            conn.close()
            print(f"[-] Client {addr[0]} disconnected.\n")
            print("[+] Waiting for next client...")

    except KeyboardInterrupt:
        print("\n[*] Server shutdown signal received.")
    finally:
        server.close()
        print("[+] Multiplexed Chat Server closed.")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    run_server(port=port_arg)
