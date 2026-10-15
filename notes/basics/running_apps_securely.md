# Securing Other Applications

### Principle of Least Functionality
- **Concept:** Only provide users with the tools they need for their job functions, reducing unnecessary risk.

### User Account Control (Windows)
- **Function:** Keeps users at a regular user level of access by default, requiring prompts for actions needing administrative rights.

### Create Policies
- **Policy Approach:** Prioritize application whitelisting over blacklisting to restrict users to only necessary applications.

### Securing Common Windows Programs
1. **Outlook:**
   - Keep Outlook updated and consider upgrading to newer Office versions.
   - Implement email whitelisting to filter out junk mail.
   - Configure Outlook to read emails in text format rather than HTML.
   - Enable attachment blocking for security.
   - Use encryption methods like SPA (Secure Password Authentication), PGP, or SSL for secure communication.

2. **Word:**
   - Use passwords to protect document opening/modification.
   - Set documents to read-only to prevent unauthorized changes.
   - Employ digital certificates for document authenticity.

3. **Excel:**
   - Protect worksheets with passwords and avoid using macros.
   - Utilize Excel’s encryption features to secure sensitive data.

### Mobile Applications
- **Security Measures:**
   - Disable GPS when not needed.
   - Use strong passwords for accessing mobile applications.

### Server Applications
- **Examples:** FTP, Email, Web, SQL Database.
- **Best Practices:**
   - Change default usernames and passwords immediately after installation.
   - Avoid consolidating multiple services onto a single server to reduce risk.
