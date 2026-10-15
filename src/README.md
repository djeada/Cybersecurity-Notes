# Python Examples

[Repository home](../README.md) · [Cryptography notes](../notes/README.md#cryptography)

These are small learning utilities, not a packaged security product. Use Python
3.10 or newer. Run commands below from the repository root.

## Dependencies

The hash and textbook RSA examples use only the standard library. Utilities that
make HTTP requests use `requests`; the domain lookup uses `python-whois`:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The latency utility also needs the system `ping` command. The saved Wi-Fi utility
requires Windows `netsh` and parses English output.

## Utility index

| File | Purpose and important behavior |
| --- | --- |
| [file_hash_checker.py](file_hash_checker.py) | Hash a file or compare it with a trusted digest; returns nonzero on mismatch or invalid input |
| [rsa.py](rsa.py) | Demonstrate textbook signing with the private exponent and public verification; deliberately insecure tiny keys |
| [hostname_to_ip.py](hostname_to_ip.py) | Resolve a hostname to an IPv4 address |
| [display_ip.py](display_ip.py) | Query ipinfo.io; its optional argument is a URL whose response supplies an IP |
| [domain_whois_retriever.py](domain_whois_retriever.py) | Query WHOIS registration data; fields depend on registry and access policy |
| [mac_info_retriever.py](mac_info_retriever.py) | Send a MAC address to api.macvendors.com for vendor lookup |
| [ping_latency_checker.py](ping_latency_checker.py) | Run the system ping command; defaults to 8.8.8.8 |
| [port_scanner.py](port_scanner.py) | Make TCP connections to common ports and send a short probe; defaults to localhost |
| [ssl_certificate_checker.py](ssl_certificate_checker.py) | Fetch a TLS certificate using default trust and hostname validation |
| [website_status_checker.py](website_status_checker.py) | Make an HTTP request and show status and elapsed time; status alone does not establish application health |
| [local_wifi_password.py](local_wifi_password.py) | Print saved Windows Wi-Fi credentials accessible to the current user; output contains secrets |

Network utilities contact external services or the supplied target when run.
Use your own systems or authorized lab targets and consider what data a lookup
sends to its service. Do not commit saved credentials or sensitive outputs.

## File integrity examples

```bash
python src/file_hash_checker.py README.md
python src/file_hash_checker.py README.md --algorithm sha512
python src/file_hash_checker.py README.md <trusted-sha256-digest>
```

Replace the placeholder with a digest obtained through a trusted channel. Exit
status is `0` for a successful hash or a match, `1` for a mismatch, and `2` for
invalid input or an unreadable file.

## RSA arithmetic example

```bash
python src/rsa.py
```

This demonstrates the mathematics only. It has no secure padding, side-channel
protections, or production key generation. Use maintained cryptographic
implementations and [appropriate schemes](../notes/cryptography/rsa.md#practical-rsa)
in applications.

## Offline checks

```bash
python -m unittest discover -s tests -v
```

The regression tests exercise local files and arithmetic and do not make network
requests or retrieve credentials.
