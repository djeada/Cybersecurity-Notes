# Breached Passwords

Data breaches involving passwords are among the most significant security incidents, often leading to severe consequences for individuals and organizations. When passwords are leaked in a data breach, they can be exploited by attackers to gain unauthorized access to user accounts, perform credential stuffing, or compromise entire networks. Penetration testers frequently use breached password databases to assess the strength of user passwords and identify vulnerabilities in systems.

### Famous Data Breaches Involving Passwords

1. **LinkedIn (2012 and 2016):**
   - **Description:** LinkedIn suffered a massive data breach in 2012, initially reported to affect 6.5 million accounts. However, in 2016, it was revealed that the breach actually exposed over 117 million user accounts, including email addresses and hashed passwords.
   - **Impact:** The breach resulted in a significant number of LinkedIn passwords being cracked and sold on the dark web, leading to widespread credential stuffing attacks across multiple platforms.

2. **Yahoo (2013 and 2014):**
   - **Description:** Yahoo experienced two major data breaches affecting over 3 billion accounts. The breaches exposed email addresses, hashed passwords (many using the weak MD5 algorithm), and security questions.
   - **Impact:** These breaches led to one of the largest exposures of user credentials in history, significantly impacting user security across the internet.

3. **Facebook (2019):**
   - **Description:** In 2019, Facebook disclosed that millions of user passwords were stored in plaintext in internal logs, which were accessible to Facebook employees. Although there was no evidence of external breaches, the incident highlighted significant internal security lapses.
   - **Impact:** The incident raised concerns about the secure storage of passwords and led to Facebook implementing more robust security measures.

4. **Adobe (2013):**
   - **Description:** Adobe suffered a data breach that exposed the email addresses, usernames, and encrypted passwords of approximately 153 million users. The encryption was poorly implemented, making it relatively easy to decrypt many of the passwords.
   - **Impact:** The breach highlighted the importance of proper encryption practices and the risk of using weak or reused passwords.

5. **MySpace (2016):**
   - **Description:** In 2016, a breach from 2013 was discovered, affecting approximately 360 million MySpace accounts. The data included email addresses and weakly hashed passwords (using SHA1 without a salt).
   - **Impact:** Although MySpace was no longer a popular platform at the time, the breach emphasized the risks associated with legacy systems and weak password hashing methods.

### Resources for Accessing Breached Passwords

Penetration testers and security professionals often use various databases and tools to access breached passwords. These resources can help identify if passwords from a particular organization or individual have been compromised.

- **Snusbase (https://snusbase.com/):** Snusbase is a searchable database of breached data, including usernames, email addresses, passwords, and other sensitive information. It allows users to search for specific data across multiple breaches.
- **Leak-Lookup (https://leak-lookup.com/):** Leak-Lookup provides a service similar to Snusbase, offering access to a large database of breached credentials. Users can search for leaked passwords, email addresses, and other personal information.
- **DeHashed (https://dehashed.com/):** DeHashed is an extensive breach database and search engine that allows users to search for breached data, including passwords, emails, IP addresses, and more. It also offers API access for automated searches.
- **IntelX (https://intelx.io/signup):** IntelX (Intelligence X) is a platform that offers access to various data sources, including breached data, dark web content, and public records. It provides powerful search capabilities for investigators and security professionals.
- **Leakcheck (https://leakcheck.io/):** Leakcheck is a paid service that offers access to a vast database of leaked credentials. Users can search for specific email addresses or usernames to see if they have been compromised.

### Using Breached Passwords in Penetration Testing

1. **Credential Stuffing:**
   - **Description:** Attackers use breached username-password pairs to attempt logins on different services, exploiting users who reuse passwords across multiple sites.
   - **Tools:** Sentry MBA, Snipr, STORM.
   - **Penetration Testing Use:** Penetration testers can simulate credential stuffing attacks to evaluate how well an organization’s systems handle large-scale automated login attempts.

2. **Password Spraying:**
   - **Description:** In password spraying, attackers try common passwords across many accounts, rather than trying many passwords on a single account. This technique avoids account lockouts.
   - **Tools:** CrackMapExec, Hydra.
   - **Penetration Testing Use:** Password spraying tests can help determine the effectiveness of an organization’s account lockout policies and the strength of user passwords.

3. **Brute-Force Attacks:**
   - **Description:** Using automated tools to try many possible passwords in a short period to gain unauthorized access. While more time-consuming, brute-force attacks can be effective if passwords are weak.
   - **Tools:** Hydra, Hashcat, Medusa.
   - **Penetration Testing Use:** Brute-force testing can identify weak passwords and help organizations improve password policies and complexity requirements.

4. **Phishing Campaigns Using Breached Data:**
   - **Description:** Attackers use breached email addresses and other personal data to craft targeted phishing emails, tricking users into revealing their current passwords or other sensitive information.
   - **Tools:** SET (Social Engineering Toolkit), Gophish.
   - **Penetration Testing Use:** Phishing simulations using breached data can assess how well employees recognize and respond to phishing attempts.

### Best Practices for Handling Breached Passwords

1. Organizations should continuously monitor for breached passwords related to their employees and users. Tools like Have I Been Pwned or the resources mentioned above can help in this monitoring.
2. If an organization is affected by a data breach, it’s crucial to enforce immediate password changes for all affected accounts to reduce the risk of credential reuse.
3. Implement MFA across all accounts to provide an additional layer of security beyond just passwords. Even if a password is breached, MFA can prevent unauthorized access.
4. Regularly educate users about the risks of password reuse and the importance of using strong, unique passwords for different services.
5. Enforce policies that require users to create complex passwords that are difficult to crack and ensure that passwords are hashed using strong algorithms like bcrypt or Argon2.
