# Laboratory Report: Study of Socket Programming & Implementation of Transmission Control Protocol (TCP)

---

## 1. Objective
To study the fundamentals of network socket programming and understand the implementation of the **Transmission Control Protocol (TCP)** using Python. This laboratory investigates socket lifecycles, connection establishment (3-Way Handshake), connection termination (4-Way Teardown), client-server communication paradigms, I/O multiplexing (`select`), and multi-threaded broadcast architectures.

---

## 2. Theoretical Foundations

### 2.1 The Socket Abstraction
A **network socket** is an endpoint of a two-way communication link between two programs running over a network. Originating in the Berkeley Software Distribution (BSD Unix), the Berkeley sockets API provides standard system calls for inter-process communication (IPC).

A TCP socket endpoint is defined by a 5-tuple:
$$\text{Socket Association} = (\text{Protocol}, \text{Source IP}, \text{Source Port}, \text{Destination IP}, \text{Destination Port})$$

```
+-------------------------------------------------------------------+
|                        Application Layer                          |
|  [Google Client]   [Telnet/Echo]   [Chat Client]   [Chat Room]    |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                      Transport Layer (TCP)                        |
|  - Connection-Oriented    - Reliable Byte Stream   - Flow Control |
|  - 3-Way Handshake        - Ordered Delivery       - Error Checks |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                       Network Layer (IP)                          |
|  - Logical Addressing (IPv4/IPv6)                  - Routing      |
+-------------------------------------------------------------------+
```

### 2.2 TCP Characteristics
1. **Connection-Oriented**: A dedicated logical connection is negotiated before data exchange begins.
2. **Reliability**: Uses sequence numbers, positive acknowledgments (ACK), checksums, and retransmission timers to guarantee error-free delivery.
3. **Full-Duplex Byte Stream**: Data flows in both directions simultaneously without preserving application-level message boundaries.
4. **Flow & Congestion Control**: Implements sliding windows (Advertised Window) and algorithms (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery).

### 2.3 TCP Connection Establishment (Three-Way Handshake)
```
     Client (Active Open)                                 Server (Passive Open)
         [ CLOSED ]                                            [ LISTEN ]
             |                                                     |
             | ------------------ 1. SYN (Seq=x) ----------------> | [ SYN_RCVD ]
       [ SYN_SENT ]                                                |
             |                                                     |
             | <---------- 2. SYN-ACK (Seq=y, Ack=x+1) ---------- |
      [ ESTABLISHED ]                                              |
             |                                                     |
             | ------------------ 3. ACK (Ack=y+1) --------------> | [ ESTABLISHED ]
             |                                                     |
             v                                                     v
                         Bidirectional Data Transfer
```

### 2.4 TCP Connection Teardown (Four-Way Handshake)
```
     Client (Active Close)                                Server (Passive Close)
      [ ESTABLISHED ]                                         [ ESTABLISHED ]
             |                                                     |
             | ------------------ 1. FIN (Seq=u) ----------------> | [ CLOSE_WAIT ]
      [ FIN_WAIT_1 ]                                               |
             | <----------------- 2. ACK (Ack=u+1) --------------- |
      [ FIN_WAIT_2 ]                                               |
             |                                                     | (Server finishes data)
             | <----------------- 3. FIN (Seq=v, Ack=u+1) -------- | [ LAST_ACK ]
             |                                                     |
             | ------------------ 4. ACK (Ack=v+1) --------------> | [ CLOSED ]
       [ TIME_WAIT ] (2*MSL)                                       |
             |                                                     |
         [ CLOSED ]                                                v
```

---

## 3. Systematic Procedure Breakdown

### Procedure 1: Client Program Connecting to Google.com
- **Path**: `01_google_client/client.py`
- **Socket Methods Used**:
  - `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`: Allocates an IPv4 TCP stream socket.
  - `socket.gethostbyname('www.google.com')`: Translates the domain name to an IP address using the DNS resolver.
  - `s.connect((host, 80))`: Initiates TCP 3-way handshake with Google's web server.
  - `s.sendall(request)`: Sends standard HTTP request.
  - `s.recv(1024)`: Reads HTTP response header bytes from the socket.
  - `s.close()`: Closes socket connection.
