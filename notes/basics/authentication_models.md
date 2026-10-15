# Physical Security and Authentication Models

### Key Concepts

- **Identification:** Something that identifies a person.
- **Authentication:** The process of confirming or verifying a person's identity.
- **Authorization:** Granting a user permission to access certain materials; occurs after authentication.

---

## Physical Security

Effective physical security measures are crucial to protect organizational assets and data. The following are key components:

### 1. Perimeter Security

- Ensure ample lighting to deter unauthorized access.
- Eliminate hidden corners and blind spots.
- Implement surveillance systems such as CCTV cameras.
- Employ security personnel or guards for monitoring.

### 2. Server Room Security

- **Location:** Position server rooms on elevated levels to avoid water damage.
- **Protection Measures:**
  - Use secure cabling methods to prevent tampering.
  - Install physical locks on server racks and entry points.
  - Control and monitor access strictly.

### 3. Door Access Control

- **Assessment:** Implement access controls based on local crime rates and the sensitivity of data within the facility.
- **Access Methods:**
  - Utilize electronic keycards and cardkey controllers.
  - Employ hardware-based tokens and One-Time Password (OTP) generators for added security.
  - Use smart cards for authentication purposes.
    - Examples include:
      - **PIV (Personal Identity Verification):** Used by government employees.
      - **CAC (Common Access Card):** Used by Department of Defense (DoD) and military personnel.
- **Additional Measures:**
  - Implement mantraps to prevent tailgating and unauthorized entry.

### 4. Biometrics

- **Considerations:**
  - Monitor and minimize **False Acceptance Rates (FAR)** and **False Rejection Rates (FRR)**.
  - Aim for a low **Crossover Error Rate (CER):** The point where FAR equals FRR, indicating optimal biometric system performance.

---

## Authentication Models and Components

Understanding various authentication models and technologies is essential for securing access to systems and data.

### 1. Authentication Models

#### a) Username/Password

- The most basic form of authentication requiring users to provide a valid username and corresponding password.

#### b) Multifactor Authentication (MFA)

- Enhances security by requiring two or more verification methods from independent categories:
  - **Something you know:** Password or PIN.
  - **Something you have:** Smart card or token.
  - **Something you are:** Biometrics like fingerprint or retina scan.
- Prefer phishing-resistant MFA such as appropriately configured FIDO2/WebAuthn
  authenticators. Password plus PIN is still one factor; SMS and one-time codes
  are susceptible to phishing. Protect recovery and enrollment as carefully as login.

#### c) Context-Aware Authentication

- Grants access based on the context of the user’s request, such as location, time, and device used.
- Dynamically adjusts security requirements based on risk assessment.

#### d) Single Sign-On (SSO)

- Allows users to authenticate once and gain access to multiple systems without re-entering credentials.
- Simplifies user experience and reduces password fatigue.

#### e) Federated Identity Management

- Extends SSO across multiple organizations or domains.
- Enables trusted identity sharing between disparate systems.

#### f) Web-Based SSO

- Provides SSO capabilities specifically for web applications and services.
- Common protocols include SAML and OpenID Connect (OIDC). OAuth 2.0 provides
  delegated authorization; OIDC adds an authentication and identity layer.

---

### 2. Localized Authentication Technologies

Methods used to authenticate users connecting to a Local Area Network (LAN).

#### a) 802.1X and EAP (Extensible Authentication Protocol)

- **Purpose:** Ensures port-based network access control, operating at the Data Link Layer.
- **Authentication Process:**
  1. **Initialization:** The authenticator detects a new client and initiates the 802.1X process.
  2. **EAP Request/Response:** The authenticator sends EAP requests; the client responds with EAP responses forwarded to the authentication server.
  3. **EAP Method Selection:** The authentication server requests a specific EAP method, which is communicated to the client.
  4. **Authentication Exchange:** EAP requests and responses are exchanged until authentication is successful.
- **Types of EAP Methods:**
  - **EAP-MD5:** Uses MD5 hashing; considered insecure.
  - **EAP-TLS:** Employs Transport Layer Security; provides strong security using certificates.
  - **EAP-TTLS:** Tunneled TLS; allows legacy password-based authentication within a secure tunnel.
  - **EAP-FAST:** Flexible Authentication via Secure Tunneling; developed by Cisco.
  - **PEAP (Protected EAP):** Encapsulates EAP within a TLS tunnel.
