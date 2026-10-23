# Procedure 4: Turn-Based Chat Client and Server

## Overview
Demonstrates half-duplex (taking turns) communication over a TCP connection:
- Client initiates by sending a message.
- Server waits (`recv`), reads the message, prints it, and replies with `input()`.
- Client reads the reply, prints it, and prepares next input.
- Communication cleanly terminates when either side transmits `bye`.

## How to Run

### Step 1: Start Server
```bash
python3 server.py
```

### Step 2: In a Second Terminal, Start Client
```bash
python3 client.py
```

### Example Interaction
**Client Terminal:**
```
[+] Connected to Chat Server at 127.0.0.1:12345
    Type 'bye' to exit the chat.

Enter a message to send: Hello Server
received: Hi Client, how are you?
Enter a message to send: I am learning socket programming!
received: That is awesome!
Enter a message to send: bye
[*] You ended the conversation.
[+] Chat client closed.
```

**Server Terminal:**
```
[+] Got connection from ('127.0.0.1', 59188)
    Waiting for client to send the first message...

received: Hello Server

Enter a msg: Hi Client, how are you?
received: I am learning socket programming!

Enter a msg: That is awesome!
received: bye

[*] Client ended conversation with 'bye'.
[-] Closed connection with ('127.0.0.1', 59188).
```
