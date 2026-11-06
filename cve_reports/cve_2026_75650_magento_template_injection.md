# CVE-2026-75650 — Magento and Adobe Commerce Template Injection

[Repository home](../README.md) · [CVE reports index](README.md)

Adobe disclosed this unauthenticated remote code execution flaw on
7 September 2026. It affects Adobe Commerce, Adobe Commerce B2B, and Magento
Open Source. Adobe reported exploitation against merchants, and CISA added
the CVE to KEV on 8 September.

## How it works

Akamai describes a path where an API request causes attacker-controlled
input to be recorded in a server log. A later request invokes the template
engine, for example when a transactional email is rendered. If the renderer
loads the tainted log as template input, it can evaluate code under the web
process's privileges.

This is a stored injection. The incoming request writes data in one context
and a later operation interprets it in a different context. The relevant
boundary is between server-side data storage and files the template engine
is permitted to evaluate.

## Exposure and response

Adobe's bulletin lists affected builds by product and release line. For
example, it lists `2.4.8-2026-aug` and earlier on that Adobe Commerce and
Magento Open Source release line. Use APSB26-146 and Adobe's hotfix guide to
map the deployed edition and build to the applicable fix. The hotfix is
identified as `VULN-39341`. Adobe directs operators using the hotfix to
rotate their encryption keys as part of remediation.

Verify that the running storefront contains the specific CVE fix. Adobe's
October isolated security patch and this hotfix are separate packages. For an
exposed store, preserve relevant API and server logs and review unexpected
changes to templates or files as part of incident triage.

## Study exercise

Trace a harmless marker from a mock API request to a log entry in a local
test application. Design a regression check that keeps the marker in the
logging path and restricts the renderer to the intended template directory.
Use a normal email preview as a control to show that rendering still works.

## Related notes

- [Web application security](../notes/basics/web_application_security.md)
- [Incident response](../notes/basics/incident_response.md)

## Sources

- [Adobe security bulletin APSB26-146](https://www.adobe.com/trust/security/products/commerce/apsb26-146)
- [Adobe hotfix instructions and encryption key guidance](https://experienceleague.adobe.com/en/docs/commerce-knowledge-base/kb/announcements/commerce-apsb26-146)
- [Adobe guidance on October isolated patches and the separate hotfix](https://experienceleague.adobe.com/en/docs/experience-cloud-kcs/kbarticles/ka-49323)
- [Akamai analysis of the request, log, and renderer path](https://www.akamai.com/blog/security-research/cve-2026-75650-stylesmuggler-adobe-commerce-magento)
- [CISA KEV addition for CVE-2026-75650](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/428fa64)
