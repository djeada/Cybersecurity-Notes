# Encryption

Encryption protects **confidentiality** by transforming plaintext into ciphertext
under a key. Integrity and authenticity need additional properties, such as
authenticated encryption, a MAC, or a digital signature. Encryption alone does
not guarantee either.

## Data states

| State | Examples | Security considerations |
| --- | --- | --- |
| At rest | Files, databases, backups | Protect keys separately; encryption does not stop an authorized compromised application |
| In transit | HTTPS, SSH, service connections | Authenticate peers and validate certificates or host keys |
| In use | Data processed by an application | Restrict process and user access; ordinary disk encryption does not hide live memory |

A secure design must also define key generation, storage, access, backup,
rotation, and destruction. Losing a key can make data unavailable; exposing it
can defeat encryption.

## Symmetric encryption

Symmetric schemes use a shared secret key and are efficient for bulk data.
AES is a block cipher with a 128-bit block and 128-, 192-, or 256-bit keys.
ChaCha20 is a stream cipher.

Prefer established **authenticated encryption with associated data (AEAD)**
schemes such as AES-GCM or ChaCha20-Poly1305 through a maintained library.
They protect ciphertext integrity and can authenticate additional unencrypted
metadata. Follow the scheme's nonce requirements: reusing a nonce with the same
key can be catastrophic.

A stream cipher or block cipher is a primitive, not a complete application
protocol. Do not design your own cipher mode or combine primitives casually.

## Public-key cryptography

Public and private keys support several distinct operations:

| Operation | Examples | Purpose |
| --- | --- | --- |
| Public-key encryption | RSA-OAEP | Encrypt for a recipient who holds the private key |
| Key agreement | ECDH, finite-field DH | Establish shared key material; authenticate the exchange separately |
| Digital signatures | RSA-PSS, ECDSA, Ed25519 | Sign with a private key and verify with the public key |

Diffie–Hellman is key agreement, not an encryption algorithm. Elliptic-curve
cryptography is a family of constructions, not one interchangeable operation.
Kerberos is an authentication protocol that uses cryptography, not a cipher.

Hybrid protocols combine public-key operations with symmetric encryption.
TLS 1.3 commonly uses ephemeral key agreement, signatures for authentication, and
AEAD for record protection. It does not use RSA key transport.

## Historical algorithms

DES, 3DES, and RC4 belong in historical study, not new designs. Blowfish has a
64-bit block; Twofish has a 128-bit block. Small block sizes can constrain safe
data volumes even when a cipher's key length looks large.

A one-time pad has theoretical secrecy only when its key is truly random, as
long as the message, secret, and never reused. Secure key distribution remains
a major practical obstacle.

Steganography hides the presence of a message rather than necessarily encrypting
its content. A cryptographically secure random generator is a building block for
keys and nonces, not an encryption scheme.

See [hashing](hashes_intro.md), [RSA](rsa.md), and [PKI and TLS](../basics/pki.md).

## Sources

- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [RFC 5116: authenticated encryption interface](https://www.rfc-editor.org/rfc/rfc5116.html)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [NIST: transition away from 3DES](https://csrc.nist.gov/news/2023/nist-to-withdraw-sp-800-67-rev-2)
