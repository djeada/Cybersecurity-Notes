# CVE-2026-108097 — Drupal Field UI Code Execution

[Repository home](../README.md) · [CVE reports index](README.md)

On 14 October 2026, Drupal published a critical remote code execution advisory
for Field UI, the core module used to configure entity fields and their
display. Drupal credits Drew Webber and Octavio Galland. Its advisory
identifies serious paths through contributed modules, including at least
one that an unauthenticated visitor can reach.

## How it works

Drupal represents renderable elements as structured arrays. Field UI used a
row-level `#region_callback` to determine where to place a table row. A
callback is executable behavior selected by name or reference. If another
module lets untrusted input influence that callback, rendering the table can
invoke code with the privileges of the Drupal process. The fix removes the
row callback invocation, as documented in Pantheon's backport notes.

The flaw is in core. Drupal describes the vulnerable operation becoming
reachable through contributed modules or potentially custom code. A useful
inventory therefore includes the installed core version, whether Field UI is
enabled, and which extensions expose paths into the affected functionality.

## Exposure and response

| Affected core versions | Fixed release listed by Drupal |
| --- | --- |
| `8.9.0` through releases before `10.6.19` | `10.6.19` |
| `11.0.0` through releases before `11.3.19` | `11.3.19` |
| `11.4.0` through releases before `11.4.10` | `11.4.10` |
| `12.0.0-alpha1` through prereleases before `12.0.0-beta2` | `12.0.0-beta2` |

Use a supported, fixed core release. Drupal lists uninstalling `field_ui`
as a temporary mitigation while arranging an update. After deployment,
verify the installed core version and exercise the Manage fields and Manage
display pages, especially if custom code used the old callback.

## Study exercise

Two lab sites run Drupal `11.4.9`. Site A has Field UI uninstalled. Site B
has Field UI enabled and a contributed module with an anonymous route into
the affected functionality. For each site, record the core version, module
state, and route access, then explain which configuration makes the vulnerable
operation reachable and what evidence would close its remediation ticket.

## Related notes

- [PHP2Shell and the PHP request lifecycle](cve_2026_109618_109619_php_request_lifecycle.md)
- [Threat modeling](../notes/basics/threat_modeling.md)

## Sources

- [Drupal core advisory SA-CORE-2026-014](https://www.drupal.org/sa-core-2026-014)
- [Drupal Field UI module guide](https://www.drupal.org/docs/8/core/modules/field-ui)
- [Pantheon's Field UI backport and compatibility notes](https://docs.pantheon.io/release-notes/2026/10/drupal-7-107-security-update)
