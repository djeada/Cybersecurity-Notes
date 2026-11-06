# CVE-2026-97229 — GitLab CI Regex Compiler Integer Overflow

[Repository home](../README.md) · [CVE reports index](README.md)

GitLab reports that under certain conditions an unauthenticated request can
cause affected Community and Enterprise Edition servers to compile a crafted
regular expression from CI/CD configuration. The resulting memory corruption
can allow code execution on the GitLab server. GitLab assigns a CVSS 3.1
score of 10.0 and credits Johan Carlsson (`joaxcar`).

## How it works

GitLab compiles some user-supplied patterns through Ruby's `Regexp.new`.
Ruby's Onigmo engine had an integer overflow when calculating the size of a
compiled pattern. If a size exceeds what its integer type can represent,
subsequent memory operations can use an incorrect size. The vulnerable step
is pattern compilation, which can happen while the server validates CI
configuration, before a runner executes a job.

The same engine is used outside GitLab. Ruby's advisory identifies
applications that compile attacker-controlled patterns as the relevant
exposure and lists the upstream fixes. In GitLab, the affected server and the
Ruby runtime it ships are the components to track.

## Exposure and response

| GitLab CE/EE branch | First fixed release |
| --- | --- |
| 19.2 | `19.2.8` |
| 19.3 | `19.3.5` |
| 19.4 | `19.4.2` |

CISA added this CVE to KEV on 29 October 2026. Update affected self-managed
instances using GitLab's release guidance and verify the running server
version. GitLab says GitLab.com and GitLab Dedicated are patched and publishes
detections for self-managed instances, including CI lint activity and native
worker crashes. Correlate signals with request logs and other incident
evidence before concluding a server was compromised.

## Study exercise

Compare two CI validators. One compiles a developer-defined regular expression
and uses it to match submitted text. The other compiles a regular expression
supplied in the submission. Mark where untrusted input crosses into the
compiler. Explain why limiting runner permissions or setting a matching
timeout leaves the compiler exposure in the second design.

## Related notes

- [Threat modeling](../notes/basics/threat_modeling.md)
- [Incident response](../notes/basics/incident_response.md)

## Sources

- [GitLab critical patch release, scope, and detections](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-4-2-released/)
- [Ruby advisory on the underlying regex compiler fixes](https://www.ruby-lang.org/en/news/2026/10/23/regexp-fixes-for-gitlab-cves/)
- [CISA's corrected KEV bulletin for CVE-2026-97229](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/4310049)
