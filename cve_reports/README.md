# CVE Reports and Vulnerability Write-ups

[Repository home](../README.md) · [Notes index](../notes/README.md)

Deep dives into specific disclosed or hypothesized vulnerabilities: how the
underlying bug works, what is independently confirmed versus hypothesized,
and a lab-style reproduction where one applies. Each entry states plainly
what it could and could not verify in public sources (NVD, vendor
advisories, mailing lists) — a write-up here is not a substitute for a
vendor advisory or an official CVE record, and a lab reproduction in one of
these files is not, by itself, evidence of a real-world, unpatched,
publicly disclosed vulnerability.

Apply the [lab usage guidance](../README.md#using-the-practical-material)
from the repository home to any reproduction steps below.

## Reports

### Disclosed CVEs

The reports below use public advisories reviewed on 6 November 2026.
Discovery credit identifies who reported or researched the flaw. A research
demonstration shows what worked under test conditions. The [CISA Known Exploited
Vulnerabilities (KEV) Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
lists vulnerabilities with evidence of exploitation in the wild.

| Report | Study topic | Discovery and exploitation evidence |
| --- | --- | --- |
| [CVE-2026-119977 · WordPress core upgrade race](cve_2026_119977_wordpress_upgrade_race.md) | Trust boundaries during updates | Reported by Umut Bayram. Listed in CISA KEV. |
| [CVE-2026-118350 · Chrome Turbolev memory safety](cve_2026_118350_chrome_turbolev.md) | Browser code execution and sandboxing | Google credits OpenAI Codex Security. |
| [CVE-2026-111497 · Brotli decoder out-of-bounds write](cve_2026_111497_brotli_decoder.md) | Streaming parser state and bundled dependencies | Node.js credits OpenAI Codex Security. Listed in CISA KEV. |
| [CVE-2026-98432 · Linux IPv4 TCP use-after-free](cve_2026_98432_linux_tcp_use_after_free.md) | Concurrent object lifetime and RCU | Anthropic reports Claude-assisted discovery and a research demonstration. |
| [CVE-2026-97229 · GitLab CI regex compiler overflow](cve_2026_97229_gitlab_ci_regex.md) | Server-side parsing of untrusted configuration | Reported by Johan Carlsson. Listed in CISA KEV. |

### Other write-ups

- [musl `crypt()` overflow and a hypothetical SSH password bypass](musl_crypt_ssh_bypass.md) — a confirmed musl libc bug (returns the literal `*` for passwords over 256 bytes, crashing PAM) examined alongside an unverified hypothesis about chaining it into an SSH authentication bypass.
