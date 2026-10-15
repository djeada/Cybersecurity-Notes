# Hashing and Password Storage

A cryptographic hash maps arbitrary input to a fixed-size digest. It is
deterministic and is not encryption: there is no decryption key. Low-entropy
inputs such as common passwords can still be guessed and checked against a digest.

## Security properties

- **Preimage resistance:** Given a digest, finding an input with that digest
  should be infeasible.
- **Second-preimage resistance:** Given one input, finding a different input with
  the same digest should be infeasible.
- **Collision resistance:** Finding any two distinct inputs with the same digest
  should be infeasible. A birthday attack targets this property; it does not
  require matching a specific original message.

Use a modern digest such as SHA-256 or SHA-3 for security-sensitive hashing.
MD5 and SHA-1 have broken collision resistance and are unsuitable for new
security-sensitive integrity or signature designs.

## Integrity is not authenticity

A checksum detects changes only if the expected digest is trustworthy. An attacker
who replaces both a file and its published digest can defeat that comparison.
Use authenticated distribution, a digital signature, or an HMAC with an
appropriately managed secret key when authenticity matters.

Try the [file hash utility](../../src/README.md) with a harmless file and a known
SHA-256 digest.

## Password storage

General-purpose hashes such as SHA-256 are intentionally fast and are not suitable
password-storage functions on their own.

- Use a password hashing scheme such as Argon2id with parameters appropriate to
  the environment. Follow maintained guidance for alternatives and required
  compliance constraints.
- A **salt** is a unique, nonsecret random value stored with each password hash.
  It prevents shared hashes for identical passwords and reuse of precomputed work.
- A **work factor** increases the cost of each guess; memory-hard schemes also
  require memory. Tune parameters and plan to upgrade them over time.
- A **pepper** is an optional secret stored separately from the password database.
  Its lifecycle and recovery need careful design.

Salting and increasing computational cost solve different problems. A salt alone
does not make each password guess substantially slower.

## Windows terminology

The NT password hash is based on MD4 over a UTF-16LE password, not RC4. NTLM is an
authentication protocol family; NTLMv2 uses HMAC-MD5 in its response calculation.
Pass-the-hash abuses password-equivalent material in NTLM authentication.
Kerberos ticket abuse is a distinct technique.

See [Windows hashes](windows_hashes.md),
[Linux hashes](linux_user_hashes.md), and [digital signatures](signature_and_certificates.md).

## Sources

- [NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Microsoft: NTLM overview](https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview)
