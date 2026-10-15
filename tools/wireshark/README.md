# Wireshark Cheat Sheet

## 1. **Installation**
   - **Ubuntu/Debian:** 
     ```bash
     sudo apt-get install wireshark
     ```
   - **Fedora/CentOS:**
     ```bash
     sudo yum install wireshark-gnome
     ```
   - **Windows:**
     - Download the installer from [Wireshark's official site](https://www.wireshark.org/download.html) and follow the installation wizard.

## 2. **Capture Filters**
   Filters that limit the packets Wireshark captures.
   
   | Syntax | Description |
   |--------|-------------|
   | `host 192.168.1.1` | Capture traffic to/from a specific IP |
   | `net 192.168.0.0/24` | Capture traffic within a specific subnet |
   | `port 443` | Capture traffic on a specific port (e.g., HTTPS) |
   | `tcp` | Capture only TCP traffic |
   | `udp` | Capture only UDP traffic |
   | `not arp` | Exclude ARP packets from capture |

## 3. **Display Filters**
   Filters that control which packets are displayed after capture.
   
   | Syntax | Description |
   |--------|-------------|
   | `ip.addr == 192.168.1.1` | Display packets from/to a specific IP |
   | `tcp.port == 80` | Display HTTP traffic (port 80) |
   | `http` | Display only HTTP traffic |
   | `tcp.flags.syn == 1` | Display packets with the SYN flag set |
   | `eth.addr == ff:ff:ff:ff:ff:ff` | Display broadcast traffic |
   | `!(ip.addr == 192.168.1.1)` | Exclude traffic from/to a specific IP |
   | `frame.time >= "2022-01-01 00:00:00"` | Display packets after a specific date/time |

## 4. **Keyboard Shortcuts**
   Common shortcuts to streamline your workflow.
   
   | Shortcut | Action |
   |----------|--------|
   | `Ctrl + E` | Start/Stop capturing |
   | `Ctrl + F` | Open display filter dialog |
   | `Ctrl + G` | Go to the next packet matching the current display filter |
   | `Ctrl + R` | Apply or reapply the current display filter |
   | `Ctrl + Shift + R` | Clear the current display filter |
   | `F12` | Toggle the time display format between absolute and relative |

## 5. **Main Toolbar Items**
   Essential options accessible via the toolbar.
   
   | Icon | Menu Item | Description |
   |------|-----------|-------------|
   | ![Start Icon](https://www.wireshark.org/docs/wsug_html_chunked/figures/ws-main-toolbar.png) | Capture → Start | Start capturing packets |
   | ![Stop Icon](https://www.wireshark.org/docs/wsug_html_chunked/figures/ws-main-toolbar.png) | Capture → Stop | Stop current capture |
   | ![Restart Icon](https://www.wireshark.org/docs/wsug_html_chunked/figures/ws-main-toolbar.png) | Capture → Restart | Restart the capture session |
   | ![Find Icon](https://www.wireshark.org/docs/wsug_html_chunked/figures/ws-main-toolbar.png) | Edit → Find Packet… | Search for packets based on specific criteria |
   | ![Colorize Icon](https://www.wireshark.org/docs/wsug_html_chunked/figures/ws-main-toolbar.png) | View → Colorize | Apply color rules to packets |

## 6. **Advanced Features**
   Powerful features for deep packet analysis.
   
   | Feature | Description |
   |---------|-------------|
   | **Follow TCP Stream** | Reconstructs the data stream of a TCP connection. Useful for viewing HTTP sessions. |
   | **Protocol Decode** | Decodes packet contents according to the protocol specification. |
   | **Conversation Statistics** | Displays statistics about communication between endpoints. |
   | **GeoIP Mapping** | Maps IP addresses to geographical locations (requires GeoIP database). |
   | **Decrypt SSL/TLS** | Decrypts SSL/TLS traffic if you have the server’s private key or using a browser’s SSL session. |

## 7. **TShark Command-Line Tool**
   The command-line version of Wireshark.
   
   | Command | Description |
   |---------|-------------|
   | `tshark -i eth0` | Start capture on interface eth0 |
   | `tshark -r capture.pcap` | Read packets from a capture file |
   | `tshark -T fields -e ip.src -e ip.dst` | Display only the source and destination IPs |

---

### **Helpful Tips**
- **Resolving DNS Names:** Enable under `Edit → Preferences → Name Resolution`.
- **Customizing Columns:** Right-click on any column header to add/remove fields such as IP addresses, ports, etc.
- **Exporting Data:** Wireshark allows exporting packets to various formats including CSV, JSON, and XML.

## Resources

Here's a list of useful websites that you can use alongside Wireshark for various purposes, such as packet visualization, protocol analysis, and educational resources:

- **PacketTotal**: [https://packettotal.com/](https://packettotal.com/)  
- **ProtocolAnalyser**: [https://protocolanalyzer.com/](https://protocolanalyzer.com/)  
- **NetworkXray**: [https://networkxray.com/](https://networkxray.com/)  
- **MaxMind GeoIP**: [https://www.maxmind.com/en/geoip2-databases](https://www.maxmind.com/en/geoip2-databases)  
- **IPinfo**: [https://ipinfo.io/](https://ipinfo.io/)  
- **VirusTotal**: [https://www.virustotal.com/](https://www.virustotal.com/)  
- **Hybrid Analysis**: [https://www.hybrid-analysis.com/](https://www.hybrid-analysis.com/)  
- **CloudShark**: [https://www.cloudshark.org/](https://www.cloudshark.org/)  
- **PCAP Analyzer**: [https://pcapanalyzer.com/](https://pcapanalyzer.com/)
