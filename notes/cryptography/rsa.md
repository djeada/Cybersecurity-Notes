# RSA: Rivest–Shamir–Adleman

RSA is a public-key cryptosystem. Its security is connected to the difficulty of
factoring a large composite integer into its prime factors, not factoring
a prime number.

## Key components

| Symbol | Meaning |
| --- | --- |
| `p, q` | Distinct secret primes |
| `n = p × q` | Public modulus |
| `φ(n) = (p − 1)(q − 1)` | Euler's totient for the two-prime construction |
| `e` | Public exponent, coprime to `φ(n)` |
| `d` | Private exponent satisfying `e × d ≡ 1 mod φ(n)` |

The public key is `(n, e)`. The private key includes `d` and usually the prime
factors and other values used to accelerate private operations.

## Textbook arithmetic

For a representative `m` with `0 ≤ m < n`:

- Encryption: `c = m^e mod n`; decryption: `m = c^d mod n`.
- Signing arithmetic: `s = m^d mod n`; verification checks `s^e mod n = m`.

**A signature uses the private exponent; verification uses the public exponent.**
Signing is not generally described as encrypting with a private key.

For a deliberately tiny example, `p = 61`, `q = 53`, `n = 3233`, `e = 17`,
and `d = 2753`. The [Python example](../../src/rsa.py) demonstrates the arithmetic
and rejects invalid parameters. These small keys and raw operations are
educational and insecure.

## Practical RSA

Textbook RSA is deterministic and lacks the encoding, padding, and implementation
protections required for security.

- Use a maintained library with **RSA-OAEP** for encryption and **RSA-PSS** for
  new signature applications where the protocol supports them.
- Follow the protocol's key-size requirements; the library guidance recommends
  at least 2048 bits. Never deploy the tiny keys used in teaching examples.
- Encrypt bulk data with an authenticated symmetric scheme; RSA-OAEP accepts only
  a limited message size and is typically used in a hybrid construction.
- Generate keys with a cryptographically secure generator, protect private keys,
  and plan their rotation and revocation.
- TLS 1.3 does not use RSA key transport; RSA certificates can still authenticate
  a connection through signatures.

See [encryption](encryption.md), [signatures](signature_and_certificates.md), and
[PKI and TLS](../basics/pki.md).

## Sources

- [RFC 8017: PKCS #1 v2.2](https://www.rfc-editor.org/rfc/rfc8017.html)
- [cryptography library RSA guidance](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
