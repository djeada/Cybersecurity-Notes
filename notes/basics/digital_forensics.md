# Digital Forensics

Digital forensics preserves, examines, and explains digital evidence in a
repeatable way. It supports [incident response](incident_response.md) but also
requires careful documentation of evidence handling and analytical limits.

## Working process

1. **Scope and authorize:** Define the question, systems, collection authority,
   and permitted handling of personal or sensitive data.
2. **Preserve and collect:** Consider volatile data, isolate originals where
   appropriate, and record the collection method and changes it causes.
3. **Examine:** Work from verified copies with suitable tools; recover relevant
   artifacts such as logs, file metadata, memory data, or network captures.
4. **Analyze:** Correlate artifacts to test hypotheses and build a timeline.
5. **Report:** Separate observations from inferences, explain methods, and state
   missing evidence, tool limitations, and alternative explanations.

Collect volatile evidence before it disappears when feasible. Rebooting can lose
memory contents, while live collection itself changes system state. Record those
effects. For offline disk acquisition, a suitable write blocker helps prevent
writes to the original media; verify its operation and work on a copy.

## Chain of custody

Record an evidence ID, source, collector, UTC acquisition time, collection method,
hashes, storage location, access restrictions, and every transfer or access event.
Each handoff should identify who had custody, when, and why.

Use a modern cryptographic digest such as SHA-256 to compare a preserved image
with a working copy. A matching digest demonstrates byte equality under the hash
assumptions; it does not prove the source was truthful or that custody was sound.

## Evidence and interpretation

| Artifact | What it may help establish | Limitation |
| --- | --- | --- |
| Memory capture | Running processes and in-memory activity | Volatile; collection changes state |
| Filesystem image | Files, metadata, and recoverable deleted content | Encryption, overwrite, and SSD TRIM may prevent recovery |
| Identity and application logs | Account activity and requested actions | Missing retention, clock drift, or attacker modification |
| Network capture | Observed endpoints and protocol activity | Encryption and capture position limit visibility |
| Cloud audit export | Control-plane actions and identity changes | Service permissions, retention, and export scope vary |

Normalize time zones while retaining original timestamps and precision. A file
timestamp alone is insufficient to attribute an action to a particular person.
File carving uses content patterns to recover data; fragmentation and overwritten
content can limit results.

## Practice

Hash a harmless sample file, copy it, and compare the digests. Change the copy and
verify that the digest changes. Write a short evidence record and explain what
this comparison establishes. Use the [file hash example](../../src/README.md).

## Sources

- [NIST SP 800-86: Integrating Forensic Techniques into Incident Response](https://csrc.nist.gov/pubs/sp/800/86/final)
- [NIST Computer Forensics Tool Testing](https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt)
