#!/usr/bin/env python3
"""
Automated Test Suite for Socket Programming and TCP Implementation Lab
Tests all 6 procedures systematically using Python unittest.
"""

import unittest
import subprocess
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSocketProcedures(unittest.TestCase):

    def test_01_google_client(self):
        """Procedure 1: Verify TCP client connects to Google.com and gets HTTP response."""
        script_path = os.path.join(BASE_DIR, "01_google_client", "client.py")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertIn("socket connected to google http server", result.stdout)
        self.assertIn("HTTP/1.1", result.stdout)

    def test_02_telnet_server_and_client(self):
        """Procedure 2: Verify server accepts connection and sends greeting."""
        port = 13002
        srv_path = os.path.join(BASE_DIR, "02_telnet_server", "server.py")
        cli_path = os.path.join(BASE_DIR, "02_telnet_server", "client.py")

        srv = subprocess.Popen([sys.executable, srv_path, str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.4)

        try:
            cli = subprocess.run([sys.executable, cli_path, "127.0.0.1", str(port)], capture_output=True, text=True, timeout=5)
            self.assertEqual(cli.returncode, 0)
            self.assertIn("Thank you for connecting", cli.stdout)
        finally:
            srv.terminate()
            srv.wait()

    def test_03_echo_server_and_client(self):
        """Procedure 3: Verify single message echo exchange."""
        port = 13003
        srv_path = os.path.join(BASE_DIR, "03_echo_single_message", "server.py")
        cli_path = os.path.join(BASE_DIR, "03_echo_single_message", "client.py")

        srv = subprocess.Popen([sys.executable, srv_path, str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.4)

        test_msg = "Hello TCP Echo Server"
        try:
            cli = subprocess.run([sys.executable, cli_path, "127.0.0.1", str(port), test_msg], capture_output=True, text=True, timeout=5)
            self.assertEqual(cli.returncode, 0)
            self.assertIn(f"Echo received from server: {test_msg}", cli.stdout)
        finally:
            srv.terminate()
            srv.wait()

    def test_04_basic_chat_turns(self):
        """Procedure 4: Verify turn-based chat conversation terminated by 'bye'."""
        port = 13004
        srv_path = os.path.join(BASE_DIR, "04_basic_chat_turns", "server.py")
        cli_path = os.path.join(BASE_DIR, "04_basic_chat_turns", "client.py")

        srv = subprocess.Popen([sys.executable, srv_path, str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.4)

        cli = subprocess.Popen([sys.executable, cli_path, "127.0.0.1", str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.4)

        try:
            cli.stdin.write("Hi Server\n")
            cli.stdin.flush()
            time.sleep(0.3)

            srv.stdin.write("Hello Client\n")
            srv.stdin.flush()
            time.sleep(0.3)

            cli.stdin.write("bye\n")
            cli.stdin.flush()

            cli_out, _ = cli.communicate(timeout=4)
            self.assertIn("received: Hello Client", cli_out)
            self.assertIn("You ended the conversation", cli_out)
        finally:
            srv.terminate()
            try:
                srv.communicate(timeout=1)
            except Exception:
                pass
            srv.wait()

    def test_05_chat_select_multiplex(self):
        """Procedure 5: Verify I/O multiplexed chat permitting multiple consecutive messages."""
        port = 13005
        srv_path = os.path.join(BASE_DIR, "05_chat_select_multiplex", "server.py")
        cli_path = os.path.join(BASE_DIR, "05_chat_select_multiplex", "client.py")

        srv = subprocess.Popen([sys.executable, srv_path, str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.4)

        cli = subprocess.Popen([sys.executable, cli_path, "127.0.0.1", str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.4)

        try:
            cli.stdin.write("Message One\n")
            cli.stdin.write("Message Two\n")
            cli.stdin.flush()
            time.sleep(0.3)

            srv.stdin.write("Server Ack\n")
            srv.stdin.flush()
            time.sleep(0.3)

            cli.stdin.write("bye\n")
            cli.stdin.flush()

            cli_out, _ = cli.communicate(timeout=4)
            self.assertIn("<You> Message One", cli_out)
            self.assertIn("<You> Message Two", cli_out)
            self.assertIn("<received> Server Ack", cli_out)
        finally:
            srv.terminate()
            try:
                srv.communicate(timeout=1)
            except Exception:
                pass
            srv.wait()

    def test_06_chat_room_broadcast(self):
        """Procedure 6: Verify multi-client chat room broadcasting messages between participants."""
        port = 13006
        srv_path = os.path.join(BASE_DIR, "06_chat_room_multiclient", "server.py")
        cli_path = os.path.join(BASE_DIR, "06_chat_room_multiclient", "client.py")

        srv = subprocess.Popen([sys.executable, srv_path, str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.4)

        c1 = subprocess.Popen([sys.executable, cli_path, "127.0.0.1", str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.3)

        c2 = subprocess.Popen([sys.executable, cli_path, "127.0.0.1", str(port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(0.3)

        try:
            c1.stdin.write("Greetings from Peer 1\n")
            c1.stdin.flush()
            time.sleep(0.4)

            c2.stdin.write("bye\n")
            c2.stdin.flush()
            c2_out, _ = c2.communicate(timeout=4)

            self.assertIn("Welcome to this chatroom!", c2_out)
            self.assertIn("Greetings from Peer 1", c2_out)

            c1.stdin.write("bye\n")
            c1.stdin.flush()
            c1_out, _ = c1.communicate(timeout=4)
            self.assertIn("<You> Greetings from Peer 1", c1_out)
        finally:
            srv.terminate()
            srv.wait()


if __name__ == "__main__":
    unittest.main(verbosity=2)
