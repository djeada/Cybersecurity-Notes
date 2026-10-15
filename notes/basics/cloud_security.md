# Cloud and Container Security

Cloud security depends on the service and its **shared responsibility model**.
The provider operates underlying infrastructure; customers still make decisions
about identities, data, access, and configuration. For a virtual machine, the
customer typically manages the guest OS and application. A managed service moves
some operational tasks to the provider, but does not remove customer responsibility.
Check the contract and documentation for each service.

## Cloud control checklist

| Area | Questions to answer |
| --- | --- |
| Identity | Are human and workload identities separate? Are privileges scoped, temporary where possible, and regularly reviewed? |
| Administration | Are privileged accounts protected with phishing-resistant MFA and monitored emergency access? |
| Network | Are storage, databases, and administrative endpoints exposed only where needed? Is outbound access controlled? |
| Data | Are storage access rules, encryption, key permissions, retention, and recovery configured? |
| Secrets | Are secrets stored outside source code and images, narrowly scoped, and rotated after exposure? |
| Visibility | Are control-plane and relevant data-access logs enabled, retained, and available during an account compromise? |
| Recovery | Can critical data and infrastructure be restored after deletion or account loss? |

Prefer workload identities or short-lived credentials over embedded access keys.
Protect metadata-service access and limit which workloads can retrieve credentials.

## Container boundaries

Containers commonly share the host kernel; they are not the same isolation
boundary as separate virtual machines.

- Build from maintained minimal images and track their provenance and dependencies.
- Run as a non-root user; avoid privileged mode, unnecessary capabilities, host
  namespaces, and exposing the container runtime socket.
- Limit CPU, memory, filesystem writes, and network access.
- Keep secrets out of image layers, build arguments, and committed configuration.
- Scan and rebuild images when dependencies change; patch the host and runtime too.
- In an orchestrator, restrict service accounts, workload permissions, and network
  paths. Monitor privileged workload creation and unexpected administrative changes.

## Practice

Review a lab application's identity permissions, storage access, and deployment
configuration. Demonstrate that a container cannot read another workload's secret
and that an unauthorized storage request is denied. Record both the expected
control and the evidence.

See [virtualization](virtualization.md), [web application security](web_application_security.md),
and [incident response](incident_response.md).

## Sources

- [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
