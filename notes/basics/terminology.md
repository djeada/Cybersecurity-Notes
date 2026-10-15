# Security Terminology

## Security goals

- **Confidentiality:** Prevent unauthorized disclosure.
- **Integrity:** Protect against unauthorized modification or destruction.
- **Availability:** Keep information and services accessible when needed.

See the [CIA triad](cia_triad.md) for examples.

## Identity and access: AAA

- **Authentication:** Verify an identity using an authenticator.
- **Authorization:** Decide which actions that identity may perform.
- **Accounting:** Record activity and resource usage for auditing.

Accounting supports accountability; it does not automatically provide
**non-repudiation**, which requires evidence that an action or message can be
attributed under the relevant trust assumptions.

## Threat, vulnerability, and risk

| Term | Meaning | Example |
| --- | --- | --- |
| Asset | Something of value to protect | Customer records |
| Threat | A potential cause of harm | A malicious actor seeking records |
| Vulnerability | A weakness a threat could exploit | Missing object-level authorization |
| Exploit | A method of taking advantage of a weakness | Requesting another user's record |
| Risk | Potential harm in context, considering likelihood and impact | Customer data disclosure and service disruption |
| Control | A measure that changes risk | Authorization checks and monitoring |
| Residual risk | Risk remaining after controls | Misconfiguration or undiscovered paths |

An **attack surface** is the set of exposed entry points and interactions.
**Defense in depth** combines controls so one failure need not defeat the whole
system.

## Controls and actors

Controls may be administrative (policy and training), technical (access checks
and encryption), or physical (locks and protected facilities). Their purposes
include prevention, detection, correction, and recovery.

Potential threat actors include criminals, malicious insiders, activists, and
state-associated groups. Authorized security researchers assess systems within
an agreed scope. Labels such as “white hat” or “grey hat” do not replace explicit
permission.

An **advanced persistent threat (APT)** describes a capable, persistent threat;
the term is often associated with state-sponsored activity but is not a synonym
for every nation-state action.

See [access control](access_control_methods.md), [risk assessment](risk_assessment.md),
and [threat modeling](threat_modeling.md).

## Sources

- [NIST cybersecurity glossary](https://csrc.nist.gov/glossary)
