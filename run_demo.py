#!/usr/bin/env python3
"""
Interactive CLI Launcher for TCP Socket Programming Lab
Allows running individual procedures, clients, servers, or automated tests from a single terminal interface.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCEDURES = [
    {
        "id": 1,
        "title": "Client Program that connects to Google.com",
        "folder": "01_google_client",
        "has_server": False,
        "client": "client.py",
    },
    {
        "id": 2,
        "title": "Server Program. Connect using Netcat / Telnet / Python Client",
        "folder": "02_telnet_server",
        "has_server": True,
        "server": "server.py",
        "client": "client.py",
    },
    {
        "id": 3,
        "title": "Echo Client & Server (Single Message Exchange)",
        "folder": "03_echo_single_message",
        "has_server": True,
        "server": "server.py",
        "client": "client.py",
    },
    {
        "id": 4,
        "title": "Turn-Based Chat Client & Server ('bye' to finish)",
        "folder": "04_basic_chat_turns",
        "has_server": True,
        "server": "server.py",
        "client": "client.py",
    },
    {
        "id": 5,
        "title": "Multiplexed Chat Client & Server (select() multiple messages)",
        "folder": "05_chat_select_multiplex",
        "has_server": True,
        "server": "server.py",
        "client": "client.py",
    },
    {
        "id": 6,
        "title": "Multi-Client Broadcast Chat Room",
        "folder": "06_chat_room_multiclient",
        "has_server": True,
        "server": "server.py",
        "client": "client.py",
    },
]


def print_banner():
    print("\n" + "=" * 70)
    print("  STUDY OF SOCKET PROGRAMMING & TRANSMISSION CONTROL PROTOCOL (TCP)  ")
    print("=" * 70)
    for p in PROCEDURES:
        print(f" [{p['id']}] Procedure {p['id']}: {p['title']}")
    print(" [T] Run Complete Automated Test Suite (test_all.py)")
    print(" [V] Launch Interactive Web Socket Visualizer")
    print(" [Q] Quit")
    print("=" * 70)


def handle_procedure(proc):
    print("\n" + "-" * 60)
    print(f" Procedure {proc['id']}: {proc['title']}")
    print("-" * 60)

    if not proc["has_server"]:
        print("Executing Google Client...")
        client_file = os.path.join(BASE_DIR, proc["folder"], proc["client"])
        subprocess.run([sys.executable, client_file])
        return

    print("Choose action:")
    print("  [1] Start Server")
    print("  [2] Start Client (connects to running server)")
    print("  [B] Back to Main Menu")
    choice = input("\nEnter choice: ").strip().lower()

    if choice == "1":
        server_file = os.path.join(BASE_DIR, proc["folder"], proc["server"])
        print(f"\n[*] Starting Server: python3 {proc['folder']}/{proc['server']}")
        print("[*] Note: Open another terminal window to run the client simultaneously!\n")
        subprocess.run([sys.executable, server_file])
    elif choice == "2":
        client_file = os.path.join(BASE_DIR, proc["folder"], proc["client"])
        print(f"\n[*] Starting Client: python3 {proc['folder']}/{proc['client']}\n")
        subprocess.run([sys.executable, client_file])


def main():
    while True:
        print_banner()
        choice = input("Select an option [1-6, T, V, Q]: ").strip().lower()

        if choice in ["q", "exit"]:
            print("\nExiting. Thank you!")
            break
        elif choice == "t":
            print("\n[*] Running all automated unit tests...\n")
            test_file = os.path.join(BASE_DIR, "test_all.py")
            subprocess.run([sys.executable, test_file])
        elif choice == "v":
            print("\n[*] Starting local HTTP server for Web Socket Visualizer at http://localhost:8080 ...")
            web_dir = os.path.join(BASE_DIR, "web_visualizer")
            if os.path.exists(web_dir):
                print("[*] Press Ctrl+C in this terminal when finished viewing.")
                try:
                    subprocess.run([sys.executable, "-m", "http.server", "8080", "--directory", web_dir])
                except KeyboardInterrupt:
                    print("\n[*] Visualizer stopped.")
            else:
                print("[-] Web visualizer directory not found.")
        elif choice in ["1", "2", "3", "4", "5", "6"]:
            idx = int(choice) - 1
            handle_procedure(PROCEDURES[idx])
        else:
            print("[!] Invalid option. Please try again.")


if __name__ == "__main__":
    main()
