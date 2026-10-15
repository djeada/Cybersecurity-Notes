# VPN (Virtual Private Network)

A Virtual Private Network (VPN) creates a protected tunnel between endpoints,
such as a device and an organizational gateway or two private networks. A
consumer VPN can change the public source IP seen by destinations. It does not
guarantee anonymity, hide logged-in identities, or secure a compromised endpoint.

### Key Functions of a VPN

1. **Anonymizing IP Address:**
   - **Description:** For traffic routed through the tunnel, destinations generally
     see the VPN exit's source address. Accounts, cookies, fingerprints, and other
     metadata can still identify the user.
   - **Consideration:** Trust shifts toward the VPN operator. Check which traffic,
     DNS requests, and IPv6 routes are actually included in the tunnel.

2. **Encrypting Data Traffic:**
   - **Description:** VPNs encrypt data traffic between the user's device and the VPN server, making it unreadable to anyone who intercepts it. This is particularly important when using public Wi-Fi networks.
   - **Encryption Protocols:** Common protocols include OpenVPN, WireGuard, and IPsec. These protocols ensure secure communication by encrypting data packets.

3. **Bypassing Geo-Restrictions:**
   - **Description:** VPNs can be used to bypass geographical restrictions on content by making it appear as though the user is accessing the internet from a different location.
   - **Example:** Accessing streaming services or websites that are restricted to certain regions.

4. **Improving Online Privacy:**
   - **Description:** By masking the user's IP address and encrypting their internet traffic, VPNs enhance online privacy, reducing the risk of being tracked by advertisers, ISPs, or malicious actors.

### Common VPN Vulnerabilities and Concerns

1. **Trust in the VPN Provider:**
   - **Description:** The operator can observe connection metadata and any
     unencrypted traffic leaving the tunnel. End-to-end HTTPS still protects its
     encrypted application content from the VPN operator.
   - **Mitigation:** Assess operational practices, independent evidence, and the
     trust model. Open client source code or a no-logs claim alone does not prove
     how the service is operated.

2. **VPN Server Compromise:**
   - **Description:** A compromised gateway can expose tunnel traffic and metadata;
     it does not automatically decrypt independently protected HTTPS content.
   - **Mitigation:** Regularly update server software, use secure VPN protocols, and employ multi-factor authentication for server access.

3. **DNS Leaks:**
   - **Description:** A DNS leak occurs when a VPN fails to hide your DNS requests, exposing them to your ISP or other unauthorized parties. This can undermine the privacy the VPN is supposed to provide.
   - **Mitigation:** Use VPNs with built-in DNS leak protection and periodically test for DNS leaks using online tools.

4. **Weak Encryption Protocols:**
   - **Description:** Some VPNs may use outdated or weak encryption protocols, making it easier for attackers to decrypt the data.
   - **Mitigation:** Use VPNs that support strong encryption protocols like OpenVPN, WireGuard, or IPsec with AES-256 encryption.

5. **Connection Stability and Kill Switch:**
   - **Description:** If a VPN connection drops, the user's real IP address may be exposed. A kill switch prevents this by automatically blocking internet traffic until the VPN connection is restored.
   - **Mitigation:** Ensure your VPN has a reliable kill switch feature and consider testing it to ensure it functions correctly.

6. **Poor Logging Policies:**
   - **Description:** Some VPN providers may log user activity, which could be accessed by law enforcement or other entities. This logging undermines the privacy protection that VPNs are supposed to provide.
   - **Mitigation:** Evaluate retention, access controls, transparency, and available
     evidence rather than treating a marketing claim as a technical guarantee.

### Best Practices for Secure VPN Usage

1. **Choose a Reputable VPN Provider:**
   - **Description:** Select a maintained implementation and an operator whose
     access controls, update process, and data practices fit the threat model.
   - **Consideration:** Ensure the provider operates in a jurisdiction with strong privacy laws and is not subject to intrusive government surveillance.

2. **Use Strong Encryption Protocols:**
   - **Description:** Use a maintained protocol and its supported secure configuration.
     WireGuard uses ChaCha20-Poly1305, not AES-256. OpenVPN and IPsec have their own
     configurable algorithms and authentication requirements.
   - **Impact:** Strong encryption protects your data from being intercepted or decrypted by unauthorized parties.

3. **Enable Kill Switch:**
   - **Description:** Where the threat model requires traffic to stay within the
     tunnel, enable and test traffic-blocking behavior during disconnects,
     including DNS and IPv6. It is not a guarantee of anonymity.
   - **Impact:** Prevents accidental exposure of your real IP address and unencrypted data.

4. **Regularly Update VPN Software:**
   - **Description:** Keep your VPN client and server software up to date to protect against newly discovered vulnerabilities and exploits.
   - **Impact:** Ensures that your VPN setup is secure and benefits from the latest security patches and improvements.

5. **Test for DNS Leaks:**
   - **Description:** Regularly test your VPN for DNS leaks to ensure that your DNS requests are being routed securely through the VPN tunnel.
   - **Tools:** Use online tools like DNSLeakTest.com or similar to check for leaks.
   - **Impact:** Protects against inadvertent exposure of browsing activity to your ISP or other entities.

6. **Avoid Free VPN Services:**
   - **Description:** Free VPN services often come with significant security and privacy trade-offs, such as logging user activity or injecting ads into your browsing.
   - **Impact:** Paid VPN services, especially those with a strong privacy reputation, are generally more reliable and secure.

### Penetration Testing of VPNs

1. **Assessment of Encryption Protocols:**
   - **Objective:** Evaluate the strength of the encryption protocols used by the VPN. This includes verifying the implementation of secure encryption standards like AES-256 and assessing the vulnerability of the VPN to known attacks (e.g., BEAST, Heartbleed).
   - **Tools:** Wireshark, OpenVPN audit tools, WireGuard security analysis.

2. **Testing for DNS Leaks:**
   - **Objective:** Ensure that all DNS requests are routed through the VPN tunnel and not leaking to external servers.
   - **Tools:** DNSLeakTest.com, tcpdump, Wireshark.

3. **Kill Switch Functionality Testing:**
   - **Objective:** Test the reliability of the VPN’s kill switch feature to ensure it activates in the event of a dropped connection, preventing data leaks.
   - **Method:** Simulate a dropped VPN connection and observe whether internet traffic is blocked until the VPN reconnects.

4. **Evaluation of Logging Practices:**
   - **Objective:** Verify the VPN provider’s claim of not logging user activity by analyzing the VPN’s logging and data storage practices.
   - **Method:** Review the VPN provider’s privacy policy, conduct a thorough analysis of logs generated during VPN use, and inspect server configurations.

5. **Server Compromise Simulation:**
   - **Objective:** Assess the impact of a potential VPN server compromise by simulating an attack on the server and analyzing the ability to intercept or decrypt traffic.
   - **Tools:** Penetration testing tools like Metasploit, nmap, and OpenVAS.

6. **Credential Security:**
   - **Objective:** Test the strength of authentication mechanisms used by the VPN, including the security of stored credentials and the implementation of multi-factor authentication (MFA).
   - **Tools:** Hydra, John the Ripper for password cracking; Burp Suite for web-based authentication testing.

## Sources

- [WireGuard protocol and cryptography](https://www.wireguard.com/protocol/)
- [NIST SP 800-77 Rev. 1: IPsec VPNs](https://csrc.nist.gov/pubs/sp/800/77/r1/final)
