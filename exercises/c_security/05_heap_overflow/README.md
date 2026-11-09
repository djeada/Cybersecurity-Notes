# 05 — Copying past a heap allocation

[All C security exercises](../README.md)

**Weakness:** [CWE-122](https://cwe.mitre.org/data/definitions/122.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

`malloc(16)` reserves sixteen bytes; it does not constrain a later
`strcpy()`. A message of sixteen characters already needs seventeen bytes
including its NUL terminator. Longer input overwrites memory outside the
allocation, potentially corrupting nearby objects or allocator state.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/05_heap_overflow/vulnerable AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
./exercises/c_security/build-asan/05_heap_overflow/fixed AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
./exercises/c_security/build-asan/05_heap_overflow/fixed hello
```

AddressSanitizer reports `heap-buffer-overflow` for the vulnerable copy.
The fixed version rejects the same input and prints `hello` for a fitting
message. An ordinary uninstrumented run may appear to succeed despite the
invalid write; a crash is not required to establish the bug.

## Fix

Reject messages whose length is at least sixteen before allocation and
copying. Copy `length + 1` bytes only after that check, preserving room for
the terminator. The allocation remains owned until its final use and is
released once.

## Check the patch

Try lengths 0, 15, 16, and 30. Lengths 0 and 15 fit the allocation;
lengths 16 and 30 must fail before a copy occurs.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
