# 07 — Releasing one allocation twice

[All C security exercises](../README.md)

**Weakness:** [CWE-415](https://cwe.mitre.org/data/definitions/415.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

Two cleanup operations call `free(task)` on the same allocation. After the
first call the pointer is no longer an owner. Passing it to `free()` again
violates the allocator contract, causing undefined behavior that can abort
the process or corrupt allocator state.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/07_double_free/vulnerable
./exercises/c_security/build-asan/07_double_free/fixed
```

The vulnerable version needs no input: AddressSanitizer reports an
attempted `double-free`. The fixed version exits with status 0 and no output.
Modern allocators may also abort an uninstrumented run; that does not make
the duplicate release valid.

## Fix

Keep one owning cleanup path with exactly one `free(task)`. Clearing the
owner afterward records that it no longer owns an allocation. This would
not make a second stale alias safe; ownership must remain unambiguous.

## Check the patch

Run the fixed version under AddressSanitizer. If you add early-return
paths, ensure each successful allocation reaches exactly one cleanup path.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
