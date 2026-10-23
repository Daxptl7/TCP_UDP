# Procedure 1: Client Program Connecting to Google.com

## Objective
Study basic client socket creation, DNS name resolution, and establishing a TCP connection to an active remote server (`www.google.com` on port 80).

## Key Socket Concepts Demonstrated
1. **Socket Allocation**: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` allocates a TCP endpoint.
2. **DNS Resolution**: `socket.gethostbyname('www.google.com')` queries the DNS resolver to map the hostname to an IPv4 address.
3. **Three-Way Handshake**: `s.connect((host, port))` triggers the OS TCP stack to send `[SYN]`, await `[SYN-ACK]`, and reply `[ACK]`.
4. **HTTP Protocol Interaction**: Once connected, an HTTP request (`HEAD / HTTP/1.1`) is transmitted using `s.sendall()`.
5. **Data Reception & Teardown**: Server response headers are read using `s.recv(1024)`, decoded from bytes to string, and the socket is closed using `s.close()`.

## How to Run
```bash
python3 client.py
```

## Sample Output
```
============================================================
 Procedure 1: TCP Socket Connection to Google.com
============================================================
[+] Socket successfully created.
[+] DNS Resolution: 'www.google.com' resolved to IP address: 142.251.150.119
[*] Attempting to connect to www.google.com (142.251.150.119) on port 80...
socket connected to google http server
[+] Local socket endpoint (IP, Port): ('10.2.0.2', 59073)
[+] Remote socket endpoint (IP, Port): ('142.251.150.119', 80)
[+] Sent HTTP HEAD request to remote host.

[+] Response received from Google server (First 1024 bytes):
--------------------------------------------------
HTTP/1.1 200 OK
Content-Type: text/html; charset=ISO-8859-1
...
--------------------------------------------------

[+] Socket connection closed cleanly.
```
