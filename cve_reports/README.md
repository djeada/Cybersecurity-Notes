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

- [musl `crypt()` overflow and a hypothetical SSH password bypass](musl_crypt_ssh_bypass.md) — a confirmed musl libc bug (returns the literal `*` for passwords over 256 bytes, crashing PAM) examined alongside an unverified hypothesis about chaining it into an SSH authentication bypass.
