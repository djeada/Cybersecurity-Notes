# Hashcat

**Hashcat** is a popular and powerful password-cracking tool used in cybersecurity, penetration testing, and ethical hacking. It is designed to recover passwords from hashes, which are fixed-length representations of data that have been processed through a cryptographic hash function. Hashes are commonly used to store passwords securely, but if a weak or compromised hash is found, tools like Hashcat can be used to attempt to recover the original plaintext password.

### Key Features and Purposes of Hashcat:

1. **Password Recovery**:
   - The primary purpose of Hashcat is to recover plaintext passwords from hashed passwords. This is often done as part of a penetration test, security audit, or forensic investigation.
   - Hashcat supports a wide variety of hash algorithms, including MD5, SHA1, SHA256, bcrypt, NTLM, and many others.

2. **High Performance**:
   - Hashcat is designed to be extremely efficient and fast, leveraging the power of modern CPUs and GPUs (Graphics Processing Units). GPU-based cracking is significantly faster than CPU-based cracking, especially for complex passwords and strong hashing algorithms.

3. **Flexibility**:
   - Hashcat supports many attack modes, including:
     - **Brute-Force Attack**: Trying all possible combinations of characters until the correct one is found.
     - **Dictionary Attack**: Using a precompiled list of possible passwords (a dictionary) and hashing each one to see if it matches the target hash.
     - **Combination Attack**: Combining words from multiple dictionaries.
     - **Rule-Based Attack**: Applying specific rules to modify words in a dictionary (e.g., adding numbers or changing case).
     - **Hybrid Attack**: Combining dictionary and brute-force attacks.
     - **Mask Attack**: Brute-forcing with a mask that defines character sets for each position (useful for targeting passwords with a known structure).

4. **Security Audits and Penetration Testing**:
   - Security professionals use Hashcat to audit password security within an organization. By attempting to crack passwords, they can identify weak passwords and enforce stronger password policies.

5. **Password Strength Evaluation**:
   - By running a password hash through Hashcat, security teams can assess how easily a given password could be cracked. This helps in understanding the effectiveness of existing password policies.

6. **Digital Forensics**:
   - In digital forensics, Hashcat can be used to recover passwords from hashed data found in seized digital evidence, which may help investigators access locked files or accounts.

7. **Learning and Education**:
   - Hashcat is also a valuable tool for learning about cryptography, password security, and the importance of strong, complex passwords.

### Typical Workflow:
1. **Obtain Hashes**: Hashcat requires hashes to crack. These can be extracted from various sources, like databases, password dumps, or captured traffic.
2. **Choose Attack Mode**: Depending on the situation, select an appropriate attack mode (e.g., brute-force, dictionary).
3. **Run Hashcat**: Execute Hashcat with the desired parameters and let it run until it finds a match or exhausts the possibilities.
4. **Analyze Results**: Review the cracked passwords and take necessary actions, such as improving security or continuing an investigation.

### **Likely Full Command Used for Hashcat:**

While the screenshot doesn’t show the full `hashcat` command, a typical command that might have been used could look something like this:

```bash
./hashcat.bin -m 3200 hashes/usage.bcrypt -a 0 /path/to/wordlist.txt
```

### **Explanation of the Command:**
- **./hashcat.bin**: Executes the `hashcat` binary.
- **-m 3200**: Specifies the hash type. `3200` is the hash mode for bcrypt.
- **hashes/usage.bcrypt**: Specifies the input file containing the bcrypt hashes.
- **-a 0**: Specifies the attack mode. `0` is for a dictionary attack, where `hashcat` uses a wordlist to compare against the hash.
- **/path/to/wordlist.txt**: The wordlist file used for the attack. `hashcat` will hash each entry in this wordlist and compare it to the hash in `usage.bcrypt` to find matches.

### **Input:**
- The `usage.bcrypt` file containing bcrypt-hashed passwords.
- The wordlist used by `hashcat` for the attack (if using a dictionary attack).

### **Output:**
- The cracked passwords, if `hashcat` successfully finds matches for the bcrypt hashes in the wordlist. The output is usually displayed in the terminal and can be saved to a file.
