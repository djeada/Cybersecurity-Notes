# CVE-2026-109618 and CVE-2026-109619 — PHP2Shell

[Repository home](../README.md) · [CVE reports index](README.md)

Two flaws in PHP's request lifecycle can let an unauthenticated attacker
execute code with the web worker's privileges. The affected code is in the
PHP runtime used by applications such as WordPress, Drupal, and Joomla.
PHP published fixes on 21 October 2026, and CISA added both CVEs to KEV on
26 October.

## How they work

A PHP web worker initializes a request, runs the application, and cleans up
request-owned memory. Some request parsing occurs during initialization,
before the application has a chance to authenticate the caller.

| CVE | Failure | Fix |
| --- | --- | --- |
| CVE-2026-109618 | An out-of-memory error can abort parsing while request data is only partly initialized. Shutdown can then operate on that incomplete state. | Report a soft out-of-memory error at a safe point and terminate the worker at a higher threshold. |
| CVE-2026-109619 | A fatal error can leave worker state pointing into a request's freed memory. An early operation on a later request handled by that worker can access the stale state. | Reset request-owned state across request boundaries, including after failures. |

PHP's advisory describes code execution against Apache `mod_php` before
application code runs. PHP also validated a session-lifecycle path for
CVE-2026-109619 on PHP-FPM that depends on a suitable application operation.
The PHP integration and application configuration determine which paths
are reachable.

OpenAI reports that Calif used GPT-5.6 Sol to identify a critical flaw and
that Wiz independently reported both CVEs. Wiz describes using Gemini 4
Argon and GPT-5.6 Sol during its research. These accounts describe discovery
and validation. The KEV entries separately establish exploitation in the wild.

## Exposure and response

| PHP branch | First upstream release fixing both CVEs |
| --- | --- |
| 8.2 | `8.2.35` |
| 8.3 | `8.3.36` |
| 8.4 | `8.4.27` |
| 8.5 | `8.5.12` |

Inventory PHP for each web workload, including per-site workers and container
images. Apply the vendor's fixed package, restart or redeploy the web workers,
and verify the running build. For distributor backports, check the package
revision against the distributor's advisory. Earlier branches can also be
affected. Check your distributor for a backport or move to a supported build.

PHP also disclosed CVE-2026-115560 on 23 October for a separate session upload
progress issue. It requires upload progress to be enabled and the application
to switch `session.serialize_handler` from `php_binary` or `php_serialize` to
`php` before starting the session. For affected setups, PHP advised disabling
`session.upload_progress.enabled` in the configuration used before request
parsing and restarting workers while awaiting a fixed release.

## Study exercise

In a disposable local PHP stack, record `php -v` in the terminal. Use a
temporary local-only handler to report `PHP_VERSION` and `PHP_SAPI` from a
web request. Compare the results with the package or image used by the worker,
then remove the handler. Explain which observations would establish that the
service handling web traffic is running the patched build.

## Related notes

- [WordPress core upgrade race](cve_2026_119977_wordpress_upgrade_race.md)
- [Vulnerability management](../notes/basics/vulnerability_management.md)

## Sources

- [PHP October security release and fixed versions](https://www.php.net/archive/2026.php#2026-10-21-5)
- [PHP advisory for CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w)
- [PHP advisory for CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)
- [PHP informational advisory for CVE-2026-115560](https://openwall.com/lists/oss-security/2026/10/23/23)
- [OpenAI account of the coordinated PHP disclosure](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/)
- [Wiz's account of its PHP2Shell research](https://www.wiz.io/blog/php2shell-php-rce)
- [CISA KEV additions for both PHP2Shell CVEs](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/4309083)
