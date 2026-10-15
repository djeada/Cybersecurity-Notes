# Vulnerability and Risk Assessment

### Conducting Risk Assessment

**General Risk Management Strategies:**
1. **Transfer Risk:** Shift the risk to a third party, such as through insurance or outsourcing.
2. **Avoid Risk:** Avoid the risk by not using specific technology or equipment.
3. **Reduce Risk:** Minimize damage and attack surface by implementing defense mechanisms.
4. **Accept Risk:** Acknowledge and accept the consequences of the risk.

**Risk Assessment Process:**
1. **Identify Company Assets:** Determine what assets need protection.
2. **Identify Vulnerabilities:** Assess weaknesses that could be exploited.
3. **Identify Threats and Likelihood:** Evaluate potential threats and how likely they are to occur.
4. **Identify Monetary Impact:** Estimate the financial impact of potential risks.

- **Risk Register:** A record of risk assessment, often referenced and updated regularly.

---

### Qualitative vs. Quantitative Risk Assessment

**Qualitative Risk Assessment:**
- **Description:** Assigns numeric values to the probability of risk and its potential impact. 
- **Challenges:** Difficult to estimate exact values, often relies on historical data and surveys.

**Quantitative Risk Assessment:**
- **Description:** Measures risk using exact monetary losses.
- **Key Metrics:**
  1. **Single Loss Expectancy (SLE):** The expected monetary loss from a single event.
  2. **Annual Rate of Occurrence (ARO):** How often a risk is expected to occur annually.
  3. **Annual Loss Expectancy (ALE):** Calculated as SLE multiplied by ARO.
  4. **Mean Time Between Failures (MTBF):** Average number of failures in a million hours of operation.

---

### Active vs. Passive Security Analysis

**Active Security Analysis:**
- **Description:** Involves actual testing, which may interfere with regular operations.
- **Example:** Active scanning.

**Passive Security Analysis:**
- **Description:** Involves analyzing network documentation without interfering with the network.
- **Example:** Passive fingerprinting.

---

### Security Controls

**Categorical Controls:**
1. **Management Controls:** Focus on executive-level decisions and risk management.
2. **Operational Controls:** Focus on individuals, including user awareness, incident handling, and fault tolerance.
3. **Technical Controls:** Focus on the system, such as firewall configurations and IPS/IDS settings.

**Definitive Controls:**
4. **Preventative Controls:** Employed before an event to prevent occurrences.
5. **Detective Controls:** Employed during an event to identify malicious activity.
6. **Corrective Controls:** Employed after an event to minimize damage.

---

### Vulnerability Management

**Five-Step Process:**
1. **Define a Desired State of Security:** Establish what security should look like.
2. **Create a Baseline:** Determine the current state of security.
3. **Vulnerability Prioritization:** Prioritize vulnerabilities based on risk.
4. **Mitigate Vulnerability:** Implement measures to address vulnerabilities.
5. **Monitor Environment:** Continuously monitor the environment for new vulnerabilities.

---

### Penetration Testing

**Description:**
- A method of demonstrating vulnerabilities found during risk assessment by exploiting them.

**Types:**
1. **Black Box Testing:** No prior knowledge of the system.
2. **Gray Box Testing:** Limited knowledge of the system.
3. **Glass Box Testing:** Full knowledge of the system.

**Key Concepts:**
- **Pivot:** Launching additional exploits after gaining a network foothold.
- **Persistence and Backdoors:** Methods attackers use to maintain access to a compromised system.
- **Race Conditions:** Situations where the outcome depends on the timing of uncontrollable events.

**Basic Methodologies:**
1. **OSSTMM:** Open Source Security Testing Methodology Manual.
2. **NIST Pen Testing Standard:** A guideline for penetration testing by the National Institute of Standards and Technology.
- **OVAL:** Standardized secure transfer of information on security.

---

### Assessing Vulnerabilities with Security Tools

**Network Mapping:**
- **Purpose:** Draw out the physical and logical connections of the network.
- **Tools:** Network Topology Mapper, AirMagnet (for WiFi).
- **Details to Include:** Devices, IP addresses, roles, connections.

**Vulnerability Scanning:**
- **Tools:**
  - **Nessus:** Basic vulnerability scanner.
  - **Nmap:** Basic port scanner.

**Network Enumeration and Banner Grabbing:**
- **Purpose:** Gather information about the network and its devices.

**Network Sniffing:**
- **Description:** Capturing and analyzing packets on a network.
- **Tools:**
  - **Wireshark:** Basic packet analyzer.
  - **Fluke Networks:** Hardware-based network tester.

**Password Analysis:**
- **Purpose:** Test the strength of passwords.
- **Tools:** Cain and Abel, John the Ripper, Hydra, Aircrack-ng suite.

**Password Storage Locations:**
- **Windows:** Stored in the SAM hive, typically encrypted.
- **Linux:** Stored in `/etc/passwd` or `/etc/shadow`, also encrypted.
