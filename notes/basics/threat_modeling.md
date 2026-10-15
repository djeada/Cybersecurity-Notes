# Threat Modeling

Threat modeling identifies ways a system could be misused and turns them into
design decisions and verification tasks. It complements
[risk assessment](risk_assessment.md) and should evolve with the application.

## A repeatable process

1. Define the system, sensitive assets, users, administrators, and external services.
2. Draw the data flows, stores, entry points, and **trust boundaries** where data
   crosses between different privileges or owners.
3. Describe plausible abuse at each boundary, including business logic failures.
4. Choose a response: mitigate, avoid, transfer, or explicitly accept the risk.
5. Assign an owner and a test for each mitigation; revisit the model after changes.

## STRIDE prompts

| Threat | Question to ask | Example control |
| --- | --- | --- |
| Spoofing | Can a caller impersonate another identity? | Authenticate users and workloads |
| Tampering | Can someone alter a request or stored record? | Authorize writes and verify integrity |
| Repudiation | Can a sensitive action occur without useful evidence? | Protect audit records |
| Information disclosure | Can data cross an unintended boundary? | Check object and field access |
| Denial of service | Can one caller exhaust a shared resource? | Enforce quotas and timeouts |
| Elevation of privilege | Can a lower privilege user gain administrative capabilities? | Separate roles and privileged operations |

STRIDE is a prompt list, not proof that every threat has been found. Include abuse
such as refund fraud, account recovery misuse, and cross-tenant access.

## Worked example: invoice download

An authenticated customer requests an invoice using an identifier in a URL.
The trust boundary is between the customer-controlled request and the server's
invoice store.

| Finding | Decision | Verification |
| --- | --- | --- |
| A customer could request another customer's invoice | Enforce ownership on every read | Customer A cannot read customer B's invoice |
| Download links could leak through logs | Avoid bearer secrets in URLs; redact sensitive fields | Review access and application logs |
| Repeated downloads could exhaust storage bandwidth | Set per-customer quotas | Test limits in a lab |

## Practice

Model a password-reset flow. Record what happens when a token is reused, expires,
or is sent to the wrong account. Link the decisions to
[web application security](web_application_security.md).

## Sources

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Threat Modeling project](https://owasp.org/www-community/Threat_Modeling)
