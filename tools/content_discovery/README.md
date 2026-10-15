# Content Discovery

Content discovery uses known paths, application links, and wordlists to find web
resources during an authorized assessment. A discovered path is not necessarily
a vulnerability; verify access controls and intended exposure.

- [DIRB](dirb/README.md): wordlist-based web content discovery.
- [Gobuster](gobuster/README.md): directory and file discovery, with other modes
  available depending on the installed version.

## Before running a scan

Confirm the allowed hostnames, paths, request rate, test window, and excluded
operations. Start with a small wordlist and conservative concurrency. Check
whether the server returns the same page for nonexistent paths, follows
redirects to other hosts, or requires a test session.

On Kali, packaged wordlists are commonly under `/usr/share/wordlists`; SecLists
may be installed separately. Verify the path on your own machine.

## Interpreting results

Compare response status, length, and content with a known nonexistent path.
A `200` response can be a generic error page; `401` and `403` indicate access
restrictions rather than permission to bypass them. Keep evidence minimal and
report the configuration or access-control issue, not just the path name.

See [web application security](../../notes/basics/web_application_security.md).