- **Key Observation**: The client's operating system assigns an ephemeral source port (e.g., `59073`) to pair with Google's well-known destination port `80`.

---

### Procedure 2: Server Program with Telnet / Netcat Interaction
- **Path**: `02_telnet_server/server.py`, `client.py`
- **Socket Methods Used**:
  - `s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`: Permits immediate binding to the port after restart, avoiding `TIME_WAIT` lockouts.
  - `s.bind(('', port))`: Binds the socket to `INADDR_ANY` (`0.0.0.0`) on port `12345`.
  - `s.listen(5)`: Places the socket in passive listening mode with a backlog queue capacity of 5 connections.
  - `c, addr = s.accept()`: Blocks until a connection arrives, then returns a new client-specific communication socket `c` and peer address tuple `addr`.
  - `c.send(b'Thank you for connecting\n')`: Transmits welcome greeting.
  - `c.close()`: Tears down the client socket.
- **Verification**: Tested using `nc 127.0.0.1 12345` and companion Python client.

---

### Procedure 3: Echo Client and Server (Single Message Exchange)
- **Path**: `03_echo_single_message/server.py`, `client.py`
- **Workflow**:
  1. Client prompts user: `input("Enter a message to send: ")`.
  2. Client transmits UTF-8 encoded string.
  3. Server receives bytes via `c.recv(1024)`.
  4. Server logs the received string and immediately echoes it back via `c.sendall(buf)`.
  5. Client receives the mirrored buffer and prints it.
- **Key Concept**: Demonstrates basic request-response pattern and byte array handling over TCP.

---

### Procedure 4: Turn-Based Half-Duplex Chat
- **Path**: `04_basic_chat_turns/server.py`, `client.py`
- **Workflow**:
  - Sequential alternating communication:
    1. Client types and sends message.
    2. Server blocks on `recv()`, reads client message, then enters input prompt.
    3. Server types and sends reply.
    4. Client blocks on `recv()`, reads server reply, then enters input prompt.
  - Either side typing `bye` terminates the conversation loop.
- **Limitations Identified**: Rigid turn-taking (half-duplex). Neither participant can send two consecutive messages or interrupt while waiting for the other side.

---

### Procedure 5: Multiplexed Chat via `select()` (Multiple Message Send/Receive)
- **Path**: `05_chat_select_multiplex/server.py`, `client.py`
- **Mechanism (I/O Multiplexing)**:
  - Both client and server call `select.select([sys.stdin, sock], [], [])`.
  - The OS blocks the process until **either** standard input (keyboard) has data ready to read **or** the TCP socket has an incoming packet ready.
  - When keyboard input occurs: transmits message immediately without waiting for a reply.
  - When socket input occurs: receives and renders peer message immediately.
- **Result**: Achieves asynchronous full-duplex communication semantics over a single thread.

---

### Procedure 6: Multi-Client Broadcast Chat Room
- **Path**: `06_chat_room_multiclient/server.py`, `client.py`
- **Architecture**:
  - **Server Concurrency**:
    - Uses `threading.Thread` to spawn an independent worker thread for each accepted client.
    - Maintains a shared `list_of_conns` protected by a `threading.Lock()` to prevent race conditions during list iteration and client disconnection.
    - When a message arrives from Client $i$, the server calls `broadcast(msg, connection)` which loops through `list_of_conns` and sends the message to all clients *except* Client $i$.
  - **Client Concurrency**:
    - Employs `select.select([sys.stdin, server_socket], [], [])` to listen for keyboard input and server broadcasts simultaneously.

---

## 4. Python 2 to Python 3 Migration & Bug Corrections

The original lab manual contained code written for legacy Python 2 with several syntactical and logical defects. The following table documents all corrections made:

