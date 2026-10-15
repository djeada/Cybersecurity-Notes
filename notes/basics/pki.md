# PKI and TLS

Public Key Infrastructure (PKI) manages certificates, issuers, trust anchors,
and key lifecycles. An X.509 certificate binds a public key to an identity or
name; it does not by itself make a service trustworthy.

## Certificate validation

A client builds a chain from a leaf certificate through intermediate issuers
to a root in its configured trust store. It checks signatures, validity dates,
constraints, intended usage, the requested hostname, and applicable revocation
policy. The peer also proves possession of the private key.

- **Domain Validation (DV):** Validates control of the domain.
- **Organization Validation (OV) / Extended Validation (EV):** Include additional
  identity checks. They do not make the TLS encryption stronger.
- **Wildcard:** A name such as `*.example.com` generally matches one label,
  such as `api.example.com`, not `a.api.example.com` or the bare domain.
- **Mutual TLS (mTLS):** Both client and server authenticate with certificates.

CRLs and OCSP provide revocation information; actual checking behavior depends
on the client and policy. Automate renewal, monitor expiry and issuance failures,
protect private keys, and plan replacement after compromise.

## Formats and encoding

| Format | Description |
| --- | --- |
| DER | Binary ASN.1 encoding using Distinguished Encoding Rules |
| PEM | Base64-encoded data between labels such as `BEGIN CERTIFICATE` |
| PKCS #12 / PFX | Container that can include certificates and private keys |

BER, CER, and DER are encoding rules defined by X.690, not X.609. Filename
extensions are conventions: inspect the content and labels. A `.pem` file can
contain a certificate, key, chain, or a combination. Protect exported private keys
and any associated passwords.

## TLS

Prefer TLS 1.3 and allow properly configured TLS 1.2 when compatibility requires
it. Disable SSL, TLS 1.0, and TLS 1.1.

TLS combines peer authentication, key establishment, and symmetric authenticated
encryption. In TLS 1.3, key establishment can use ephemeral (EC)DHE or pre-shared
keys; RSA key transport was removed. An RSA certificate can still be used for
signature-based authentication. Certificate validation remains essential.

A TLS terminator decrypts traffic at its boundary. Consider protection and
authentication on the next hop rather than assuming the entire path is encrypted.

## Related protocols

- **SSH:** Authenticated remote sessions and file transfer. Verify host keys;
  public-key user authentication does not replace server authentication.
- **S/MIME:** Certificate-based email signing and encryption; encryption is a
  separate capability from signing.
- **IPsec:** Protects IP traffic. ESP can provide confidentiality and integrity;
  AH provides integrity and authentication without encryption. Tunnel mode
  encapsulates an inner IP packet; the outer header remains visible.
- **L2TP:** Tunneling without encryption on its own; often paired with IPsec.
- **PPTP:** Legacy VPN technology with serious security weaknesses; avoid new use.

See [digital signatures](../cryptography/signature_and_certificates.md),
[encryption](../cryptography/encryption.md), and [VPNs](vpn.md).

## Sources

- [RFC 5280: X.509 certificate profile](https://www.rfc-editor.org/rfc/rfc5280.html)
- [RFC 9325: TLS deployment recommendations](https://www.rfc-editor.org/rfc/rfc9325.html)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 4301: IPsec architecture](https://www.rfc-editor.org/rfc/rfc4301.html)
