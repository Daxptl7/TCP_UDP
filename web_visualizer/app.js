/**
 * TCP Socket Programming & Protocol Visualizer
 * Interactive Client-Side Simulation & State Machine Engine
 */

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initTcpHandshakeSimulation();
    initProcedure1();
    initProcedure2();
    initProcedure3();
    initProcedure4();
    initProcedure5();
    initProcedure6();
});

/* ----------------------------------------------------
 * Tab Navigation
 * ---------------------------------------------------- */
function initTabs() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");

            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add("active");
            }
        });
    });
}

/* ----------------------------------------------------
 * 0. TCP Handshake & Teardown State Simulation
 * ---------------------------------------------------- */
function initTcpHandshakeSimulation() {
    const clientBadge = document.getElementById("clientStateBadge");
    const serverBadge = document.getElementById("serverStateBadge");
    const clientCall = document.getElementById("clientCurrentCall");
    const serverCall = document.getElementById("serverCurrentCall");
    const packet = document.getElementById("packetElement");
    const packetFlag = document.getElementById("packetFlag");
    const packetDetails = document.getElementById("packetDetails");
    const timelineLog = document.getElementById("timelineLog");

    const btnHandshake = document.getElementById("btnRunHandshake");
    const btnTeardown = document.getElementById("btnRunTeardown");
    const btnReset = document.getElementById("btnResetSimulation");

    let isAnimating = false;

    function addLog(text, type = "system-entry") {
        const entry = document.createElement("div");
        entry.className = `log-entry ${type}`;
        entry.innerHTML = text;
        timelineLog.appendChild(entry);
        timelineLog.scrollTop = timelineLog.scrollHeight;
    }

    function animatePacket(fromLeft, toLeft, flag, details, durationMs = 1200) {
        return new Promise(resolve => {
            packet.style.display = "flex";
            packet.style.transition = "none";
            packet.style.left = fromLeft;
            packetFlag.textContent = flag;
            packetDetails.textContent = details;

            // Trigger reflow
            packet.offsetHeight;

            packet.style.transition = `left ${durationMs / 1000}s cubic-bezier(0.4, 0, 0.2, 1)`;
            packet.style.left = toLeft;

            setTimeout(() => {
                packet.style.display = "none";
                resolve();
            }, durationMs);
        });
    }

    async function runHandshake() {
        if (isAnimating) return;
        isAnimating = true;
        btnHandshake.disabled = true;
        btnTeardown.disabled = true;

        timelineLog.innerHTML = "";
        addLog("▶ <strong>Starting TCP 3-Way Handshake Connection Establishment...</strong>", "system-entry");

        // Client: socket() & connect()
        clientBadge.textContent = "SYN_SENT";
        clientBadge.className = "node-state state-listen";
        clientCall.textContent = "s.connect(('127.0.0.1', 12345))";
        serverCall.textContent = "c, addr = s.accept() [BLOCKING]";

        // Step 1: Client -> Server [SYN]
        addLog("1. [Client → Server] SYN sent: <code>Seq=100</code>, Flags: [SYN]", "packet-c2s");
        await animatePacket("20px", "calc(100% - 160px)", "SYN", "Seq=100");

        // Server receives SYN, transitions to SYN_RCVD
        serverBadge.textContent = "SYN_RCVD";
        serverBadge.className = "node-state state-listen";
        addLog("2. [Server] Received SYN. Transitioned to <strong>SYN_RCVD</strong>. Generating SYN-ACK response.", "system-entry");

        // Step 2: Server -> Client [SYN, ACK]
        addLog("2. [Server → Client] SYN-ACK sent: <code>Seq=300, Ack=101</code>, Flags: [SYN, ACK]", "packet-s2c");
        await animatePacket("calc(100% - 160px)", "20px", "SYN+ACK", "Seq=300, Ack=101");

        // Client receives SYN-ACK, transitions to ESTABLISHED
        clientBadge.textContent = "ESTABLISHED";
        clientBadge.className = "node-state state-established";
        clientCall.textContent = "Connected! s.sendall() / s.recv()";
        addLog("3. [Client] Received SYN-ACK. Transitioned to <strong>ESTABLISHED</strong>. Sending final ACK.", "system-entry");

        // Step 3: Client -> Server [ACK]
        addLog("3. [Client → Server] ACK sent: <code>Seq=101, Ack=301</code>, Flags: [ACK]", "packet-c2s");
        await animatePacket("20px", "calc(100% - 160px)", "ACK", "Seq=101, Ack=301");

        // Server transitions to ESTABLISHED
        serverBadge.textContent = "ESTABLISHED";
        serverBadge.className = "node-state state-established";
        serverCall.textContent = "c.recv() / c.sendall()";
        addLog("✔ <strong>3-Way Handshake Complete! TCP Connection ESTABLISHED.</strong> Both endpoints ready for bidirectional data transfer.", "success-entry");

        isAnimating = false;
        btnHandshake.disabled = false;
        btnTeardown.disabled = false;
    }

    async function runTeardown() {
        if (isAnimating) return;
        isAnimating = true;
        btnHandshake.disabled = true;
        btnTeardown.disabled = true;

        addLog("<br>⏹ <strong>Starting TCP 4-Way Connection Teardown...</strong>", "system-entry");

        // Step 1: Client sends FIN
        clientBadge.textContent = "FIN_WAIT_1";
        clientBadge.className = "node-state state-closed";
        clientCall.textContent = "s.close()";
        addLog("1. [Client → Server] FIN sent: <code>Seq=101, Ack=301</code>, Flags: [FIN, ACK]", "packet-c2s");
        await animatePacket("20px", "calc(100% - 160px)", "FIN", "Seq=101");

        // Step 2: Server sends ACK
        serverBadge.textContent = "CLOSE_WAIT";
        serverBadge.className = "node-state state-closed";
        serverCall.textContent = "Passive close: c.close() pending";
        clientBadge.textContent = "FIN_WAIT_2";
        addLog("2. [Server → Client] ACK sent: <code>Ack=102</code>", "packet-s2c");
        await animatePacket("calc(100% - 160px)", "20px", "ACK", "Ack=102");

        // Step 3: Server sends FIN
        serverBadge.textContent = "LAST_ACK";
        serverCall.textContent = "c.close() executed";
        addLog("3. [Server → Client] FIN sent: <code>Seq=301, Ack=102</code>, Flags: [FIN, ACK]", "packet-s2c");
        await animatePacket("calc(100% - 160px)", "20px", "FIN", "Seq=301");

        // Step 4: Client sends ACK & enters TIME_WAIT
        clientBadge.textContent = "TIME_WAIT";
        addLog("4. [Client → Server] ACK sent: <code>Ack=302</code>. Entering <strong>TIME_WAIT</strong> (2*MSL timer).", "packet-c2s");
        await animatePacket("20px", "calc(100% - 160px)", "ACK", "Ack=302");

        serverBadge.textContent = "CLOSED";
        serverBadge.className = "node-state state-closed";
        addLog("✔ <strong>4-Way Teardown Finished. Connection CLOSED.</strong>", "success-entry");

        isAnimating = false;
        btnHandshake.disabled = false;
        btnTeardown.disabled = false;
    }

    function resetSimulation() {
        clientBadge.textContent = "CLOSED";
        clientBadge.className = "node-state state-closed";
        serverBadge.textContent = "LISTEN";
        serverBadge.className = "node-state state-listen";
        clientCall.textContent = "s = socket(AF_INET, SOCK_STREAM)";
        serverCall.textContent = "s.bind(('', 12345)) & s.listen(5)";
        timelineLog.innerHTML = `<div class="log-entry system-entry">Simulation reset. Click "Play 3-Way Handshake" to visualize TCP packet exchange.</div>`;
    }

    btnHandshake.addEventListener("click", runHandshake);
    btnTeardown.addEventListener("click", runTeardown);
    btnReset.addEventListener("click", resetSimulation);
}

