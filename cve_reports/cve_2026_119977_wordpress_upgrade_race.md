# CVE-2026-119977 — WordPress Core Upgrade Race

[Repository home](../README.md) · [CVE reports index](README.md)

A full-package WordPress core upgrade can briefly expose a second copy of the
application under the site's web root. On affected installations, an attacker
who reaches the staged installer during that window can potentially run code
with the web server account's privileges, without a WordPress account.

## How it works

The updater extracts the release under `wp-content/upgrade/` before copying
the new core files into place. In vulnerable versions the staging directory
name is predictable. If the web server serves that directory and executes its
PHP files, a request can reach the installer between extraction and cleanup.
The staged installer treats the extracted copy as an unconfigured site. This
is a time-of-check/time-of-use race (CWE-367) across the boundary between
temporary update files and executable web content.

The 7.1.4 fix randomizes the staging directory name, preserves the directory's
index file, and excludes `wp-config.php` from the core file copy. The first
upgrade from an affected release can still use the old extraction code, so
the security of that transition depends on how the site is upgraded.

## Exposure and response

- Wordfence lists affected releases from 4.7 through 7.1.3 and publishes the
  fixed versions for each branch. WordPress released 7.1.4 on 28 October 2026.
  WordPress credits Umut Bayram of Picus Security with the report.
- Before using the built-in updater on an affected site, follow the
  researcher's guidance to deny HTTP access to the actual upgrade directory
  at the web server. Verify the rule while preserving local filesystem access
  for the updater. Apply a supported fixed release and confirm the running
  core version after the update.
- CISA added the CVE to KEV on 3 November 2026. For a previously exposed site,
  review requests to staged paths around update times and check the live
  configuration and core files for unexpected changes. Use those findings
  with the [incident response notes](../notes/basics/incident_response.md).

## Study exercise

On a disposable local web server, model the staging directory with an inert
text file. Apply a rule that denies HTTP access to the directory. Verify that
the updater's local account can still read the file, that HTTP requests to
the file are denied, and that a normal site page still loads. Explain which
boundary the rule protects while the old updater is running.

## Related notes

- [Web application security](../notes/basics/web_application_security.md)
- [Vulnerability management](../notes/basics/vulnerability_management.md)

## Sources

- [WordPress 7.1.4 security release and backports](https://wordpress.org/news/2026/10/wordpress-7-1-4/)
- [Wordfence CVE advisory and branch-specific fixes](https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-core/wordpress-core-470-713-unauthenticated-upgrade-window-staged-installer-remote-code-execution)
- [Umut Bayram's analysis of the staging race and first-upgrade exposure](https://www.picussecurity.com/resource/blog/cve-2026-119977-when-updating-wordpress-becomes-the-vulnerability)
- [CISA KEV addition for CVE-2026-119977](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/4318a48)
