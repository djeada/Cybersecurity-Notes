# Secure Programming

### SDLC (Software Development Life Cycle)
1. **Waterfall:**
   - Traditional development method where requirements are defined before development begins.
   
2. **Agile:**
   - Rapid Application Development (RAD) approach that breaks down development into incremental changes.
   - Requires high dedication and frequent communication among team members.

3. **DevOps:**
   - A deployment tool often used alongside Agile methodologies to streamline development and operations.

### Core SDLC and DevOps Principles
1. **Preserving CIA:**
   - Ensure the Confidentiality, Integrity, and Availability of software throughout its development lifecycle.

2. **Secure Code Review:**
   - Conduct in-depth reviews to identify security bugs before moving to fuzzing or penetration testing.

3. **Threat Modeling:**
   - Identify and prioritize potential threats to software during the design phase.

### Common Security Principles
1. **Least Privilege:**
   - Ensure users and processes operate with the minimum privileges necessary.
   
2. **Defense in Depth:**
   - Implement multiple layers of security to protect against threats.

3. **Never Trust User Input:**
   - Validate all user inputs to prevent injection attacks.

4. **Minimizing Attack Surface:**
   - Reduce the number of entry points for attackers.

5. **Secure Defaults:**
   - Configure software with security settings enabled by default.

6. **Authenticity and Integrity:**
   - Use program signatures and verification methods to ensure software authenticity.

7. **Fail Securely:**
   - Design systems to handle errors securely, avoiding unintended information disclosure.

8. **Thorough Testing:**
   - Regularly test security fixes and patches to ensure they do not introduce new vulnerabilities.

---

## Program Testing Methods

1. **White Box vs Black Box Testing:**
   - **White Box:** Internal testing with knowledge of the code.
   - **Black Box:** External testing with no prior knowledge of the code.
   - **Gray Box:** A mix of both white box and black box testing.
   - **Stress Testing:** Evaluates system performance under extreme conditions.
   - **Penetration Testing:** Simulates an attack on the system to find vulnerabilities.

2. **Compile-Time vs Runtime Errors:**
   - **Compile-Time:** Errors detected during the compilation process.
   - **Runtime:** Errors occurring during program execution.
   - **Structured Exception Handling (SHE):** A method for handling both software and hardware errors.

3. **Input Validation:**
   - **Importance:** Crucial for preventing SQL injections and cross-site scripting (XSS) attacks.
   - **Best Practices:** Perform validation on both client and server sides.

4. **Static vs Dynamic Code Analysis:**
   - **Static:** Analyzes code without executing it, often using automated tools.
   - **Dynamic:** Examines code behavior during execution to identify bugs.

5. **Fuzz Testing:**
   - **Method:** Inputs large amounts of random data to uncover code errors and vulnerabilities.

---

## Program Vulnerability and Attacks

1. **Backdoors:**
   - **Definition:** Preprogrammed authentication bypasses built into a system.
   - **Prevention:** Updates, job rotation, and code cross-checking can help remove or prevent backdoors.

2. **Memory/Buffer Vulnerabilities:**
   - **Types:** Buffer overflows (stack, heap), integer overflows, memory leaks, null pointer dereference.
   - **Defense:** Address Space Layout Randomization (ASLR) and Data Execution Prevention (DEP) are common defenses.

3. **Arbitrary and Remote Code Execution:**
   - **Threat:** Attackers can execute arbitrary code or commands on a target system.
   - **Defense:** Strong input validation and fuzz testing are critical defenses.

4. **XSS/XSRF:**
   - **Threat:** Browser-based attacks that exploit code injection vulnerabilities in HTML.
   - **Prevention:** Implement strict content security policies and input validation.

5. **Other Code Injections:**
   - **Types:** SQL Injection, LDAP Injection, XML Injection.
   - **Prevention:** Sanitize and validate all inputs to prevent these attacks.

6. **Directory Traversal:**
   - **Threat:** Attackers gain unauthorized access to files outside the web root directory.
   - **Prevention:** Restrict file access permissions and validate user inputs.

7. **Zero-Day Attacks:**
   - **Definition:** Attacks exploiting unknown vulnerabilities before they can be patched.
   - **Defense:** Regularly update and patch systems, and employ behavior-based detection systems.
