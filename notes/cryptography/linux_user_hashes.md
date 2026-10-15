# Cracking Hashes from `/etc/shadow`

### Overview

- **Purpose:** In Linux, the `/etc/shadow` file securely stores hashed passwords along with metadata like password expiration and last change dates. Due to the sensitive nature of this file, it is accessible only to the root user. If an attacker gains access to this file, they may attempt to crack the hashed passwords to gain unauthorized access to user accounts.

### Understanding `/etc/shadow`

- **Content:** The `/etc/shadow` file contains entries for each user, typically including the username, hashed password, and fields related to password policies.
- **Format Example:**
  ```
  username:$6$randomsalt$hashedpassword:18000:0:99999:7:::
  ```
  - `username`: The user's login name.
  - `$6$`: Indicates the hashing algorithm used (in this case, SHA-512).
  - `randomsalt`: A random string used as a salt to make the hash more secure.
  - `hashedpassword`: The result of the password and salt being hashed together.

### Preparing for Hash Cracking

#### Unshadowing

- **Purpose:** The `/etc/passwd` file contains user account information, while `/etc/shadow` holds the hashed passwords. To crack the hashes, you must combine these two files into a format that password cracking tools like John the Ripper can process.
  
- **Steps:**
  1. **Extract relevant lines** from `/etc/passwd` and `/etc/shadow` if you’re targeting specific users.
  2. **Use the `unshadow` tool** to combine these files into a single file.
  
  **Example Command:**
  ```bash
  unshadow /etc/passwd /etc/shadow > unshadowed.txt
  ```
  This command creates a file named `unshadowed.txt` that contains the necessary information for cracking.

#### Cracking the Hashes

- **Tools:** Popular tools for cracking password hashes include John the Ripper and Hashcat. These tools use techniques like dictionary attacks, brute-force attacks, and rainbow tables to attempt to recover the original passwords from the hashes.

- **Basic Cracking Process:**
  1. **Select a wordlist:** Use a predefined wordlist (e.g., `rockyou.txt`) containing common passwords.
  2. **Specify the hash format:** Depending on the hash type, specify the correct format. For example, SHA-512 hashes from `/etc/shadow` would use `sha512crypt`.

  **Example Command with John the Ripper:**
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt --format=sha512crypt unshadowed.txt
  ```
  This command attempts to crack the hashes using the `rockyou.txt` wordlist.

### Important Considerations

- **Hash Formats:** Different hashing algorithms are indicated by specific prefixes in the `/etc/shadow` file:
  - `$1$` = MD5-crypt (legacy)
  - `$5$` = SHA-256-crypt
  - `$6$` = SHA-512-crypt
  - `$y$` = yescrypt, used by some current distributions

  These are password-hashing schemes, not plain hashes of the password. Defaults
  vary by distribution and configuration; inspect the prefix rather than assuming
  SHA-512-crypt. Locked or disabled password fields may contain `!` or `*` rather
  than a usable hash. Protect exports of `/etc/shadow` as sensitive credentials.

- **Security Implications:** Successfully cracking a password hash can give an attacker unauthorized access to the associated user account. It highlights the importance of using strong passwords, implementing salting, and regularly auditing system security.

- **Mitigations:** To protect against hash cracking:
  - Use strong, unique passwords.
  - Implement multifactor authentication (MFA).
  - Regularly update and audit access controls to sensitive files like `/etc/shadow`.

### Example Scenario

- **Scenario:** An attacker gains root access to a Linux system and retrieves the `/etc/shadow` file. They combine it with `/etc/passwd` using the `unshadow` tool and then attempt to crack the hashes with John the Ripper, using a popular wordlist.
  
- **Outcome:** If the attacker successfully cracks one or more passwords, they could use this information to further compromise the system.
