# Web Application and API Security

An application must enforce security on the server even when the browser or API
client is modified. Begin with a [threat model](threat_modeling.md) of identities,
data, business operations, and trust boundaries.

## Core controls

| Area | Practical control | Verification in an authorized lab |
| --- | --- | --- |
| Authentication | Use a maintained identity system; protect recovery and require appropriate MFA | Check expired reset tokens and revoked sessions |
| Authorization | Deny by default; check action, object ownership, and tenant on every request | Customer A cannot read or change customer B's records |
| SQL injection | Bind data using parameterized queries; allowlist dynamic identifiers | Quotes in user data do not change query structure |
| Cross-site scripting (XSS) | Use context-aware output encoding and safe templating | User text renders as text in HTML, attributes, and scripts |
| Cross-site request forgery (CSRF) | Protect cookie-authenticated state changes with CSRF tokens and appropriate cookie settings | Cross-origin state changes without a valid token fail |
| Server-side request forgery (SSRF) | Restrict destinations and outbound access; validate redirects and resolved addresses | A user-supplied URL cannot access internal or metadata services |
| File uploads | Limit size and type, generate storage names, and prevent execution | Uploaded files cannot execute as server code |
| Resource abuse | Apply quotas, pagination, payload limits, and timeouts | One caller cannot request unlimited expensive work |

Input validation complements these controls; it does not replace parameterized
queries, authorization, or output encoding. Content Security Policy is an
additional defense against XSS, not a substitute for safe rendering.

## Sessions and browser boundaries

- Use HTTPS and appropriately scoped cookies with `Secure`, `HttpOnly`, and a
  suitable `SameSite` policy. Rotate session identifiers after login or privilege
  changes; expire and revoke sessions on the server.
- Treat CORS as a browser response-sharing policy. It is not authentication or
  authorization, and it does not stop non-browser clients from sending requests.
- Validate token signatures, expected algorithms, issuer, audience, and expiry.
  A signed token still needs authorization checks and a revocation strategy.
- Keep secrets out of URLs and logs. Return useful errors without stack traces or
  credentials; log enough context for investigation.

## Secure delivery

Review code and dependencies, separate environments and deployment identities,
test security requirements, and monitor changes after release. Use
[SQL injection notes](../pentesting/sql_injections/README.md) for deeper study.

## Sources

- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
