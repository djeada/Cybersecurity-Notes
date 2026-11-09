# 08 — Allocating with a truncated byte count

[All C security exercises](../README.md)

**Weakness:** [CWE-197](https://cwe.mitre.org/data/definitions/197.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The vulnerable program multiplies a record count by sixteen, then casts
the result to `uint16_t` for allocation. With `4100` records, the product is
65,600 but conversion to sixteen bits leaves 64. `malloc()` receives 64 while
`memset()` still writes 65,600 bytes.

The unsigned narrowing conversion is defined; the subsequent out-of-bounds
write is undefined behavior. The immediate cause is numeric truncation,
rather than overflow of the `unsigned long` multiplication in this example.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/08_integer_truncation/vulnerable 4100
./exercises/c_security/build-asan/08_integer_truncation/fixed 4100
./exercises/c_security/build-asan/08_integer_truncation/fixed 4096
```

The vulnerable version prints `allocated=64 requested=65600` before
AddressSanitizer reports `heap-buffer-overflow`. The fixed version rejects
`4100` under its resource limit, while `4096` safely prints `allocated=65536`
without truncating the allocation size.

## Fix

Check the complete numeric conversion, reject counts outside 1–4096,
and keep byte sizes in `size_t`. Check `count > SIZE_MAX / 16` before
multiplying, then reuse the same `bytes` value for allocation and writing.
The count limit bounds resource use; the type and multiplication checks
keep the allocation consistent with the write.

## Check the patch

Check 0, 4, 4096, 4100, a negative count, trailing text, and a number too
large for `unsigned long`. Valid boundary input must retain its full byte
count; malformed or oversized input must be rejected.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux strtoul manual: conversion errors and end-pointer checking](https://man7.org/linux/man-pages/man3/strtoul.3.html).