/* ----------------------------------------------------
 * Procedure 1 Simulator: Google Client
 * ---------------------------------------------------- */
function initProcedure1() {
    const btn = document.getElementById("btnSimP1");
    const output = document.getElementById("outputP1");

    btn.addEventListener("click", () => {
        output.innerHTML = "Executing DNS query and TCP handshake...\n";
        setTimeout(() => {
            output.innerHTML = 
`============================================================
 Procedure 1: TCP Socket Connection to Google.com
============================================================
[+] Socket successfully created: socket.socket(AF_INET, SOCK_STREAM)
[+] DNS Resolution: 'www.google.com' resolved to IP: 142.251.150.119
[*] Attempting to connect to www.google.com (142.251.150.119) on port 80...
socket connected to google http server
[+] Local socket endpoint (IP, Port): ('10.2.0.2', 59073)
[+] Remote socket endpoint (IP, Port): ('142.251.150.119', 80)
[+] Sent HTTP HEAD request to remote host.

[+] Response received from Google server (First 1024 bytes):
--------------------------------------------------
HTTP/1.1 200 OK
Content-Type: text/html; charset=ISO-8859-1
Date: Fri, 16 Oct 2026 08:47:14 GMT
Server: gws
Connection: close
--------------------------------------------------

[+] Socket connection closed cleanly.`;
        }, 400);
    });
}

