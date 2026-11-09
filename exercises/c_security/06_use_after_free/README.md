# 06 — Reading a contact after it has been freed

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-416](https://cwe.mitre.org/data/definitions/416.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The caller supplies a contact name. Any name, including a short valid
one, reaches the faulty lifetime path. The input does not need to be long:
`snprintf()` bounds the initial name copy. The demonstration's objective is
to locate a read of storage the program no longer owns.

## How the attack works

1. `malloc()` creates a `struct Contact`, and the program stores the name.
2. `free(contact)` ends that allocation's lifetime. It does not erase or
   invalidate every copy of its numeric address.
3. The program still evaluates `contact->name` and calls `puts()` on it.
4. The allocator may already have changed the bytes, and the program has no
   right to read them even if the old name appears to survive.

The missing condition is an ownership/lifetime condition, not a missing
length check. A longer buffer would leave this bug intact.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/06_use_after_free
"$LAB_BIN/vulnerable" Ada
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" Ada
printf 'fixed exit=%s\n' "$?"
```

The vulnerable run reports `heap-use-after-free`, with a read and stack
traces for the allocation, the free, and the later use. The patched run prints
`Ada` and exits 0. Use those three traces to reconstruct the object's lifetime;
addresses and the reported read size can differ between runtimes.

## What the attacker gains

**Demonstrated:** an invalid read after free and termination by the
sanitizer. This program does not allocate a replacement object after freeing
the contact, so the caller has no demonstrated way to control reused storage.
A normal run might print stale bytes or allocator metadata; no particular
secret or attacker-chosen replacement contact is reliably disclosed here.

A stronger use-after-free exploit would need influence over the reuse of the
allocation and a later operation that uses the replacement bytes for an
unauthorized effect. There is no such reuse workflow, callback, write, or
command-execution path in this toy program.

## Why the patch stops this attack

Read and print the contact before freeing it. Release it once, after its
final use, and clear the owner's pointer. Clearing only one pointer would not
repair stale aliases; the actual fix here is ending all uses before `free()`.

## Verify the result

Repeat `Ada` through both versions under AddressSanitizer. The fixed
version must print the name successfully with no diagnostic. Explain why
changing the name's length cannot repair the vulnerable ordering.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
