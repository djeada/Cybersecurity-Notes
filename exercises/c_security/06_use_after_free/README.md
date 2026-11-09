# 06 — Reading a contact after its lifetime ends

[All C security exercises](../README.md)

**Weakness:** [CWE-416](https://cwe.mitre.org/data/definitions/416.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The program frees a heap-allocated contact and then passes `contact->name`
to `puts()`. The address may still look usable, but the allocation's lifetime
has ended. Reuse of that memory can make the stale reference read unrelated
data; allocator bookkeeping alone can also change what is printed.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/06_use_after_free/vulnerable Ada
./exercises/c_security/build-asan/06_use_after_free/fixed Ada
```

AddressSanitizer reports `heap-use-after-free` in the vulnerable program.
The fixed program prints `Ada` and exits successfully. The example shows an
invalid read, not a reliable way to control another allocation.

## Fix

Move the read before `free(contact)`. Release the allocation only after
its last use, then clear the owning pointer. Setting one pointer to `NULL`
would not repair other aliases; the essential fix is the order of use and
destruction.

## Check the patch

Run the same name through both versions under AddressSanitizer. Check that
the fixed version prints the name before freeing it and has no later access
through the pointer.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
