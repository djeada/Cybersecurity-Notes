# Access Control Methods and Models

Authentication establishes an identity. Authorization decides which resources and
actions that identity may access. Apply checks on each request, including access
to a particular record or tenant.

## Models

| Model | How access is decided | Example |
| --- | --- | --- |
| Discretionary access control (DAC) | An owner grants permissions | A file owner grants read access |
| Mandatory access control (MAC) | A centrally enforced policy compares labels and clearances | Classified records subject to a labeling policy |
| Role-based access control (RBAC) | Permissions are assigned to roles held by users | A support role can view tickets |
| Attribute-based access control (ABAC) | A policy evaluates subject, resource, action, and environment attributes | A managed device can access a record in an allowed region |

Rule-based policies are not limited to MAC. No model is universally the
“strictest”; the policy, implementation, and administration determine protection.

## Operating principles

- Deny by default and grant only the privileges needed for a task.
- Separate ordinary and administrative accounts and sensitive duties.
- Review grants, group memberships, service accounts, and temporary access.
- Revoke access when roles change or accounts are no longer needed.
- Log security-relevant decisions and protect the resulting records.

SSO reduces repeated sign-in; it does not remove the need for per-application
authorization or lifecycle management.

## Filesystem permissions

Windows NTFS supports explicit and inherited access-control entries. Review
effective permissions and inheritance rather than assuming a single grant wins.
Moving a file within the same NTFS volume generally retains its permissions;
a copy or a move across volumes generally inherits destination permissions.
Tools and options can preserve or replace permissions, so verify the result.

Linux mode bits and ACLs govern filesystem access, while additional controls
such as SELinux or AppArmor can further restrict processes.

## Password and elevation policies

Favor long, unique passwords, compromised-password screening, password managers,
and appropriate MFA. NIST SP 800-63B-4 requires at least 15 characters for a
password used as a single factor; passwords used within MFA may be at least
8 characters. It rejects mandatory composition rules and routine password changes
without evidence of compromise.

A Windows secure attention sequence such as `Ctrl + Alt + Delete` helps reach
a trusted sign-in path when required by policy; it does not prove a user is local
or prevent all remote logons.

User Account Control (UAC) prompts for consent or credentials when elevation is
needed. It is not a replacement for least privilege or a security boundary
against code already running with appropriate user rights.

See [authentication models](authentication_models.md) and
[web application security](web_application_security.md).

## Sources

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [Microsoft: UAC overview](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/)
