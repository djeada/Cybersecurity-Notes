# CVE-2026-111497 — Brotli Decoder Out-of-Bounds Write

[Repository home](../README.md) · [CVE reports index](README.md)

An application that decompresses attacker-controlled Brotli data can reach an
out-of-bounds write in the native decoder. The flaw can crash the process,
expose process memory, or potentially allow code execution. Node.js credits
Khai Tran and Sylvie Mayer of OpenAI Codex Security with reporting the issue.
CISA added it to KEV on 27 October 2026.

## How it works

A streaming decoder has to distinguish a valid stream that needs more bytes
from one that has already violated the format. A malformed block switch was
treated as a request for more input. The decoder continued buffering incoming
bytes past the end of an eight-byte internal buffer. The fix propagates a
format error so the stream stops at the invalid transition.

The same native library is bundled in multiple runtimes. An HTTP client can
reach it by decoding an untrusted response, and a service can reach it by
decompressing an upload or request body. Check whether the application
actually decodes that input and which library copy it loads. For example,
Microsoft's .NET advisory identifies exposure where Brotli decompression is
enabled or called explicitly.

## Exposure and response

Google's CVE record covers upstream Brotli 1.0.3 through 1.2.0, with fixes
released on multiple branches. Node.js and .NET each ship their own fixes.

| Component | First fixed releases in the cited advisories |
| --- | --- |
| Upstream Brotli | `1.0.10`, `1.1.1`, and `1.2.1` on their respective branches |
| Node.js | `22.23.4`, `24.22.1`, and `26.12.1` |
| .NET stable release lines | `8.0.33`, `9.0.22`, and `10.0.14` |

Inventory OS packages and bundled copies separately. For a runtime with its
own copy, rebuild and redeploy from a patched runtime or base image, then
verify the version inside the running workload. Google assigned a CVSS 4.0
score of 9.2 to the decoder CVE. Node.js rates the issue high in its runtime
advisory.

## Study exercise

Draw two input paths for a lab HTTP client, one that decompresses a response
and one that passes the body through as bytes. Mark where untrusted input
enters native code. Then describe a decoder regression test that distinguishes
an incomplete but valid block from an invalid block switch. The former can
wait for another chunk. The latter should produce a terminal format error.

## Related notes

- [Developing secure applications](../notes/basics/developing_secure_apps.md)
- [Vulnerability management](../notes/basics/vulnerability_management.md)

## Sources

- [Google CVE record and Brotli severity](https://www.cve.org/CVERecord?id=CVE-2026-111497)
- [Google Brotli upstream releases](https://github.com/google/brotli/releases)
- [Node.js October 2026 security releases and reporter credit](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
- [Microsoft advisory for the bundled .NET decoder](https://github.com/dotnet/runtime/security/advisories/GHSA-p3jp-9v83-76w9)
- [CISA KEV addition for CVE-2026-111497](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/430af9d)
