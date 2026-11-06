# CVE-2026-118514 — Symfony HEAD Authorization Bypass

[Repository home](../README.md) · [CVE reports index](README.md)

Symfony disclosed a mismatch between routing and method-based access checks
on 4 November 2026 and credits Ivan Tse with the report. On affected
applications, a `HEAD` request can reach a `GET` controller while bypassing
an access rule that lists only `GET`.

## How it works

HTTP `HEAD` requests ask for the metadata a `GET` would provide, with the
response content omitted. Symfony's router can dispatch both methods to the
same controller. Before the fix, HttpFoundation's request matchers compared
the method literally. A `GET`-only `access_control` rule or firewall could
therefore miss a `HEAD` request even though the controller still ran.
Headers can reveal information, and any side effects in the controller can
still occur.

An earlier fix for CVE-2026-45075 covered certain controller attributes.
CVE-2026-118514 covers the separate request matchers used by access rules and
firewalls. The fix makes a matcher that includes `GET` also include `HEAD`,
aligning the authorization check with routing.

## Exposure and response

| Installed `symfony/http-foundation` release line | Fixed release listed by Symfony |
| --- | --- |
| 5.4 | `5.4.56` |
| 6.x | `6.4.50` |
| 7.x | `7.4.23` |
| 8.x | `8.1.11` |

Update the dependency and verify it in the deployed build, for example with
`composer show symfony/http-foundation` from the application directory. Review
the order of method-specific rules. Where `HEAD` deliberately has a separate
rule for the same path, Symfony's guidance is to place that rule before the
one for `GET`.

## Study exercise

On a local test route with a role requirement, make a matrix for `GET` and
`HEAD` with an authorized account and an anonymous client. Use a harmless
controller log marker to check whether each request reached the handler.
After updating, verify that both anonymous requests are rejected before the
controller runs, and that the authorized `HEAD` response omits the body.

## Related notes

- [Access control methods](../notes/basics/access_control_methods.md)
- [Network protocols](../notes/basics/network_protocols.md)

## Sources

- [Symfony advisory for CVE-2026-118514](https://symfony.com/blog/cve-2026-118514-head-requests-bypass-the-methods-option-of-access-control-and-firewalls-incomplete-fix-for-cve-2026-45075)
- [HTTP Semantics, RFC 9110 section 9.3.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.2)
