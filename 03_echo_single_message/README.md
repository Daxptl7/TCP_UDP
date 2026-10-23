# Procedure 3: Echo Client and Echo Server (Single Message Exchange)

## Overview
Illustrates an Echo service using TCP:
1. Client connects to server on port `12345`.
2. Client takes user input via `input()` (replacing Python 2 `raw_input()`).
3. Client encodes and sends the string over the TCP connection.
4. Server receives the buffer with `recv(1024)`, logs it, and echoes it back using `sendall()`.
5. Client receives the echoed message, prints it, and both sides close the connection.

## How to Run

### Step 1: Start Server
```bash
python3 server.py
```

### Step 2: In a Second Terminal, Run Client
```bash
python3 client.py
```
Or pass the message as an argument:
```bash
python3 client.py 127.0.0.1 12345 "Hello from Computer Networks Lab"
```
