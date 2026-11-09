# 05 — Writing beyond a heap message buffer

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-122](https://cwe.mitre.org/data/definitions/122.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker chooses the message bytes and length in `argv[1]`. The
objective of this demonstration is to make the victim write outside a
sixteen-byte allocation. The example does not contain a neighboring role
flag, callback, or other chosen target that could demonstrate a takeover.

## How the attack works

1. The victim reserves sixteen bytes with `malloc(16)`.
2. The attacker supplies thirty `A` characters.
3. `strcpy()` writes those thirty bytes plus a NUL, for 31 bytes total.
4. Only offsets 0–15 belong to the allocation; fifteen bytes are written
   beyond it. Allocation size does not automatically limit a later copy.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/05_heap_overflow
LAB_PAYLOAD=$(python3 -c 'print("A" * 30)')
"$LAB_BIN/vulnerable" "$LAB_PAYLOAD"
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" "$LAB_PAYLOAD"
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" hello
```

The vulnerable run reports `heap-buffer-overflow` for a write, normally
including a `WRITE of size 31` report from `strcpy`. Its sanitizer process
exits nonzero. The fixed run rejects the same message with exit 1, and
prints `hello` for the valid input. Exact stack traces vary by compiler.

## What the attacker gains

**Demonstrated:** an attacker-controlled out-of-bounds heap write and
termination of the instrumented process. The payload controls the copied
bytes, but this example does not show corruption of a chosen variable,
a useful arbitrary-address write, or execution of attacker code.

An ordinary build might crash, corrupt nearby memory, or appear to work.
If such an input crashed a running service it could deny service; this CLI
and its AddressSanitizer abort alone do not establish a remote DoS or system
takeover. A stronger exploit would need a useful adjacent object and a
demonstrated path from corrupting it to an unauthorized action.

## Why the patch stops this attack

Reject `length >= 16` before copying, then copy exactly `length + 1`
bytes. Fifteen characters plus the terminator fit; sixteen characters do
not. The patch removes the out-of-bounds write rather than suppressing the
allocator or sanitizer error.

## Verify the result

Check lengths 0, 15, 16, and 30. The first two must work; the last two
must be rejected. Confirm that the fixed binary has no sanitizer report,
including when it processes the same attack payload.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
