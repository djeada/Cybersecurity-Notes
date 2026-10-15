# Incident Response

An event is an observable occurrence. An incident requires a coordinated response
because it threatens systems, data, or operations. Define escalation criteria
before an emergency; an alert alone does not establish compromise.

## Framework and preparation

NIST SP 800-61 Rev. 3 aligns incident response with CSF 2.0. Govern, Identify, and
Protect support preparation; Detect, Respond, and Recover handle incidents.
Lessons learned feed improvements throughout the organization. The operational
checklist below is a practical sequence, not a replacement for that framework.

Prepare an asset inventory, responders and deputies, an out-of-band contact
method, evidence storage, log access, and tested recovery procedures.

## Operational checklist

| Stage | Actions | Record |
| --- | --- | --- |
| Triage | Validate the alert; determine scope, impact, and urgency | Incident ID, affected assets, owner, known facts |
| Contain | Limit ongoing harm by isolating affected systems or restricting identities | What changed, when, why, and who approved it |
| Investigate | Correlate identity, endpoint, network, and application evidence | Timeline, evidence references, confidence and gaps |
| Eradicate | Remove persistence, fix the entry point, and replace compromised secrets | Remediation tasks and verification results |
| Recover | Restore trusted systems in stages and monitor for recurrence | Recovery criteria, service owner sign-off |
| Improve | Review causes, detection delays, and response decisions | Assigned follow-up actions and deadlines |

Containment and evidence collection may run in parallel. Avoid rebooting or
wiping systems before considering volatile evidence; ongoing harm can justify
immediate isolation. Record the tradeoff and actions taken.

## Example: compromised cloud account

Preserve available sign-in and audit logs, identify active sessions and workload
credentials, restrict affected access, revoke applicable sessions, rotate exposed
secrets, and inspect changes made by the identity. A password reset alone may
leave sessions, API keys, or newly created accounts usable.

## Incident record

```text
Incident ID and severity:
Responder and service owner:
First observed / last updated (UTC):
Confirmed facts and evidence references:
Hypotheses and unanswered questions:
Affected identities, assets, and business services:
Containment actions and decision log:
Recovery criteria and follow-up owners:
```

Practice with a tabletop exercise. Check that responders can access the runbook
when the main identity provider or communication service is unavailable.

See [digital forensics](digital_forensics.md), [monitoring](monitoring.md), and
[disaster recovery](disaster_recovery.md).

## Sources

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [CISA Incident and Vulnerability Response Playbooks](https://www.cisa.gov/news-events/news/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)
