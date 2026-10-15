# Online Hash Tools

A hash lookup service compares submitted digests with known inputs or guesses
candidate inputs. It does not “decrypt” a one-way hash. Success with a weak or
common password does not imply the underlying algorithm is reversible.

## Data handling

A password hash can be sensitive credential material. Uploading it gives another
party a copy that may be retained or attacked later. Do not submit organizational
or personal credential data without explicit authorization and an appropriate
data-handling agreement.

For learning, use synthetic values and known examples. Prefer local,
authorized password-auditing workflows when handling sensitive material:

- [Hashcat](../../tools/password_cracking/hashcat/README.md)
- [John the Ripper rules](../../tools/password_cracking/john_ripper/custom_rules.md)

Use [modern password storage](hashes_intro.md#password-storage) to make offline
guessing more expensive. A service's claim to support a hash type is not evidence
that it can recover every input.

## Sources

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
