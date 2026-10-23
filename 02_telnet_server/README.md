# Procedure 2: TCP Server with Telnet / Netcat Interaction

## Overview
Demonstrates creating a TCP server socket on a designated port (`12345`), waiting for incoming connections with `s.listen(5)`, accepting connections via `s.accept()`, and transmitting data back to the client (`Thank you for connecting`).

## Running the Server
Open a terminal and run:
```bash
python3 server.py
```

## Connecting to the Server
### Method 1: Using Netcat (`nc`) (Standard on macOS and Linux)
```bash
nc 127.0.0.1 12345
```
Output:
```
Thank you for connecting
```

### Method 2: Using Telnet (if installed)
```bash
telnet 127.0.0.1 12345
```

### Method 3: Using the provided Python Client
```bash
python3 client.py
```
Output:
```
[*] Connecting to server at 127.0.0.1:12345...
[+] Connected! Waiting for server greeting...
[Server Response]: Thank you for connecting
[+] Client socket closed.
```
