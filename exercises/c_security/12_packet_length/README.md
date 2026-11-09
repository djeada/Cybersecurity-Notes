# 12 — Making a packet parser read bytes that never arrived

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-125](https://cwe.mitre.org/data/definitions/125.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls a claimed payload length. In this CLI model the
argument supplies that field; the program constructs a four-byte synthetic
packet containing a one-byte header and the three payload bytes `cat`.
There is no listening socket. The objective is to make the parser trust the
claim rather than the number of bytes actually present.

## How the attack works

1. The attacker chooses the length 200, which fits in the header byte.
2. The received object has only three bytes after the header.
3. `memcpy(output, packet + 1, packet[0])` requests 200 bytes from that
   three-byte payload, reading 197 bytes beyond its end.
4. The destination has 256 bytes, so checking only its capacity would miss
   the error: the violated bound is on the source.

The program later prints only `claimed=... copied`, not the contents of
`output`. Reading bytes into an internal buffer and returning those bytes
to an attacker are different data-flow steps.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/12_packet_length
"$LAB_BIN/vulnerable" 3
"$LAB_BIN/vulnerable" 200
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" 200
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" 3
"$LAB_BIN/fixed" 259
```

Length 3 prints `claimed=3 copied` in the vulnerable program. Length
200 produces `stack-buffer-overflow` or `memcpy-param-overlap`, depending on
stack layout: the oversized source range may also overlap the destination.
Both diagnose an invalid copy; neither supplies a secret packet response.

The fixed version rejects 200 as `truncated packet`, accepts 3 with
`copied=3`, and rejects 259 as an invalid length byte before it can narrow
to 3. The attack against the source bound is 200; 259 separately tests the
synthetic command-line field conversion.

## What the attacker gains

**Demonstrated:** control over the amount of an invalid source read,
followed by sanitizer termination. This example does not exfiltrate memory:
the copied bytes are never printed, sent, or otherwise exposed to its caller.
It therefore does not demonstrate reading a password or taking over a host.

A similar parser that sent `output` back to a client could disclose bytes
outside the packet. Proving that stronger outcome would require following
those bytes to an actual response. That response path is absent here; a
crash report alone does not substitute for it.

## Why the patch stops this attack

Check the complete numeric conversion and header-byte range before
storing the synthetic claim. Then require the decoded claim to fit both
`sizeof packet - 1` and `sizeof output` before copying. A real receiver must
pass the actual received length and validate the header before accessing it.

## Verify the result

Lengths 0 and 3 are valid. Lengths 4 and 200 exceed received data.
Lengths 256 and 259 cannot be represented as this header field and must
be rejected without wrapping. Also test negative, empty, and malformed text.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux strtoul manual](https://man7.org/linux/man-pages/man3/strtoul.3.html).
