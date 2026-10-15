# Cracking Windows Hashes

Gaining access to authentication hashes on a Windows system can be a crucial step in penetration testing or red team activities. These hashes, particularly the **NTHash** or **NTLM** format, are used by modern Windows operating systems to store user and service passwords.

### NTLM Overview

- **NT password hash:** MD4 over the UTF-16LE password, without a per-password salt.
  It is often called an NTLM hash, but the stored hash is distinct from an NTLM
  challenge-response exchange. NTLM is an authentication protocol family.

### Acquiring NTLM Hashes

To crack NTLM hashes, you first need to obtain them, typically requiring elevated privileges on a Windows system. These hashes are stored in either the **Security Account Manager (SAM)** database on individual Windows machines or the **NTDS.dit** database within a domain environment.

#### Common Methods to Obtain NTLM Hashes:

1. **Dumping the SAM Database:**
   - **SAM (Security Account Manager):** Stores user passwords in a hashed format on Windows machines.
   - **Tools:** 
     - **Mimikatz:** A popular tool for extracting passwords and hashes.
     - **Metasploit's `hashdump` module:** Used within the Metasploit framework to dump SAM hashes.
     - **samdump2:** A tool that extracts SAM hashes from a Windows system.

2. **Extracting from NTDS.dit:**
   - **NTDS.dit:** The Active Directory database file that stores all information, including user credentials, within a domain environment.
   - **Tools:**
     - **ntdsutil:** A native Windows tool for interacting with the NTDS.dit file.
     - **secretsdump.py (Impacket):** A Python tool used for extracting hashes from NTDS.dit.
     - **Mimikatz (`lsadump::dcsync` command):** Allows for dumping credentials from NTDS.dit by simulating the behavior of a domain controller.

### Cracking NTLM Hashes

In an authorized lab, NT password hashes can be audited with John the Ripper or
Hashcat. They are fast, unsalted password hashes and are not a robust modern
password-storage design. Weak passwords are especially susceptible to guessing.

#### Example of Using John the Ripper:
```bash
john --format=NT --wordlist=/path/to/wordlist.txt ntlm_hashes.txt
```
- **Explanation:** This command instructs John the Ripper to use the NTLM hash format and a specified wordlist to attempt to crack the hashes.

### Pass-the-Hash Attacks

In some scenarios, cracking the hash may not be necessary. **Pass-the-Hash (PtH)** is a technique where an attacker uses the NTLM hash of a user's password instead of the plaintext password to authenticate to a network service. This method is particularly effective in Windows environments, allowing attackers to move laterally across a network without needing the actual passwords.

### Defensive Measures

1. **Enforce Strong Password Policies:**
   - **Purpose:** Use long, unique passwords and compromised-password screening;
     change exposed passwords and revoke affected sessions rather than relying
     on arbitrary periodic resets.

2. **Enable SMB Signing:**
   - **Purpose:** Require SMB signing where supported to protect SMB integrity and
     mitigate relevant relay attacks. It does not prevent credential extraction
     from an already compromised endpoint or every pass-the-hash scenario.

3. **Use Multi-Factor Authentication (MFA):**
   - **Purpose:** Apply MFA where the authentication flow supports it. Do not assume
     MFA on an interactive login also protects every legacy NTLM service. Reduce
     NTLM use, restrict administrative privileges, and avoid reused local-admin passwords.

## Sources

- [Microsoft NTLM overview](https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview)
- [Microsoft SMB signing overview](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview)
