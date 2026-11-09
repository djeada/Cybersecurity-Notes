# 07 — Triggering duplicate cleanup of one allocation

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-415](https://cwe.mitre.org/data/definitions/415.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

This program accepts no arguments. There is no malicious string to
construct: simply reaching its cleanup path triggers the bug. This is an
unconditional bug demonstration, not an implemented scenario where an
attacker chooses which live object is freed.

## How the attack works

1. The program allocates one integer and stores 42 in it.
2. The first `free(task)` legitimately releases that allocation.
3. The pointer variable still holds its old address, but no longer owns a
   live allocation.
4. The second `free(task)` submits the same allocation to the allocator again.
   That is undefined behavior. Runtime checks can detect it and abort.

“The pointer value is non-NULL” is not evidence that it is still valid to
free. Ownership ended at the first release.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/07_double_free
"$LAB_BIN/vulnerable"
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed"
printf 'fixed exit=%s\n' "$?"
```

The vulnerable run reports an attempted `double-free`, with the first
and second release sites. The fixed program has no ordinary output and the
status line prints `fixed exit=0`. Some ordinary allocators also diagnose
this case; their exact message is implementation-dependent.

## What the attacker gains

**Demonstrated:** process termination when the duplicate release is
detected. No attacker-selected data, chosen address, or unauthorized write
is obtained. Because there is no external request interface, calling this
executable is only a way to trigger and inspect the faulty path.

Real double-free exploits depend on the allocator, its checks, and subsequent
allocation/use operations. This program supplies no allocation sequence that
turns the error into two controlled owners or instruction-pointer control.
Calling the bug “a root exploit” would claim an effect that is not shown.

## Why the patch stops this attack

Use one owning cleanup path, with one release. The fixed implementation
removes the second `free()` and then clears `task`. `free(NULL)` is permitted,
but that fact does not make freeing a non-NULL stale alias valid.

## Verify the result

The fixed binary must exit 0 under the sanitizer. When reviewing a larger
function, trace normal and error returns to ensure a successful allocation
reaches exactly one cleanup operation.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
