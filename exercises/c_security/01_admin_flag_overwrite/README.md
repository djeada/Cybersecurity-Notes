# 01 — Overwriting an adjacent admin flag

[All C security exercises](../README.md)

**Weakness:** [CWE-787](https://cwe.mitre.org/data/definitions/787.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The account stores an eight-byte username next to an authorization flag.
`strcpy(account.username, argv[1])` has no destination-size argument. A long
username writes beyond the array and can corrupt the flag used by the later
authorization decision. Input data has crossed into security state.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all asan
./exercises/c_security/build/01_admin_flag_overwrite/vulnerable AAAAAAAAA
./exercises/c_security/build/01_admin_flag_overwrite/fixed AAAAAAAAA
./exercises/c_security/build/01_admin_flag_overwrite/fixed Alice
./exercises/c_security/build-asan/01_admin_flag_overwrite/vulnerable "$(python3 -c 'print("A" * 64)')"
```

On a typical Linux layout, nine `A` characters change the vulnerable
program's output to `admin=1`. The fixed program rejects that username and
prints `admin=0` for `Alice`.

The overwrite is undefined behavior: padding, optimization, and the compiler
can change the visible result. An overwrite confined to members of the same
struct may escape AddressSanitizer. The separate 64-character input crosses
the whole stack object and should produce a `stack-buffer-overflow` report.
Neither observation demonstrates arbitrary code execution.

## Fix

Measure the input before copying. Reject `length >= sizeof account.username`
so that the terminating NUL also fits, then copy exactly `length + 1` bytes
with `memcpy`. The copy can no longer reach `is_admin`.

## Check the patch

Try usernames of lengths 0, 7, 8, and 9. The first two fit; the last two
must be rejected. Inspect `offsetof(struct Account, is_admin)` in a debugger
to relate your platform's member layout to the vulnerable result.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
