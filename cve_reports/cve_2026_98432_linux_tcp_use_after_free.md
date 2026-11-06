# CVE-2026-98432 — Linux IPv4 TCP Use-After-Free

[Repository home](../README.md) · [CVE reports index](README.md)

The Linux kernel CVE team disclosed a race in IPv4 TCP connection setup on
15 October 2026. Anthropic later described how Claude helped find the issue
and generated a research exploit that ran code as root against a Multipath
TCP (MPTCP) listener without credentials or user interaction.

## How it works

During connection setup, the kernel transfers IPv4 options from a pending
request to the new child socket without copying them. A second CPU can still
read those options while preparing a SYN-ACK for a retransmitted SYN. If the
child socket is destroyed first, that CPU can read freed memory. The kernel
announcement also describes a related lifetime race during request migration.

The affected readers already used read-copy-update (RCU), a mechanism that
allows readers to access shared data while another CPU replaces it. The fix
defers freeing the options until a grace period has passed and pre-existing
RCU readers have finished. This restores the lifetime guarantee the readers
depend on.

## Exposure and response

The upstream issue dates to Linux 4.4. The kernel team's announcement lists
`6.12.113`, `6.18.56`, and `7.2.10` among the first fixed releases on their
respective branches. Use the distribution's CVE tracker for installed
kernels because vendors can backport a fix to a lower version number. Install
the applicable kernel update and, after any required reboot, check the
running release with `uname -r` against the vendor's fixed package.

Anthropic's remote-root demonstration used MPTCP. Canonical identifies the
flaw in shared IPv4 TCP code and recommends applying the kernel security
update even on systems with MPTCP disabled. The demonstration establishes an
impact under research conditions. Assess reachable listeners and running
kernels separately when triaging a fleet.

## Study exercise

Trace two CPUs on paper. CPU A starts an RCU read and loads the options
pointer. CPU B destroys the child socket before CPU A finishes. Identify
the unsafe memory access if CPU B frees the options immediately, and place
the actual free after the RCU grace period in the patched sequence. Explain
why the order matters even if the pointer value itself stays the same.

## Related notes

- [Network protocols](../notes/basics/network_protocols.md)
- [OS hardening](../notes/basics/os_hardening.md)

## Sources

- [Linux kernel CVE team announcement, code path, and fixed versions](https://lists.openwall.net/linux-cve-announce/2026/10/15/1)
- [Anthropic research account and MPTCP demonstration](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)
- [Canonical analysis of MPTCP and mitigation](https://ubuntu.com/blog/fixes-available-in-proposed-pocket-for-cve-2026-98432)
- [Canonical package status for CVE-2026-98432](https://ubuntu.com/security/CVE-2026-98432)
