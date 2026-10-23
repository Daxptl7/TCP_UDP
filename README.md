# Transmission Control Protocol (TCP) & Socket Programming Suite

An end-to-end Python 3 implementation, test suite, interactive CLI launcher, and web visualizer covering the core procedures of network socket programming and TCP.

---

## 📂 Project Structure

```
TCP_UDP/
├── 01_google_client/
│   ├── client.py                    # Procedure 1: Connects to Google HTTP server
│   └── README.md                    # Detailed guide & explanation
├── 02_telnet_server/
│   ├── server.py                    # Procedure 2: Server greeting client
│   ├── client.py                    # Companion client (for systems without telnet)
│   └── README.md                    # Instructions for nc, telnet, and client.py
├── 03_echo_single_message/
│   ├── server.py                    # Procedure 3: Single message Echo server
│   ├── client.py                    # Single message Echo client
│   └── README.md                    # Detailed guide
├── 04_basic_chat_turns/
│   ├── server.py                    # Procedure 4: Turn-based chat server
│   ├── client.py                    # Turn-based chat client ('bye' to exit)
│   └── README.md                    # Detailed guide
├── 05_chat_select_multiplex/
│   ├── server.py                    # Procedure 5: Non-blocking chat using select()
│   ├── client.py                    # Multiplexed client (multiple messages allowed)
│   └── README.md                    # Detailed guide
├── 06_chat_room_multiclient/
│   ├── server.py                    # Procedure 6: Threaded multi-client chatroom
│   ├── client.py                    # Chatroom client with live broadcast
│   └── README.md                    # Detailed guide
├── web_visualizer/                  # Interactive Browser-based Visualizer
│   ├── index.html                   # Visualizer UI with 3-Way Handshake animation
│   ├── style.css                    # Dark-mode glassmorphic styling
│   └── app.js                       # Protocol state machine & simulation engine
├── run_demo.py                      # Interactive Terminal Menu Launcher
├── test_all.py                      # Automated test suite (Python unittest)
├── report.md                        # Complete Academic Laboratory Report
└── README.md                        # Project documentation
```

---

## 🚀 Quick Start

### 1. Run the Interactive CLI Menu
Launch the interactive command center to run any procedure or server/client pair:
```bash
python3 run_demo.py
```

### 2. Run All Automated Tests
Verify all 6 procedures end-to-end with unit tests:
```bash
python3 test_all.py
```

### 3. Launch the Web Visualizer
Open the visualizer in your web browser to see the animated TCP 3-Way Handshake, Connection Teardown, and simulated chat rooms:
```bash
python3 -m http.server 8080 --directory web_visualizer
```
Then visit: **`http://localhost:8080`**

---

## 🛠️ Step-by-Step Procedure Instructions

### Procedure 1: Google HTTP Client
Connects to `www.google.com` on port 80, sends an HTTP request, and parses headers.
```bash
python3 01_google_client/client.py
```

### Procedure 2: Telnet / Netcat Server
```bash
# Terminal 1:
python3 02_telnet_server/server.py

# Terminal 2 (choose any):
nc 127.0.0.1 12345
# or
python3 02_telnet_server/client.py
```

### Procedure 3: Echo Single Message
```bash
# Terminal 1:
python3 03_echo_single_message/server.py

# Terminal 2:
python3 03_echo_single_message/client.py
```

### Procedure 4: Turn-Based Chat ('bye' to finish)
```bash
# Terminal 1:
python3 04_basic_chat_turns/server.py

# Terminal 2:
python3 04_basic_chat_turns/client.py
```

### Procedure 5: Multiplexed Chat using `select()`
Allows either party to send multiple messages consecutively without waiting for a turn.
```bash
# Terminal 1:
python3 05_chat_select_multiplex/server.py

# Terminal 2:
python3 05_chat_select_multiplex/client.py
```

### Procedure 6: Multi-Client Broadcast Chat Room
Connect multiple clients; anything typed in one client is broadcast to all others.
```bash
# Terminal 1:
python3 06_chat_room_multiclient/server.py

# Terminal 2 (Client 1 - Alice):
python3 06_chat_room_multiclient/client.py

# Terminal 3 (Client 2 - Bob):
python3 06_chat_room_multiclient/client.py

# Terminal 4 (Client 3 - Charlie):
python3 06_chat_room_multiclient/client.py
```

---

## 🔍 Bug Fixes & Python 3 Modernization

The original prompt snippets were written for Python 2 and contained several syntax errors and logical flaws. All of these have been resolved:
1. **Python 3 Compatibility**: Converted all `print '...'` statements to `print(...)` function calls.
2. **Standard I/O**: Replaced deprecated `raw_input()` with `input()` and `sys.stdin.readline()`.
3. **Byte Streams**: Sockets in Python 3 exchange raw `bytes`, so strings are explicitly encoded with `.encode('utf-8')` before transmission and decoded with `.decode('utf-8')` upon reception.
4. **Syntax Errors**: Added missing colons (`if message == 'bye':`, `if conn != connection:`).
5. **Procedure 5 Server Logic**: Moved `server.close()` out of the client handling loop so the server remains active to accept subsequent clients.
6. **Procedure 6 Client Logic**: Removed misplaced `server.close()` inside the message loop that caused clients to crash after sending only one message.
7. **Thread Safety**: Protected `list_of_conns` using `threading.Lock()` to prevent race conditions during client disconnects and broadcasts.
8. **Port Reusability**: Added `socket.SO_REUSEADDR` to avoid `Address already in use` errors during server restarts.

For full details, review [report.md](file:///Users/daxpatel/Desktop/AIML/TCP_UDP/report.md).
