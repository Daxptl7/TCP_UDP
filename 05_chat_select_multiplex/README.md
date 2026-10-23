# Procedure 5: Chat Client and Server Permitting Multiple Messages (I/O Multiplexing)

## Overview
Overcomes the limitation of half-duplex turn-taking seen in Procedure 4 by employing **I/O Multiplexing** via `select.select()`.

### Key Technical Mechanism
1. The script maintains a list of readable streams: `[sys.stdin, socket]`.
2. `select.select(input_streams, [], [])` blocks until either:
   - The user has entered a line on the keyboard (`sys.stdin` is readable), OR
   - An incoming packet has arrived from the peer (`socket` is readable).
3. If the user types multiple consecutive messages, they are transmitted immediately without needing to wait for a peer response.
4. If the peer sends multiple messages, they are received and displayed instantly.

## How to Run

### Step 1: Start Server
```bash
python3 server.py
```

### Step 2: In a Second Terminal, Start Client
```bash
python3 client.py
```

Type multiple messages consecutively on either terminal to observe non-blocking asynchronous transmission! Type `bye` on either side to conclude the session.
