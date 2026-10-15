# Securing Web Browsers

A browser processes untrusted content and often holds authenticated sessions.
Keep its software, extensions, and configuration under active maintenance.

## Updates and configuration

- Use a supported browser and keep automatic security updates enabled. Managed
  deployments can stage updates briefly for testing, with a defined rollout
  deadline and an emergency patch path.
- Remove unused extensions and install necessary ones from trusted sources.
  Review their permissions: an extension able to read every page may access
  sensitive content.
- Disable obsolete components such as Flash and ActiveX rather than treating
  them as features to retain. Keep endpoint protection and browser sandboxing on.
- Use organization-managed settings where appropriate. Do not ignore certificate
  errors or install unknown root certificates to make warnings disappear.

## Accounts, sessions, and data

- Use unique passwords stored in a maintained password manager. A browser's
  password manager can be appropriate when the device and account are protected.
- Prefer phishing-resistant MFA, such as appropriately configured passkeys or
  security keys, for important accounts.
- Use separate browser profiles for personal work, administration, and security
  labs. Profile separation is useful organization, not strong isolation from
  malicious code running as the same operating-system user.
- Review site permissions for camera, microphone, location, notifications, and
  downloads. Clear unneeded sessions on shared devices and avoid saving passwords
  there.
- Prefer HTTPS. Encryption protects transport; a phishing site can also have a
  valid certificate.

## Privacy limits

Private browsing mainly reduces local persistence of history and cookies after
the session. It does not hide activity from websites, employers, or network
providers, and downloaded files can remain on disk.

VPNs change who can observe parts of a network connection; they do not make a
compromised browser safe or guarantee anonymity. A virtual machine adds an
isolation boundary but still needs updates and careful sharing settings.

See [anonymous browsing](anonymous_browsing.md),
[PKI and TLS](pki.md), and [web application security](web_application_security.md).

## Sources

- [Mozilla: update Firefox](https://support.mozilla.org/en-US/kb/update-firefox-latest-release)
- [Chrome Safety Center](https://safety.google/chrome/)
- [Mozilla: private browsing limits](https://support.mozilla.org/en-US/kb/common-myths-about-private-browsing)
