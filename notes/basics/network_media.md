# Securing Network Media and Devices

### Wired Networks

**Vulnerabilities:**
Wired networks encompass various types of devices such as routers, switches, firewalls, and NIDS/NIPS, each with its own vulnerabilities.

1. **Default Accounts:**
   - Many devices come with default usernames and passwords that are public knowledge.
   - **Action:** Change the username/password before connecting the device to the web.

2. **Weak Passwords:**
   - **Risk:** Easier for attackers to guess or brute-force weak passwords.

3. **Privilege Escalation:**
   - **Types:**
     - **Vertical Privilege Escalation:** A lower-privilege user gains access to higher-privilege functions (e.g., user → admin).
     - **Horizontal Privilege Escalation:** A user accesses functions or data meant for another user (e.g., user1 → user2).
   - **Risks:** Kernel access, DRM bypass, jailbreaking, malware installation.

4. **Backdoors:**
   - **Definition:** Methods that bypass traditional authentication, often due to faulty code, RAT software, or rootkits.

5. **Network Attacks:**
   - **Types:** Denial of Service (DoS)/Distributed Denial of Service (DDoS), Spoofing, etc.

---

### Cable Media Vulnerabilities

**Types of Cables:**
- **Twisted Pair**
- **Fiber Optic**
- **Coax**

1. **Electromagnetic / Radio Frequency Interference:**
   - **Risk:** Creates noise and unwanted signals.
   - **Solution:** Use cable shielding.

2. **Crosstalk:**
   - **Definition:** Interference caused by wires placed in proximity.
   - **Solution:** Use twisted pair cables to minimize/eliminate crosstalk.
   - **Measurements:**
     - **NEXT (Near End Crosstalk):** Interference measured closest to the noise source.
     - **FEXT (Far End Crosstalk):** Interference measured furthest from the noise source.

3. **Data Emanation:**
   - **Definition:** Data leakage through electromagnetic (EM) field generation.
   - **Solution:** Use shielded cables or Faraday cages to prevent EM field leakage.
   - **Reference:** Follow U.S. government TEMPEST guidelines.

4. **Wiretapping:**
   - **Methods:**
     - Using a butt set on RJ11/punch block.
     - Plugging into open twisted pair ports on routers/switches/hubs.
     - Splitting twisted pair connections and cables.
     - Using spectral analyzers to detect electric signals on cables.
     - Passive optical splitters for fiber optics wiretapping.

**Wiring Closets:**
- **IDF (Intermediate Distribution Frame):** Typically one per floor.
- **MDF (Main Distribution Frame):** Central point where all IDFs connect, often connects to ISPs.
- **Security Risk:** SNMP-monitored devices (e.g., PDU, UPS) can be exploited by attackers to bypass security measures and attack IDF/MDF.

---

### Securing Wireless Networks

**Vulnerabilities:**

1. **Administration Interface (Roguing):**
   - **Risk:** Default username/password on administration consoles.
   - **Action:** Change default credentials.

2. **SSID Broadcasting:**
   - **Action:** Disable under normal circumstances, enable only when connecting a new device.

3. **Rogue Access Point:**
   - **Risk:** Unauthorized access points.
   - **Action:** Use graphing tools to monitor and investigate any undocumented APs.

4. **Evil Twin:**
   - **Definition:** A rogue AP that uses the same SSID as a legitimate AP.
   - **Solution:** Use a VPN that requires an additional authentication step.

5. **Weak Encryption:**
   - **Current Standard:** WPA2, PSK with wireless transport layer security.
   - **Protocol Descriptions:**
     - **WEP:** Wired Equivalent Privacy (Deprecated) - 64-bit.
     - **WPA:** WiFi Protected Access - 128-bit.
     - **WPA2:** WiFi Protected Access version 2 - 256-bit.
     - **TKIP:** Temporal Key Integrity Protocol (Deprecated) - 128-bit.
     - **CCMP:** Counter Mode with CBC-MAC Protocol - 128-bit.
     - **AES:** Advanced Encryption Standard - 128/192/256-bit.
     - **WTLS:** Wireless Transport Layer Security - Based on TLS.

6. **WPS (Wireless Protected Setup):**
   - **Action:** Disable in all cases as it can easily be brute-forced and compromised.

7. **Ad Hoc Networks:**
   - **Definition:** Wireless connections between clients without central control.
   - **Action:** Disallow in all cases as they are massively insecure.

8. **VPN over Open Wireless:**
   - **Action:** Ensure that all wireless VPN connections are secured with suitable encryption protocols (e.g., PPTP, IPSec).

**Wireless Access Point Security Strategy:**
- Minimize external signal bleeding and employ electromagnetic shielding.
- Conduct wireless site surveys to gauge signal strength and locate interference.
- Use built-in firewalls and Network Address Translation (NAT) on WAPs.
- Employ MAC filtering if possible.
- Implement AP isolation to segment each client on the WAP, preventing client-to-client communication.
- Utilize encryption on the application layer as well.
- Use a WLAN controller to centralize WAP management.

---

### Wireless Transmission Attacks

1. **War Driving/War Chalking**
2. **IV Attack**
3. **MAC Spoofing**
4. **Deauthentication (Deauth)**
5. **Dictionary/Brute Force Attacks on WAP Passwords**

---

### Bluetooth and Other Devices

**Bluetooth and NFC (Near Field Communication):**
- **Bluetooth Attacks:**
  - **Bluejacking:** Unsolicited Bluetooth messages.
  - **Bluesnarfing:** Unauthorized access to information from Bluetooth devices.

**RFID (Radio Frequency Identification):**
- **Usage:** Often used in authentication.
- **Security:** Modern RFID chips have better encryption and shielding, making them more secure.
- **Communication:** Uses very close range NFC (up to 4 cm) for communication and authentication.

**Other Wireless Technologies:**
- **Cell Signals:** Typically disabled within company premises to prevent unauthorized access.
