# CVE-2026-118350 — Chrome Turbolev Memory Safety

[Repository home](../README.md) · [CVE reports index](README.md)

Google's 27 October 2026 Chrome release credits OpenAI Codex Security (`amyb`)
with reporting a high-severity memory-safety flaw in Turbolev, an optimizing
compiler in the V8 JavaScript engine. Ubuntu's CVE entry describes a crafted
page leading to arbitrary code execution inside Chrome's sandbox.

## How to read the advisories

Google's release notes label the issue type confusion, which means code uses a
value as though it had a different type or memory layout. Ubuntu's CVE entry
describes a use-after-free, which means code accesses an object after its
storage has been released. The descriptions agree on the component and the
fixed build. They leave the exact sequence of operations unclear.

A browser sandbox restricts what compromised web content can do. A separate
weakness or another route across that boundary would be needed to turn the
reported in-sandbox code execution into host-level code execution. That
distinction matters when comparing a browser advisory with a server-side RCE.

## Exposure and response

Google's desktop stable rollout included `156.0.8078.73` for Linux and
`156.0.8078.73` or `.74` for Windows and macOS. Update to a current stable build
and relaunch the browser. In a managed fleet, verify the running browser version
after relaunch. For other Chromium-based browsers, use the browser vendor's
advisory to map the upstream fix to its own release numbers.

## Study exercise

Open `chrome://version` in a lab browser and compare the running build with
Google's fixed desktop builds. For a managed laptop that downloaded a fixed
build but has yet to relaunch, record which version you would use to assess
exposure and how you would verify closure. Draw the boundary between the web
page's renderer process and the operating system, and identify one action that
would require crossing it.

## Related notes

- [Browser security](../notes/basics/securing_browser.md)
- [Application isolation](../notes/basics/running_apps_securely.md)

## Sources

- [Google Chrome 156 desktop stable release and reporter credit](https://chromereleases.googleblog.com/2026/10/stable-channel-update-for-desktop_0562499947.html)
- [Ubuntu CVE entry and sandbox impact](https://ubuntu.com/security/CVE-2026-118350)
- [V8 engineering overview of Turbolev and the compiler pipeline](https://v8.dev/blog/leaving-the-sea-of-nodes)
