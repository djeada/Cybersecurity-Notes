# Wi-Fi Security

Wi-Fi networks are ubiquitous, providing wireless internet access to homes, businesses, and public spaces. However, the convenience of Wi-Fi comes with significant security risks, as wireless signals can be intercepted by anyone within range. Securing Wi-Fi networks is essential to prevent unauthorized access, data theft, and other malicious activities. Penetration testers focus on identifying vulnerabilities in Wi-Fi security to help organizations protect their networks from attackers.

### Common Wi-Fi Security Protocols

1. **WEP (Wired Equivalent Privacy):**
   - **Description:** An outdated and insecure protocol that uses RC4 encryption. WEP is easily cracked due to its use of weak initialization vectors (IVs).
   - **Vulnerabilities:** Susceptible to IV collision attacks and replay attacks, making it highly insecure.
   - **Recommendation:** WEP should no longer be used. Networks still using WEP should be upgraded to more secure protocols.

2. **WPA (Wi-Fi Protected Access):**
   - **Description:** An improvement over WEP, WPA uses TKIP (Temporal Key Integrity Protocol) for encryption. However, it still has vulnerabilities, particularly in its implementation.
   - **Vulnerabilities:** Vulnerable to attacks like the TKIP MIC (Message Integrity Check) attack.
   - **Recommendation:** WPA is considered obsolete and should be replaced with WPA2 or WPA3.

3. **WPA2 (Wi-Fi Protected Access II):**
   - **Description:** The most widely used Wi-Fi security protocol, WPA2 uses AES (Advanced Encryption Standard) for strong encryption. It offers a significant security improvement over WEP and WPA.
   - **Vulnerabilities:** WPA2 is susceptible to attacks like the KRACK (Key Reinstallation Attack) and dictionary/brute-force attacks on captured handshakes.
   - **Recommendation:** WPA2 with AES is generally secure but should be configured with a strong password. Consider upgrading to WPA3 where possible.

4. **WPA3:**
   - **Description:** The latest Wi-Fi security protocol, WPA3, introduces features like Simultaneous Authentication of Equals (SAE) to protect against dictionary attacks and provides stronger encryption.
   - **Vulnerabilities:** WPA3 is more secure than its predecessors, but early implementations have shown some vulnerabilities that need addressing.
   - **Recommendation:** WPA3 is recommended for new networks as it offers the highest level of security currently available.

### Common Wi-Fi Attacks and Exploits

1. **Leaked Passwords:**
   - **Description:** Attackers use publicly available databases and apps like Wi-Fi Map or Instabridge to find leaked Wi-Fi passwords. This is particularly effective against networks where users have shared passwords online.
   - **Mitigation:** Regularly change Wi-Fi passwords and avoid using easily guessable or commonly used passwords.

2. **Pixie Dust Attack (WPS Only):**
   - **Description:** A vulnerability in WPS (Wi-Fi Protected Setup) that allows attackers to brute-force the WPS PIN offline. This is particularly effective against certain implementations of WPS.
   - **Tools:** Pixiewps.
   - **Mitigation:** Disable WPS on your router, as it is a known weak point in Wi-Fi security.

3. **WPS PIN Brute Force (Reaver/Bully):**
   - **Description:** Attackers use tools like Reaver or Bully to brute-force the WPS PIN of a router, potentially gaining access to the Wi-Fi network.
   - **Tools:** Reaver, Bully.
   - **Mitigation:** Disable WPS on your router to prevent brute-force attacks on the WPS PIN.

4. **Dictionary/Brute-Force Attack on Captured PMKID:**
   - **Description:** Attackers capture the PMKID (Pairwise Master Key Identifier) from a WPA/WPA2 handshake and perform a dictionary or brute-force attack to recover the password.
   - **Tools:** Hashcat, hcxdumptool.
   - **Mitigation:** Use a strong, complex Wi-Fi password that is resistant to dictionary and brute-force attacks.

5. **Dictionary/Brute-Force Attack on Captured Handshake:**
   - **Description:** Attackers capture the 4-way handshake during the connection process of a WPA/WPA2 network and attempt to crack the password using a dictionary or brute-force attack.
   - **Tools:** Aircrack-ng, Hashcat.
   - **Mitigation:** Ensure that the Wi-Fi password is strong and not easily guessable. Implementing WPA3 can also mitigate this attack.

