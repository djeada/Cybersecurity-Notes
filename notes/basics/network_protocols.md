# Networking Protocols and Threats

### Ports and Protocols

#### Port Ranges, Inbound vs. Outbound, Common Ports
- **Ports:** Logical communication endpoints that are essential for network protocols.
- **TCP vs. UDP:**
  - **TCP (Transmission Control Protocol):** Ensures ordered, reliable communication, making it connection-oriented.
  - **UDP (User Datagram Protocol):** Connectionless datagrams without built-in
    delivery or ordering guarantees; applications may implement those properties.
- **Port Ranges:**
  - **0 – 1023:** Well-known ports (e.g., HTTP, FTP).
  - **1024 – 49151:** Registered ports for proprietary applications.
  - **49152 – 65535:** Dynamic and private ports, used for temporary or custom communications.

#### Inbound vs. Outbound Ports
- **Inbound Ports:** Usually involve well-known ports that need to be secured by an administrator.
- **Outbound Ports:** Used to initiate connections from a client to a server; dynamic port assignment can enhance security.

#### Well-Known Ports
| Port  | Protocol | TCP/UDP | Secure Version | Usage                                             |
|-------|----------|---------|----------------|---------------------------------------------------|
| 21    | FTP      | TCP     | Explicit FTPS on 21; implicit FTPS on 990 | File transfer; SFTP is a separate SSH-based protocol |
| 22    | SSH      | TCP     | Secure by design when configured correctly | Remote shell and SFTP |
| 23    | Telnet   | TCP     | Use SSH instead | Plaintext remote administration |
| 25    | SMTP     | TCP     | SMTP w/ TLS, 465/587 | Sends email                                 |
| 53    | DNS      | TCP/UDP | DoT on TCP 853; DoH over HTTPS | DNSSEC authenticates signed data; it does not encrypt queries |
| 80    | HTTP     | TCP     | HTTPS, 443     | Transmit web page data                            |
| 110   | POP3     | TCP     | POP3 w/ TLS, 995 | Receives email                                  |
| 143   | IMAP     | TCP     | IMAP4 w/ TLS, 993 | Email retrieval                              |
| 389   | LDAP     | TCP     | StartTLS on 389; LDAPS on 636 | Directory access; connectionless LDAP is a separate UDP use |
| 445   | SMB      | TCP     | SMB 3 supports encryption | File sharing; require signing/encryption according to policy |
| 514   | Syslog   | UDP     | Syslog w/ TLS, 6514 | Computer message logging                      |
| 3389  | RDP      | TCP/UDP | N/A            | Remote Desktop Protocol for Windows               |

Ports are defaults, not proof of the service or its security. HTTPS can also use
QUIC over UDP 443 for HTTP/3. DNSSEC validates signed DNS data; encrypted DNS
transport protects the path to a resolver and solves a different problem.

### Malicious Attacks

#### Denial of Service (DOS) – Resource Depletion Attacks
- **Flood Attack:** 
  - **Ping Floods:** Excessive ICMP traffic; use appropriate filtering and rate
    limits rather than disabling all ICMP, which can break network diagnostics
    and path-MTU discovery.
  - **Smurf Attack:** Redirects ICMP echoes to a spoofed IP address.
  - **SYN Flood:** Sends excessive TCP SYN packets to overwhelm a target.
  - **Xmas Packets:** Typically set FIN, PSH, and URG flags; they may be used in
    probing. There is no general guarantee that these packets reboot routers.
- **Ping of Death:** Sends oversized or malformed packets to crash services (mostly mitigated by modern OSes).
- **Teardrop Attack:** Mangled IP fragments crash IP reassembly code.
- **Permanent DOS:** Flashes custom images onto routers or devices, rendering them unusable.
- **Fork Bomb:** Forces numerous processes, saturating the processor.

#### Distributed Denial of Service (DDOS)
- Utilizes botnets to overwhelm and DOS a target.
- Common defenses: upstream traffic filtering, provider DDoS mitigation, capacity
  planning, and application limits. A local firewall alone cannot recover an
  already saturated upstream link.

#### Spoofing Attacks
- **Spoofing:** Impersonation of various identifiers like IP, MAC addresses, or session tokens.
- **Session Hijacking:** 
  - **Session Theft:** Hijacking browser sessions through cookies.
  - **TCP/IP Hijacking:** Predicts the next sequence number in TCP to inject data.
  - **Blind Hijacking:** Injects data without knowing the session state.
- **Man-in-the-Middle (MitM):** Intercepts and possibly alters communication between two parties.

#### Replay Attacks
- Attacker saves and reuses valid packets later.
- **Defenses:** Use session tokens, timestamps, synchronization, cryptography, and nonces.

#### Null Session
- Uses ports 139 and 445 (NetBIOS and SMB) to establish unauthenticated connections, often on older Windows systems.

#### Transitive Access and Client-side Attacks
- Compromising a trusted user to indirectly compromise a server.
- **Defenses:** Only establish temporary, necessary trust relationships.

#### DNS Poisoning
- Improper modification of DNS information, redirecting users to malicious sites.
- **Defenses:** TLS, DNSSEC, TSIG, and regular server patches.

#### ARP Poisoning
- ARP resolves IP addresses to MAC addresses.
- **Defense:** Segmentation limits scope; switch features such as Dynamic ARP
  Inspection, with correctly maintained bindings, can validate ARP messages.
  ARP itself has no authentication.

## Sources

- [IANA service names and port numbers](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- [RFC 4033: DNSSEC introduction](https://www.rfc-editor.org/rfc/rfc4033.html)
- [RFC 8484: DNS over HTTPS](https://www.rfc-editor.org/rfc/rfc8484.html)