/* ----------------------------------------------------
 * Procedure 2 Simulator: Telnet Server
 * ---------------------------------------------------- */
function initProcedure2() {
    const btnCli = document.getElementById("btnSimP2Client");
    const btnNc = document.getElementById("btnSimP2Nc");
    const output = document.getElementById("outputP2");

    btnCli.addEventListener("click", () => {
        output.innerHTML += `\n[+] Got connection from ('127.0.0.1', 59112)
[Server] Sent: "Thank you for connecting\\n"
[-] Connection with ('127.0.0.1', 59112) closed cleanly.`;
    });

    btnNc.addEventListener("click", () => {
        output.innerHTML += `\n$ nc 127.0.0.1 12345
Thank you for connecting
[Server] Client disconnected via Netcat.`;
    });
}

/* ----------------------------------------------------
 * Procedure 3 Simulator: Echo Single Message
 * ---------------------------------------------------- */
function initProcedure3() {
    const btn = document.getElementById("btnSimP3");
    const input = document.getElementById("inputP3");
    const output = document.getElementById("outputP3");

    btn.addEventListener("click", () => {
        const text = input.value.trim() || "Default Echo Test";
        output.innerHTML = 
`[*] Client connecting to 127.0.0.1:12345...
[+] Connected!
Enter a message to send: ${text}
[+] Transmitting ${text.length} bytes to server...
[Server Log]: Got connection from ('127.0.0.1', 59153)
[Server Log]: received ${text}
[Server Log]: echoing it back
Echo received from server: ${text}
[+] Both sockets closed.`;
    });
}

/* ----------------------------------------------------
 * Procedure 4 Simulator: Turn-Based Chat
 * ---------------------------------------------------- */
function initProcedure4() {
    const clientOut = document.getElementById("outputP4Client");
    const serverOut = document.getElementById("outputP4Server");
    const clientIn = document.getElementById("inputP4Client");
    const serverIn = document.getElementById("inputP4Server");
    const btnClient = document.getElementById("btnSendP4Client");
    const btnServer = document.getElementById("btnSendP4Server");

    btnClient.addEventListener("click", () => {
        const msg = clientIn.value.trim();
        if (!msg) return;

        clientOut.innerHTML += `\nEnter a message to send: ${msg}`;
        serverOut.innerHTML += `\nreceived: ${msg}\n\nEnter a msg: `;
        clientIn.value = "";

        if (msg.toLowerCase() === "bye") {
            clientOut.innerHTML += `\n[*] You ended the conversation.\n[+] Client closed.`;
            serverOut.innerHTML += `\n[*] Client ended conversation with 'bye'.\n[-] Connection closed.`;
            clientIn.disabled = true;
            btnClient.disabled = true;
            serverIn.disabled = true;
            btnServer.disabled = true;
            return;
        }

        // Switch turn to server
        clientIn.disabled = true;
        btnClient.disabled = true;
        serverIn.disabled = false;
        btnServer.disabled = false;
        serverIn.focus();
    });

    btnServer.addEventListener("click", () => {
        const msg = serverIn.value.trim();
        if (!msg) return;

        serverOut.innerHTML += `${msg}\n[+] Waiting for client...`;
        clientOut.innerHTML += `\nreceived: ${msg}`;
        serverIn.value = "";

        if (msg.toLowerCase() === "bye") {
            serverOut.innerHTML += `\n[*] You ended conversation.\n[-] Server closed connection.`;
            clientOut.innerHTML += `\n[*] Server ended the conversation with 'bye'.\n[+] Client closed.`;
            clientIn.disabled = true;
            btnClient.disabled = true;
            serverIn.disabled = true;
            btnServer.disabled = true;
            return;
        }

        // Switch turn to client
        serverIn.disabled = true;
        btnServer.disabled = true;
        clientIn.disabled = false;
        btnClient.disabled = false;
        clientIn.focus();
    });
}

