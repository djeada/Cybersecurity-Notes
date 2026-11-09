# 10 — Writing one element beyond an array

[All C security exercises](../README.md)

**Weakness:** [CWE-193](https://cwe.mitre.org/data/definitions/193.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

A sixteen-element array has valid indices 0 through 15. The vulnerable
loop uses `i <= sizeof buffer`, so it also writes index 16. A single extra
byte can corrupt adjacent state; the example's invalid store occurs on every
run and does not require a special input.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/10_off_by_one/vulnerable
./exercises/c_security/build-asan/10_off_by_one/fixed
```

The vulnerable loop produces an out-of-bounds diagnostic and an
AddressSanitizer `stack-buffer-overflow`. The fixed version prints `done`
without a sanitizer error. The `volatile` array keeps the demonstration's
stores observable to the compiler.

## Fix

Use `i < sizeof buffer`. For this `char` array, the byte size equals the
element count. With wider element types, calculate the element count as
`sizeof buffer / sizeof buffer[0]` instead.

## Check the patch

Run both versions under sanitizers and inspect their loop bounds. If the
array size changes, the fixed loop should still visit exactly its valid
elements.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
