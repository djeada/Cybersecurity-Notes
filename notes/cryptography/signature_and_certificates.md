# Digital Signatures and Certificates

Digital signatures authenticate a message and detect modification. They do not
hide the message's contents.

## Signing and verification

The signer uses a **private key** with a defined signature scheme. A verifier uses
the corresponding **public key**, the message, and the signature. Verification
checks that the signature is valid for that message under that key; it does not
decrypt the document.

For example, RSA-PSS combines hashing and an encoding scheme with RSA private
and public operations. Other schemes, such as Ed25519, have their own construction;
the phrase “encrypting a hash with a private key” is not a general definition.

A valid signature establishes a relationship to a key. Trusting the identity
behind that key requires an authenticated key-distribution mechanism. Compromised
keys, signing services, or endpoints can undermine that trust. Legal effect
depends on applicable law and how the signature and identity are established.

## Certificates and HTTPS

An X.509 certificate binds a public key to names or other identity information,
signed by an issuer. A typical HTTPS chain contains a leaf certificate and one
or more intermediates leading to a root trusted by the client.

A client must validate the chain and hostname, validity dates, permitted usage,
and applicable revocation policy. The server must also prove possession of the
corresponding private key during authentication.

A valid certificate for a domain does not establish that its content is honest.
A phishing site can have a valid certificate for its own domain.

## Operating certificates

Automate issuance and renewal where practical, monitor failures and expiry,
restrict private-key access, and replace compromised keys and certificates.
Public CAs such as Let's Encrypt provide certificates through automated workflows.
Private PKI can serve internal identities with a separately managed trust store.

See [PKI and TLS](../basics/pki.md) and [RSA](rsa.md).

## Sources

- [RFC 5280: X.509 certificate and CRL profile](https://www.rfc-editor.org/rfc/rfc5280.html)
- [cryptography RSA signing and verification](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
- [Let's Encrypt: how it works](https://letsencrypt.org/how-it-works/)
