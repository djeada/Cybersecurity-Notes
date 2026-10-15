# Security Applications

### Personal Firewalls (Host-based Firewalls)
- **Windows Firewall:** Built-in firewall for Windows operating systems.
- **ZoneAlarm:** Third-party firewall solution for personal use.
- **Packet Filter and IP Firewall (Mac OSX):** Native firewall for macOS.
- **iptables (Linux):** Command-line firewall utility for Linux.

### Intrusion Detection Systems (IDS)
- **Host-Based IDS (HIDS):**
  - Installed on individual machines.
  - Monitors and analyzes the state of a single machine.
  - Can interpret encrypted traffic.
  
- **Network-Based IDS (NIDS):**
  - Deployed either on a dedicated device or as software on a machine.
  - Monitors all packets traversing the network interface.
  - Covers multiple devices, generally less costly.
  - Cannot monitor internal OS activities.

- **Monitoring Types:**
  - **Statistical Anomaly:** Establishes a baseline and compares current performance against it.
  - **Signature:** Analyzes network traffic to identify predetermined attack patterns.

- **HIDS Examples:**
  - **Trend Micro OSSEC:** Freeware HIDS solution.
  - **Verisys:** Commercial HIDS for Windows.
  - **Tripwire:** Commercial file integrity monitoring tool.

*Note:* Ensure that the HIDS database is secured with encryption and access control.

### Popup Blockers
- **Functions:** Filters advertisements and content to block unwanted popups.

### Data Loss Prevention (DLP)
- **Purpose:** Monitors and prevents unauthorized use and leakage of data at different stages:
  - **Data in Use**
  - **Data in Motion**
  - **Data at Rest**

- **Types of DLP:**
  - **Endpoint DLP:** Software-based, operates on a single machine.
  - **Network DLP:** Can be software or hardware-based, installed on the network perimeter.
  - **Storage DLP:** Deployed in data centers or server rooms.

---

## Securing Computer Hardware and Peripherals

### Examples of Peripherals
- **USB Flash Drives**
- **SATA External HDD**
- **Optical Disks**

### Securing BIOS
- **BIOS Security Measures:**
  - **Flashing BIOS Firmware:** Regularly update BIOS firmware.
  - **BIOS Password:** Set a strong password for BIOS access.
  - **Configure BIOS Boot Order:** Restrict unauthorized boot sources.
  - **Secure Boot:** Ensure that only signed device drivers are loaded.
  
  *Note:* UEFI, Root of Trust, secure/measured boot, and attestation enhance BIOS security.

### Securing Storage Devices
- **Removable Storage:**
  - **Policy:** Prohibit all removable storage devices except for those that are specifically allowed.
  - **Removable Media Controls:** Implement USB lockdown (via BIOS), restrict USB usage, and perform regular malware scans and audits.

- **NAS (Network Attached Storage):**
  - **Function:** Built for high availability, commonly implemented as a RAID array.
  - **Security Measures:** Use encryption, authentication, and secure logging.

- **Whole Disk Encryption:**
  - **Software:** Use self-encrypting drives or full disk encryption software.
  - **Windows BitLocker Requirements:**
    1. TPM (Trusted Platform Module) or an external USB key with encrypted keys.
    2. Hard drive with two volumes (one for boot, one for encryption).
  - **Double Encryption:** Combine BitLocker with EFS for enhanced security.

- **HSM (Hardware Security Modules):**
  - **Comparison to TPM:**
    - **TPM:** Handles key storage with limited cryptographic functions.
    - **HSM:** Focuses on fast cryptographic operations with key storage, available as USB attachments or network-attached devices.

### Securing Wireless Peripherals
- **Encryption:** Ensure that all wireless devices use AES or WPA2 for secure data transmission.

---

## Securing Mobile Devices

### General Security
- **Best Practices:**
  - Keep your phone number private and avoid responding to unsolicited calls.
  - Regularly update your mobile device’s OS.
  - Use complex passwords and limit downloads to trusted sources.

### Malware Protection
- **Steps:**
  - Install and update mobile antivirus software.
  - Utilize built-in security features.
  - Avoid clicking on suspicious links and refrain from storing sensitive information on your device.
  - Be cautious about posting personal information on social media.

### Botnet Activity
- **Prevention:** Follow standard anti-malware procedures and avoid rooting/jailbreaking your device.

### SIM Cloning
- **Threat:** Cloned SIM cards can redirect calls and texts, enabling attackers to hijack messages intended for the original SIM owner.

### Wireless Attacks
- **Common Attacks:**
  - **Bluejacking:** Sending unsolicited messages via Bluetooth.
  - **Bluesnarfing:** Unauthorized access to information from Bluetooth-enabled devices.

### Theft Prevention
- **Measures:**
  - Use full device encryption (FDE).
  - Enable GPS tracking on your device.
  - Implement remote lock and remote wipe features.

### Mobile Application Security
- **Best Practices:**
  - Use third-party software for mobile key management (e.g., Verisign).
  - Implement application whitelisting/blacklisting.
  - Secure SMS applications and endpoints.
  - Avoid using public networks for mobile payments and educate users on best practices.
  - **Geotagging:** Disable GPS when not necessary.

### BYOD Concerns
- **Strategies:**
  - **Storage Segmentation:** Separate corporate data from personal data.
  - **Mobile Device Management (MDM):** Implement MDM systems to manage corporate devices.
