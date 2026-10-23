# Procedure 6: Multi-Client Broadcast Chat Room

## Overview
Implements a multi-user group chat room using multi-threading on the server and I/O multiplexing on the clients:
- **Server Architecture**:
  - Main thread listens on port `12345` and accepts client connections.
  - For each new connection, a worker thread is spawned (`threading.Thread`).
  - Worker thread listens for messages from that client and forwards them to `broadcast()`.
  - `broadcast()` delivers the message to all other connected clients, using a `threading.Lock` to ensure thread safety while managing the clients list.
- **Client Architecture**:
  - Connects to the chat server.
  - Uses `select.select()` to multiplex between `sys.stdin` (typing) and `server` socket (receiving messages from other room participants).
  - Bug Fix Note: The original prompt had `server.close()` inside the message loop, causing the client to terminate after only one message. That has been corrected to permit continuous real-time chatting until the user types `bye`.

## How to Run

### Step 1: Start Server
```bash
python3 server.py
```

### Step 2: Open Multiple Client Terminals
**Terminal 2 (Client 1):**
```bash
python3 client.py
```

**Terminal 3 (Client 2):**
```bash
python3 client.py
```

**Terminal 4 (Client 3):**
```bash
python3 client.py
```

Messages typed in any client terminal will instantly broadcast to all other client terminals!