| Issue in Original Snippet | Cause / Error in Python 3 | Resolution Applied |
| :--- | :--- | :--- |
| `print 'message'` | `SyntaxError: Missing parentheses in call to 'print'` | Converted to `print("message")` |
| `raw_input()` | `NameError: name 'raw_input' is not defined` | Replaced with `input()` and `sys.stdin.readline()` |
| `s.send("string")` | `TypeError: a bytes-like object is required, not 'str'` | Explicit UTF-8 encoding: `s.sendall(msg.encode('utf-8'))` |
| `from thread import *` | `ModuleNotFoundError: No module named 'thread'` | Modern `threading.Thread` and `threading.Lock` |
| Missing colons (`if message == 'bye'`) | `SyntaxError: expected ':'` | Added proper colon syntax |
| Missing colons (`if conn!=connection`) | `SyntaxError: expected ':'` | Added proper colon syntax |
| `While True:` in Client 4 | `NameError: name 'While' is not defined` | Corrected case to lowercase `while True:` |
| Server premature close in Procedure 5 | `server.close()` inside client loop closed server after 1 connection | Placed `server.close()` in `finally:` block |
| Client premature close in Procedure 6 | `server.close()` inside the message send branch killed client after 1 msg | Removed premature close; closes only on `'bye'` or EOF |
| Infinite loop on client disconnect | `c.recv()` returns empty `b''` on EOF, causing CPU spin | Added `if not data: break` to cleanly detect disconnects |
| Port locking (`Address already in use`) | Port in `TIME_WAIT` prevents server restart | Added `SO_REUSEADDR` socket option |

---

## 5. Verification & Test Execution Results

The automated unit test suite `test_all.py` was executed to validate all 6 procedures end-to-end:

```
$ python3 test_all.py -v
test_01_google_client (__main__.TestSocketProcedures.test_01_google_client)
Procedure 1: Verify TCP client connects to Google.com and gets HTTP response. ... ok
test_02_telnet_server_and_client (__main__.TestSocketProcedures.test_02_telnet_server_and_client)
Procedure 2: Verify server accepts connection and sends greeting. ... ok
test_03_echo_server_and_client (__main__.TestSocketProcedures.test_03_echo_server_and_client)
Procedure 3: Verify single message echo exchange. ... ok
test_04_basic_chat_turns (__main__.TestSocketProcedures.test_04_basic_chat_turns)
Procedure 4: Verify turn-based chat conversation terminated by 'bye'. ... ok
test_05_chat_select_multiplex (__main__.TestSocketProcedures.test_05_chat_select_multiplex)
Procedure 5: Verify I/O multiplexed chat permitting multiple consecutive messages. ... ok
test_06_chat_room_broadcast (__main__.TestSocketProcedures.test_06_chat_room_broadcast)
Procedure 6: Verify multi-client chat room broadcasting messages between participants. ... ok

----------------------------------------------------------------------
Ran 6 tests in 5.650s

OK
```

All 6 test cases passed with a 100% success rate.

---

## 6. Viva-Voce & Review Questions

### Q1: What is the difference between `SOCK_STREAM` and `SOCK_DGRAM`?
- **`SOCK_STREAM`**: Uses TCP. Provides reliable, connection-oriented, sequenced, and error-checked byte streams.
- **`SOCK_DGRAM`**: Uses UDP. Provides connectionless, unreliable datagrams with minimal overhead and no delivery guarantee.

### Q2: Why is `SO_REUSEADDR` needed on server sockets?
When a TCP server shuts down while having active connections, the local port enters the `TIME_WAIT` state for $2 \times \text{MSL}$ (Maximum Segment Lifetime, typically 30s to 2 minutes) to ensure delayed packets are flushed. Setting `SO_REUSEADDR` informs the operating system to allow immediate rebinding to the port without waiting for the timer to expire.

### Q3: What is the purpose of the backlog argument in `s.listen(backlog)`?
The backlog parameter specifies the maximum number of pending, fully-established connections that the operating system kernel can queue before the application calls `accept()`. If the queue is full and a new connection request arrives, the client receives a connection refused or timeout error.

### Q4: How does `select.select()` differ from multi-threading?
- **`select()` (I/O Multiplexing)**: Single-threaded event-driven model. The thread monitors multiple file descriptors simultaneously without context-switching overhead, but cannot execute CPU-bound work on multiple cores concurrently.
- **Multi-Threading**: Spawns distinct operating system threads for each socket. Simplifies linear blocking code structure, but incurs thread stack memory overhead and requires synchronization primitives (e.g., locks) to prevent race conditions.

---

## 7. Conclusion
In this laboratory, all 6 procedures of TCP socket programming were successfully implemented, updated for modern Python 3, and validated. The progression from basic external client connection to a full-featured multi-client threaded broadcast chat room demonstrates the core mechanisms governing modern transport layer networking.