/* ----------------------------------------------------
 * Procedure 5 Simulator: Multiplexed Chat via select()
 * ---------------------------------------------------- */
function initProcedure5() {
    const clientOut = document.getElementById("outputP5Client");
    const serverOut = document.getElementById("outputP5Server");
    const clientIn = document.getElementById("inputP5Client");
    const serverIn = document.getElementById("inputP5Server");
    const btnClient = document.getElementById("btnSendP5Client");
    const btnServer = document.getElementById("btnSendP5Server");

    btnClient.addEventListener("click", () => {
        const msg = clientIn.value.trim();
        if (!msg) return;

        clientOut.innerHTML += `\n&lt;You&gt; ${msg}`;
        serverOut.innerHTML += `\n&lt;received&gt; ${msg}`;
        clientIn.value = "";

        if (msg.toLowerCase() === "bye") {
            clientOut.innerHTML += `\n[*] Disconnected.`;
            serverOut.innerHTML += `\n[-] Client disconnected.`;
        }
    });

    btnServer.addEventListener("click", () => {
        const msg = serverIn.value.trim();
        if (!msg) return;

        serverOut.innerHTML += `\n&lt;You&gt; ${msg}`;
        clientOut.innerHTML += `\n&lt;received&gt; ${msg}`;
        serverIn.value = "";

        if (msg.toLowerCase() === "bye") {
            serverOut.innerHTML += `\n[*] Connection closed.`;
            clientOut.innerHTML += `\n[-] Server disconnected.`;
        }
    });
}

/* ----------------------------------------------------
 * Procedure 6 Simulator: Multi-Client Chat Room Broadcast
 * ---------------------------------------------------- */
function initProcedure6() {
    const outA = document.getElementById("outputP6A");
    const outB = document.getElementById("outputP6B");
    const outC = document.getElementById("outputP6C");
    const outServer = document.getElementById("outputP6Server");

    const inA = document.getElementById("inputP6A");
    const inB = document.getElementById("inputP6B");
    const inC = document.getElementById("inputP6C");

    function broadcastMsg(senderName, port, text, senderOut, otherOuts) {
        if (!text) return;

        // Local sender sees <You>
        senderOut.innerHTML += `\n&lt;You&gt; ${text}`;
        senderOut.scrollTop = senderOut.scrollHeight;

        // Server logs the message
        outServer.innerHTML += `\n&lt;127.0.0.1:${port}&gt; (${senderName}) ${text}`;
        outServer.scrollTop = outServer.scrollHeight;

        // Other clients receive broadcast
        otherOuts.forEach(o => {
            o.innerHTML += `\n&lt;127.0.0.1:${port}&gt; ${text}`;
            o.scrollTop = o.scrollHeight;
        });
    }

    document.getElementById("btnSendP6A").addEventListener("click", () => {
        const text = inA.value.trim();
        inA.value = "";
        broadcastMsg("Alice", 54101, text, outA, [outB, outC]);
    });

    document.getElementById("btnSendP6B").addEventListener("click", () => {
        const text = inB.value.trim();
        inB.value = "";
        broadcastMsg("Bob", 54102, text, outB, [outA, outC]);
    });

    document.getElementById("btnSendP6C").addEventListener("click", () => {
        const text = inC.value.trim();
        inC.value = "";
        broadcastMsg("Charlie", 54103, text, outC, [outA, outB]);
    });
}
