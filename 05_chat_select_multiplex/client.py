#!/usr/bin/env python3
"""
Procedure 5: Chat Client Permitting Multiple Message Send/Receive (I/O Multiplexing with select)
Objective: Allow asynchronous sending and receiving without waiting for turn-taking
           by multiplexing stdin and the server connection using select.select().
"""

import socket
import select
import sys


def run_client(host="127.0.0.1", port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print(f"[+] Connected to Multiplexed Server at {host}:{port}")
        print("    You can send multiple messages at any time. Type 'bye' to disconnect.\n")

        while True:
            # Maintains a list of possible input streams
            input_streams = [sys.stdin, s]

            try:
                read_sockets, _, _ = select.select(input_streams, [], [])
            except (ValueError, select.error):
                break

            should_exit = False
            for socks in read_sockets:
                if socks == s:
                    # Message received from the server
                    data = socks.recv(2048)
                    if not data:
                        print("\n[-] Server closed connection.")
                        should_exit = True
                        break

                    message = data.decode("utf-8", errors="replace")
                    print(f"<received> {message.rstrip()}")
                    if message.strip().lower() == "bye":
                        print("[*] Server ended conversation with 'bye'.")
                        should_exit = True
                        break
                else:
                    # User typed input in stdin
                    line = sys.stdin.readline()
                    if not line:
                        should_exit = True
                        break

                    message = line.rstrip("\r\n")
                    s.sendall((message + "\n").encode("utf-8"))
                    print(f"<You> {message}")

                    if message.strip().lower() == "bye":
                        print("[*] You signaled 'bye'.")
                        should_exit = True
                        break

            if should_exit:
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
    run_client(host=host_arg, port=port_arg)
