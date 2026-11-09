# 09 — Converting a negative length to size_t

[All C security exercises](../README.md)

**Weakness:** [CWE-195](https://cwe.mitre.org/data/definitions/195.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The guard rejects only `length > 32`, so `-1` passes. Converting that
signed value to `size_t` produces `SIZE_MAX`, and `memcpy()` attempts an
enormous copy between two small arrays. `atoi()` also makes malformed input
difficult to distinguish from a valid zero.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/09_negative_length/vulnerable -1
./exercises/c_security/build-asan/09_negative_length/fixed -1
./exercises/c_security/build-asan/09_negative_length/fixed 7
```

AddressSanitizer diagnoses `negative-size-param` for the vulnerable copy.
The fixed version rejects `-1` before copying and prints `example` for `7`.
Other toolchains can report the invalid copy differently.

## Fix

Use `strtol()` with `errno` and an end pointer. Reject an empty conversion,
trailing text, range errors, and lengths outside 0–32 before converting to
`size_t`. A 33-byte zero-initialized destination leaves room for termination
even when all 32 source bytes are copied.

## Check the patch

Check -1, 0, 7, 32, 33, nonnumeric input, and numeric input with trailing
text. Only complete conversions in the allowed range should reach `memcpy()`.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
