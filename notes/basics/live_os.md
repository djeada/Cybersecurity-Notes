# Live Operating Systems

A live operating system boots from removable media without requiring installation
on the computer's internal drive. Many live systems can still access internal
disks or use persistent storage; being a live system alone does not mean it
leaves no traces.

## Example: Tails

Tails is a privacy-focused live system designed to minimize local traces and route
internet connections through Tor. By default it avoids writing session data to
the internal disk. Optional encrypted Persistent Storage retains selected data
across boots.

MAC address anonymization can reduce local-network identification. It does not
change the identity of accounts you log into or eliminate browser and traffic
correlation risks.

## Practical limits

- A compromised firmware, hardware keylogger, or other hostile component can
  defeat protections provided by a live OS.
- Remote services and network observers may retain records regardless of local
  storage behavior.
- Files written to another disk, printed documents, or deliberately enabled
  persistence can survive shutdown.
- Keep the live image updated and verify installation media using the project's
  published verification procedure.

See [anonymous browsing](anonymous_browsing.md) for threat-model considerations.

## Sources

- [Tails security warnings](https://tails.net/doc/about/warnings/index.en.html)
- [Tails Persistent Storage](https://tails.net/doc/persistent_storage/index.en.html)
