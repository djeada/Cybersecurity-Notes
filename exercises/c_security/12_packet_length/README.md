# 12 — Trusting a packet length beyond received data

[All C security exercises](../README.md)

**Weakness:** [CWE-125](https://cwe.mitre.org/data/definitions/125.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The toy packet contains one length byte and only three payload bytes,
`cat`. The vulnerable parser trusts the length byte and copies that many
bytes from `packet + 1`. A claimed length of 200 reads beyond the received
object even though the 256-byte destination is large enough.

In a real parser such a read can expose memory if the copied bytes are later
returned. This program only reports the count; it demonstrates the invalid
read without transmitting or printing the copied memory.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/12_packet_length/vulnerable 200
./exercises/c_security/build-asan/12_packet_length/fixed 200
./exercises/c_security/build-asan/12_packet_length/fixed 3
./exercises/c_security/build-asan/12_packet_length/fixed 259
```

AddressSanitizer reports an invalid copy: depending on stack layout, this
appears as `stack-buffer-overflow` or `memcpy-param-overlap` because the
oversized source range also reaches the destination array. The fixed version
rejects `200` as a truncated packet, prints `copied=3` for a valid payload, and
rejects `259` rather than narrowing it to 3.

## Fix

Validate the complete command-line conversion and byte range before
storing the synthetic length field. Compare the decoded claim against both
`sizeof packet - 1` and the destination capacity before copying. Checking
only the destination would still permit an out-of-bounds source read.

## Check the patch

Check lengths 0, 3, 4, 200, 256, and 259, plus malformed and negative
input. Only 0–3 payload bytes are available. In a larger parser, pass the
actual received length explicitly and validate the header before reading it.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux strtoul manual: conversion errors and end-pointer checking](https://man7.org/linux/man-pages/man3/strtoul.3.html).
