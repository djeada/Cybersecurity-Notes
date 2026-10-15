# Cybersecurity Notes

Study notes, practical tool references, quizzes, and lab walkthroughs covering
security fundamentals, cryptography, OSINT, penetration testing, and defense.

## Start here

| Section | What you will find |
| --- | --- |
| [Notes](notes/README.md) | Complete topic index, from fundamentals to incident response |
| [Tools](tools/README.md) | Burp Suite, Wireshark, Metasploit, and other practical references |
| [Quizzes](quizzes/README.md) | General security, architecture, and forensics revision |
| [Walkthroughs](walkthroughs/README.md) | TryHackMe and Hack The Box lab write-ups |
| [Python examples](src/README.md) | Small utilities, their dependencies, and usage |
| [Learning resources](resources.md) | Standards, books, courses, blogs, and practice platforms |
| [Certificates](certificates/README.md) | Course completion records |

## Suggested reading path

1. **Foundations:** [Terminology](notes/basics/terminology.md),
   [CIA triad](notes/basics/cia_triad.md), and
   [network basics](notes/basics/network_basics.md).
2. **Protect systems:** [Authentication](notes/basics/authentication_models.md),
   [access control](notes/basics/access_control_methods.md),
   [OS hardening](notes/basics/os_hardening.md), and
   [browser security](notes/basics/securing_browser.md).
3. **Protect data and applications:** [Hashing](notes/cryptography/hashes_intro.md),
   [encryption](notes/cryptography/encryption.md),
   [PKI and TLS](notes/basics/pki.md),
   [threat modeling](notes/basics/threat_modeling.md), and
   [web application security](notes/basics/web_application_security.md).
4. **Operate and defend:** [Cloud security](notes/basics/cloud_security.md),
   [vulnerability management](notes/basics/vulnerability_management.md),
   [monitoring](notes/basics/monitoring.md),
   [incident response](notes/basics/incident_response.md), and
   [digital forensics](notes/basics/digital_forensics.md).
5. **Practice:** Use the tool references in an authorized lab, work through a
   walkthrough, then revisit the quizzes.

## Using the practical material

Run scans, password tests, and exploitation exercises only against systems you own
or have explicit permission to assess. Lab addresses, flags, software versions,
and outputs in walkthroughs describe a particular exercise; adapt them to your
own lab. Keep credentials, private keys, and personal data out of commits.

The RSA arithmetic example uses deliberately small numbers to explain the math.
Use maintained cryptographic libraries and established protocols in real systems.

## Contributing and checking changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for the note format and review guidance.
The following checks require only Python 3.10 or newer:

```bash
python scripts/check_notes.py
python -m unittest discover -s tests -v
```

The documentation check validates local file links, heading anchors, document
titles, and fenced code blocks. It does not make network requests or run lab tools.

## License

[MIT](LICENSE)
