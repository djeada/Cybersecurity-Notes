# Network Basics

Networking connects systems through physical links, addressing, routing, and
application protocols. Security depends on which paths and services are exposed,
how peers authenticate, and what traffic defenders can observe.

## OSI model

The OSI model is a conceptual reference; real protocols do not always fit neatly
into one layer.

| Layer | Purpose | Examples or units |
| --- | --- | --- |
| 7 — Application | Protocols used by applications | HTTP, DNS, SMTP |
| 6 — Presentation | Representation and transformation of data | Encoding and serialization concepts |
| 5 — Session | Establishing and managing conversations | Session coordination concepts |
| 4 — Transport | Communication between application endpoints | TCP segments, UDP datagrams, ports |
| 3 — Network | Addressing and routing between networks | IPv4/IPv6 packets, routers |
| 2 — Data link | Delivery on a local link | Ethernet frames, MAC addresses, switches |
| 1 — Physical | Transmission over a medium | Electrical, optical, or radio signals |

TCP provides an ordered byte stream with retransmission. UDP does not guarantee
delivery or ordering. Applications can build reliability over UDP, as QUIC does.

## Devices and observation

| Component | Main function | Security consideration |
| --- | --- | --- |
| Switch or bridge | Forward local-link frames using learned MAC locations | Protect management access and prevent loops |
| Router | Forward packets between IP networks | Restrict routes and apply access policies |
| Firewall | Enforce traffic rules, sometimes with connection or application state | Rules require review and logging |
| Forward proxy | Make requests on behalf of clients | Protect proxy configuration and credentials |
| Reverse proxy | Receive requests on behalf of services | Define trust in forwarded headers and protect backend paths |
| Network tap or mirror port | Copy traffic for observation | Capture only what the observation point can see |

Promiscuous mode does not cause a switch to send every frame to the capture host.
See [monitoring](monitoring.md) and [perimeter security](network_perimeter_security.md).

## Addressing, NAT, and subnetting

IPv4 addresses have 32 bits; IPv6 addresses have 128. A CIDR prefix states how many
leading bits identify the network.

Private IPv4 ranges are `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`.
They are not globally routed on the public internet, but can be routed inside an
organization. Addressing alone is not access control. IPv6 also has scoped
address types, including link-local and unique local addresses; secure both
protocol stacks rather than assuming IPv6 is inherently unsafe.

NAT translates addresses and sometimes ports. **Static NAT** generally provides
a fixed mapping; **PAT/NAPT** can share one public address among many connections.
NAT does not replace a firewall.

For `192.168.1.0/28`:

- The mask is `255.255.255.240`.
- Four host bits give 16 addresses in the subnet.
- The conventional network and broadcast addresses are `.0` and `.15`, leaving
  `.1` through `.14` for hosts.
- A `/24` can be divided into sixteen `/28` subnets. The next begins at `.16`.

Class A/B/C terminology is historical; use CIDR for modern addressing plans.

## Segmentation and access

A VLAN separates layer-two broadcast domains. Routing between VLANs needs policy
enforcement; creating VLANs alone does not prevent access across them. Disable
unused switch ports, restrict trunking, and manage allowed VLANs.

A DMZ is a network segment for exposed services with controlled paths to internal
systems. Network Access Control (NAC) can evaluate device or user access before
admission. Neither internal placement nor a successful network admission check
should grant unlimited application access.

Voice services, remote administration, and management interfaces also need
authentication, updates, restricted network paths, and appropriate transport
protection. Moving a service to a different port is not a substitute.

## Related notes

- [Network protocols and ports](network_protocols.md)
- [Network media](network_media.md)
- [Wi-Fi security](wifi_security.md)
- [VPNs](vpn.md)
- [Cloud and container security](cloud_security.md)

## Sources

- [RFC 1918: private IPv4 addressing](https://www.rfc-editor.org/rfc/rfc1918.html)
- [RFC 4632: CIDR](https://www.rfc-editor.org/rfc/rfc4632.html)
- [RFC 8200: IPv6](https://www.rfc-editor.org/rfc/rfc8200.html)
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000.html)