6. **Evil Twin Attack:**
   - **Description:** Attackers create a rogue Wi-Fi access point that mimics a legitimate network, tricking users into connecting to it. Once connected, attackers can intercept or manipulate the victim’s traffic.
   - **Tools:** Airgeddon, Fluxion.
   - **Mitigation:** Educate users to avoid connecting to unfamiliar Wi-Fi networks. Use secure protocols like HTTPS and VPNs to protect data transmission even on potentially compromised networks.

### Tools Used in Wi-Fi Penetration Testing

1. **Aircrack-ng Suite:**
   - **Description:** A comprehensive suite of tools for assessing Wi-Fi network security. It includes tools for monitoring, capturing packets, and performing brute-force attacks on captured handshakes.
   - **Key Components:**
     - **Airodump-ng:** For capturing packets.
     - **Aireplay-ng:** For injecting packets to generate handshakes.
     - **Aircrack-ng:** For cracking WEP and WPA-PSK passwords.

2. **Reaver:**
   - **Description:** A tool used to brute-force the WPS PIN on routers to recover WPA/WPA2 passphrases.
   - **Use Case:** Particularly effective against routers with WPS enabled and vulnerable to brute-force attacks.

3. **Hashcat:**
   - **Description:** A powerful password recovery tool that supports the cracking of Wi-Fi passwords through dictionary and brute-force attacks on captured handshakes or PMKIDs.
   - **Use Case:** Cracking WPA/WPA2 passwords, especially large wordlists or complex passwords.

4. **Wireshark:**
   - **Description:** A network protocol analyzer that can capture and analyze traffic on a Wi-Fi network. It’s often used to inspect captured packets during a penetration test.
   - **Use Case:** Analyzing captured handshakes or traffic for sensitive data.

5. **Pixiewps:**
   - **Description:** A tool for performing Pixie Dust attacks on WPS-enabled routers. It exploits vulnerabilities in WPS to recover the PIN and, consequently, the Wi-Fi password.
   - **Use Case:** Attacking vulnerable WPS implementations to gain access to Wi-Fi networks.

6. **Fluxion:**
   - **Description:** An Evil Twin attack tool that automates the process of setting up a rogue access point, intercepting traffic, and capturing credentials.
   - **Use Case:** Conducting social engineering attacks by tricking users into connecting to a fake Wi-Fi network.

### Best Practices for Securing Wi-Fi Networks

1. **Use Strong Encryption (WPA2/WPA3):**
   - **Description:** Always use WPA2 with AES encryption or, preferably, WPA3 for the highest level of security. Avoid using outdated protocols like WEP or WPA.
   - **Impact:** Strong encryption protocols make it significantly more difficult for attackers to crack Wi-Fi passwords.

2. **Disable WPS:**
   - **Description:** Wi-Fi Protected Setup (WPS) is a known vulnerability and should be disabled to prevent attacks like Pixie Dust and brute-force WPS PIN attacks.
   - **Impact:** Disabling WPS removes a significant weak point in Wi-Fi security.

3. **Use Strong, Complex Passwords:**
   - **Description:** Use a long, complex Wi-Fi password that is resistant to dictionary and brute-force attacks. Avoid using common phrases or easily guessable patterns.
   - **Impact:** Strong passwords reduce the likelihood of successful brute-force or dictionary attacks.

4. **Enable Network Segmentation:**
   - **Description:** Segment your Wi-Fi network into different VLANs or SSIDs for different user groups (e.g., guest network vs. internal network) to limit access and exposure.
   - **Impact:** Network segmentation minimizes the risk of lateral movement by attackers within the network.

5. **Monitor for Rogue Access Points:**
   - **Description:** Regularly scan for unauthorized (rogue) access points that may have been set up by attackers to conduct Evil Twin or other types of attacks.
   - **Tools:** Tools like AirMagnet or Kismet can help detect rogue access points.
   - **Impact:** Detecting and disabling rogue access points prevents attackers from intercepting network traffic.

6. **Keep Firmware Updated:**
   - **Description:** Regularly update your router’s firmware to patch any known vulnerabilities and ensure that the latest security features are in place.
   - **Impact:** Firmware updates protect against newly discovered vulnerabilities that could be exploited by attackers.
