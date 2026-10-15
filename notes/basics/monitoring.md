# Monitoring and Auditing

### Monitoring Methodologies

Effective monitoring is crucial for maintaining security and performance within an IT environment. The following methodologies are commonly used:

#### 1. Signature-Based Monitoring
- **Function:** Matches network traffic against predefined attack patterns and packet/frame signatures.
- **Limitations:** Susceptible to false negatives and requires constant updates to remain effective.

#### 2. Anomaly-Based Monitoring
- **Function:** Establishes a baseline of normal activity and detects deviations from this baseline.
- **Limitations:** An inaccurate baseline can lead to false positives, making it essential to carefully define what constitutes normal behavior.

#### 3. Behavior-Based Monitoring
- **Function:** Compares current application behavior to previous behavior patterns, identifying anomalies.
- **Limitations:** Prone to false positives due to the diversity of application behaviors.

---

### Using Tools to Monitor Systems and Networks

**Performance Baselining:**
- **Definition:** Establishing a performance baseline allows for comparison over time, identifying significant deviations that may indicate issues.
- **Baseline Reporting:** Involves comparing current performance data to the established baseline to detect and address abnormalities.

**Security Posture vs. Security Posture Assessment:**
- **Security Posture:** The overall security status of an organization, including policies, procedures, and controls.
- **Security Posture Assessment:** The process of evaluating and improving the security posture.

**Protocol Analyzer:**
- **Function:** Captures and analyzes network traffic to identify and troubleshoot issues.
- **Modes for Network Adapters:**
  - **Promiscuous Mode:** Accepts frames delivered to the adapter even when addressed
    to other hosts. It does not make a switched network deliver every frame;
    appropriate capture placement, a mirror port, or a tap is still required.
  - **Non-Promiscuous Mode:** Captures only traffic addressed to the specific adapter.

**Key Analysis Techniques:**
- **Broadcast Storm Analysis:** Identifies excessive broadcast traffic that can overwhelm network resources.
- **Header Manipulation Detection:** Examines packet headers for signs of tampering or unauthorized modification.
- **TCP Handshake Analysis:** Monitors the TCP handshake process to ensure proper connection establishment.

**Tools:**
- **Wireshark:**
  - **Promiscuous Mode Capturing:** Captures frames visible at the capture interface;
    visibility depends on network topology and capture placement.
  - **Port Mirroring:** Duplicates traffic from one port to another for monitoring purposes.
  - **Network Tap:** A dedicated device that copies traffic for analysis.
- **Tcpdump (Unix/Linux):** A command-line packet analyzer.

**SNMP (Simple Network Management Protocol):**
- **Function:** Monitors and manages network-attached devices.
- **Usage Scenarios:**
  - **Managed Devices:** Devices that are monitored and managed via SNMP.
  - **Agents:** Software on devices that report to the network management system.
  - **Network Management System:** The central system that collects and analyzes SNMP data.
- **Management Types:**
  - **Inbound Management:** Commands sent from the management system to the devices.
  - **Outbound Management:** Information sent from devices to the management system.

---

### Analytical Tools

**Windows Tools:**
- **compmgmt.msc & openfiles:** Manage and view open files and shared resources.
- **net file & suite/netstat:** Network statistics and connection management.

**Linux Tools:**
- **lsof (list open files) & netstat:** Monitor open files and network connections.

**Static vs. Dynamic Tools:**
- **Static Tools:** Provide a snapshot of the current network state (e.g., openfiles, netstat).
- **Dynamic Tools:** Capture and analyze data over time (e.g., Task Monitor, Wireshark).

---

### Conducting Audits

**Manual Assessment:**
- **Focus Areas:** Review security logs, Access Control Lists (ACLs), user rights, permissions, and group policies.
- **Additional Methods:** Conduct vulnerability scans and personnel interviews to gather comprehensive information.

**Overall Audit Process:**
1. **Define Audit Target:** Clearly identify what will be audited.
2. **Create Backups:** Ensure data is preserved before making changes.
3. **Scan, Analyze, and List Vulnerabilities/Issues:** Conduct thorough scanning and analysis.
4. **Calculate Risk:** Assess the potential impact of identified vulnerabilities.
5. **Develop a Mitigation Plan:** Create a strategy to address and minimize risks.

**Auditing Files:**
- **Capabilities:** Set auditing and logging for specific files, folders, and users.
- **Review Logs:** Support accountability with protected, attributable records;
  logging alone does not guarantee non-repudiation.

---

### Logging

**Windows Logging:**
- **Tool:** Use `compmgmt.msc` to view and manage security logs.
- **Additional Logs:** Pay attention to system and application logs.

**Syslog:**
- **Function:** Centralized log monitoring for aggregating logs from multiple systems.

---

### Log File Maintenance and Security

**Key Practices:**
- **Log File Size Management:** Regularly monitor and configure log file sizes.
- **Configuration and Encryption:** Ensure logs are securely configured and encrypted.
- **Retention:** Rotate and archive logs under a defined retention policy. Monitor
  storage capacity and collection failures; do not routinely clear evidence.

## Detection and response

Centralize useful identity, endpoint, network, application, and cloud audit events.
Synchronize clocks and retain timezone information. Record who did what, to which
resource, when, and with what outcome, without logging passwords or access tokens.
Protect access, transport, retention, and deletion of the records.

A SIEM correlates events; EDR supplies endpoint visibility and response actions.
Neither guarantees detection. Give each alert an owner, triage steps, and an
escalation path. Review false positives, missed activity, and telemetry gaps.

See [incident response](incident_response.md) and [digital forensics](digital_forensics.md).

## Sources

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Wireshark: capturing packets](https://www.wireshark.org/docs/wsug_html_chunked/ChapterCapture.html)

**Auditing System Security Settings:**
- **Management:** Use `compmgmt.msc` to manage shared folders and user privileges.
