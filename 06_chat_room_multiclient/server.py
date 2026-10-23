#!/usr/bin/env python3
"""
Procedure 6: Multi-Client Chat Room Server
Objective: A multi-threaded chat server that manages multiple concurrent clients.
           When any client sends a message, it is broadcast to all other active clients.
"""

import socket
import sys
import threading

# Global list of active client sockets and a lock for thread-safe mutations
list_of_conns = []
clients_lock = threading.Lock()


def clientthread(conn, addr):
    """Handles communication with an individual connected client."""
    welcome_msg = "Welcome to this chatroom!\n"
    try:
        conn.sendall(welcome_msg.encode("utf-8"))
    except socket.error:
        remove(conn)
        return

    while True:
        try:
            data = conn.recv(2048)
            if data:
                message = data.decode("utf-8", errors="replace").rstrip()
                print(f"<{addr[0]}:{addr[1]}> {message}")

                # Format broadcast message
                message_to_send = f"<{addr[0]}:{addr[1]}> {message}\n"
                broadcast(message_to_send.encode("utf-8"), conn)
            else:
                # Empty bytes mean client disconnected
                print(f"[-] Client {addr} disconnected.")
                remove(conn)
                break
        except Exception:
            remove(conn)
            break


def broadcast(message_bytes, connection):
    """Broadcasts a message to all active clients except the sender."""
    with clients_lock:
        clients_copy = list_of_conns[:]

    for conn in clients_copy:
        if conn != connection:
            try:
                conn.sendall(message_bytes)
            except Exception:
                remove(conn)


def remove(connection):
    """Safely removes and closes a client connection."""
    with clients_lock:
        if connection in list_of_conns:
            list_of_conns.remove(connection)
    try:
        connection.close()
    except Exception:
        pass


def run_chatroom_server(port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("", port))
    # Listen for up to 100 queued connections
    server.listen(100)
    print(f"[+] Chat Room Server active and listening on port {port}...")
    print("    Multiple clients can connect and chat simultaneously!")
    print("    Press Ctrl+C to terminate the server.\n")

    try:
        while True:
            conn, addr = server.accept()
            with clients_lock:
                list_of_conns.append(conn)

            print(f"[+] Client {addr} connected. Total active clients: {len(list_of_conns)}")

            # Create an individual thread for each connected user
            t = threading.Thread(target=clientthread, args=(conn, addr), daemon=True)
            t.start()

    except KeyboardInterrupt:
        print("\n[*] Server shutdown initiated...")
    finally:
        with clients_lock:
            for conn in list_of_conns:
                try:
                    conn.close()
                except Exception:
                    pass
            list_of_conns.clear()
        server.close()
        print("[+] Chat Room Server shutdown completed.")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    run_chatroom_server(port=port_arg)
