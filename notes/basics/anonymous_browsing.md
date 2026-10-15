# Anonymous Browsing

Privacy limits collection and disclosure of information. Anonymity aims to keep
activity from being linked to an identity. Neither is guaranteed by a single tool.

## Begin with a threat model

Identify who you want privacy from, what they can observe, and which consequences
matter. A website, network provider, employer, and compromised endpoint have
different visibility.

- Signing into an identifying account links activity to that account even through
  Tor or a VPN.
- Cookies, browser fingerprints, downloads, metadata, and repeated behaviors can
  connect sessions.
- Private browsing mainly limits local history and session persistence. It does
  not conceal activity from a network observer.
- A VPN shifts trust to its operator. Tor distributes network trust, but does not
  eliminate traffic correlation or protect a compromised endpoint.
- MAC address randomization helps against some local-network tracking. It does not
  hide an account identity or make internet activity anonymous.

## Live systems and limits

A privacy-focused live system such as Tails can reduce local traces and route
supported traffic through Tor. It cannot guarantee anonymity, defeat malicious
hardware, or erase records stored by remote services.

Avoid opening identifying accounts during an activity whose anonymity matters.
Treat unexpected files, browser changes, and optional persistence as changes to
the threat model.

See [live operating systems](live_os.md) and [browser security](securing_browser.md).

## Sources

- [Tails security warnings](https://tails.net/doc/about/warnings/index.en.html)
- [Tor Browser: staying anonymous](https://tb-manual.torproject.org/staying-anonymous/)