- **Usage:** 802.1X is often combined with VLANs for enhanced port-layer security.

#### b) LDAP (Lightweight Directory Access Protocol)

- **Function:** Accesses and maintains distributed directory information services.
- **Common Use:** Widely used in Microsoft Active Directory environments.
- **Ports:**
  - **Default:** TCP 389; use StartTLS and validate the server certificate when applicable.
  - **LDAPS:** TCP 636 for LDAP over TLS. Do not send simple-bind credentials over plaintext.

#### c) Kerberos and Mutual Authentication

- **Purpose:** Provides secure mutual authentication between client and server.
- **Features:**
  - Protects against eavesdropping and replay attacks.
  - Utilizes symmetric key cryptography and a trusted third-party (Key Distribution Center).
- **Considerations:**
  - Relies on a central server; potential single point of failure if not properly managed.

#### d) Remote Desktop Services

- **Function:** Allows remote control and access of a Windows machine from a client device.
- **Security Concerns:**
  - Uses well-known ports that can be targeted.
  - Security depends on configuration: enforce TLS, Network Level Authentication,
    patching, and restricted access through a managed gateway or VPN.
- **Access:** Avoid direct internet exposure. Apply MFA at the supported gateway
  or identity layer and monitor remote logons.

---

### 3. Remote Authentication Servers

Technologies and protocols enabling secure remote access and authentication.

#### a) RAS (Remote Access Service)

- **Definition:** Combines hardware and software to facilitate remote access to network resources.
- **Security Measures:**
  - Restrict access to necessary users only.
  - Monitor and analyze daily usage logs.
  - Implement robust RAS authentication mechanisms.

#### b) CHAP (Challenge-Handshake Authentication Protocol)

- **Authentication Process:**
  1. **Challenge:** Authenticator sends a challenge message to the client.
  2. **Response:** Client responds with a hash of the challenge combined with a shared secret (e.g., password).
  3. **Verification:** Authenticator verifies the response; if correct, the connection is maintained; otherwise, it is terminated.
- **Legacy risk:** CHAP and MS-CHAPv2 have known weaknesses. Do not treat
  MS-CHAPv2 as a modern standalone security control; prefer certificate-based
  authentication where supported and validate the authentication server.

#### c) VPN (Virtual Private Network)

- **Function:** Establishes a secure, encrypted connection (tunnel) over a public network.
- **Common Protocols:**
  - **Modern choices:** Maintained IPsec/IKEv2, WireGuard, or TLS-based VPN implementations,
    selected according to organizational requirements.
  - **Legacy context:** L2TP has no encryption by itself; PPTP should be avoided.
- **Configurations:**
  - **Remote Access VPN:** Connects individual clients to a private network.
  - **Site-to-Site VPN:** Connects entire networks to each other.
- **Considerations:**
  - **Split Tunneling:** Allows clients simultaneous access to the internet and the VPN; can pose security risks by bypassing network controls.
  - **GRE (Generic Routing Encapsulation):** Encapsulates network-layer protocols;
    tunneling alone does not encrypt or authenticate the traffic.

#### d) RADIUS vs. TACACS+

**RADIUS (Remote Authentication Dial-In User Service):**
- **Function:** Provides centralized authentication, authorization, and accounting for network access, including dial-up, VPN, and wireless services.
- **Features:**
  - Compatible with EAP and 802.1X protocols.
  - Can be organized into a federation of RADIUS servers for broader authentication management.

**TACACS+ (Terminal Access Controller Access-Control System Plus):**
- **Function:** Provides centralized authentication, authorization, and accounting,
  commonly for network-device administration.
- **Features:**
  - Offers more granular control over user permissions compared to RADIUS.
  - Traditional TACACS+ obfuscates its body; it is not a substitute for modern
    transport protection. Traditional RADIUS also lacks full packet encryption.
    Protect AAA traffic with the secure transport supported by the deployment.

## Sources

- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [RFC 8907: TACACS+ security considerations](https://www.rfc-editor.org/rfc/rfc8907.html)
