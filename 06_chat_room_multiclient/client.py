#!/usr/bin/env python3
"""
Procedure 6: Multi-Client Chat Room Client
Objective: Connects to Chat Room Server, receives broadcast messages from other clients,
           and allows the user to send messages to the room concurrently.
"""

import socket
import select
import sys


def run_chatroom_client(host="127.0.0.1", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((host, port))
        print(f"[+] Connected to Chat Room at {host}:{port}")
        print("    Type your message and press Enter to chat. Type 'bye' to leave.\n")

        while True:
            # Maintains a list of possible input streams: standard input and the socket
            sockets_list = [sys.stdin, server]

            """
            select returns which stream is ready for input:
            - If server socket is ready: incoming broadcast from another peer
            - If sys.stdin is ready: local user entered text
            """
            try:
                read_sockets, _, _ = select.select(sockets_list, [], [])
            except (ValueError, select.error):
                break

            should_exit = False
            for socks in read_sockets:
                if socks == server:
                    # Message from server / other participants
                    data = socks.recv(2048)
                    if not data:
                        print("\n[-] Chat room server disconnected.")
                        should_exit = True
                        break
                    print(data.decode("utf-8", errors="replace").rstrip())
                else:
                    # User input from keyboard
                    message = sys.stdin.readline()
                    if not message:
                        should_exit = True
                        break

                    clean_msg = message.rstrip("\r\n")
                    server.sendall((clean_msg + "\n").encode("utf-8"))
                    print(f"<You> {clean_msg}")

                    if clean_msg.strip().lower() == "bye":
                        print("[*] Leaving chat room...")
                        should_exit = True
                        break

            if should_exit:
                break

    except ConnectionRefusedError:
        print(f"[-] Connection refused. Ensure Chat Room Server is running on {host}:{port}")
    except socket.error as err:
        print(f"[-] Socket error: {err}")
    finally:
        server.close()
        print("[+] Chat room client closed.")


if __name__ == "__main__":
    host_arg = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    run_chatroom_client(host=host_arg, port=port_arg)
