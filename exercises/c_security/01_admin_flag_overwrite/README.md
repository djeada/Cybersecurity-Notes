# 01 — Changing an application admin flag

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-787](https://cwe.mitre.org/data/definitions/787.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker supplies the username in `argv[1]`, including its length and
bytes. The objective is to change `account.is_admin` without an authentication
check. The victim's mistake is trusting that the username fits eight bytes.

## How the attack works

1. The program initializes an account with `is_admin = 0`.
2. `strcpy()` copies the entire input plus its NUL terminator into `username[8]`.
3. On a common Linux ABI, `is_admin` starts at offset 8. Nine `A` bytes write
   past the username into that integer; the terminating NUL lands at offset 9.
4. The program evaluates the corrupted value with `account.is_admin != 0` and
   prints `admin=1`.

For a little-endian, four-byte `int` at offset 8, the relevant bytes are:

| Offset | Intended storage | After nine `A` bytes and the NUL |
| --- | --- | --- |
| 0–7 | Username | Eight `0x41` bytes |
| 8 | First byte of `is_admin` | `0x41` |
| 9 | Second byte of `is_admin` | `0x00`, the input terminator |
| 10–11 | Remaining integer bytes | `0x00 0x00` from initialization |

That integer becomes 65, which is true. The printed `1` is a boolean result,
not necessarily the raw value stored in the integer.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all asan
LAB_BIN=./exercises/c_security/build/01_admin_flag_overwrite
"$LAB_BIN/vulnerable" Alice
LAB_PAYLOAD=$(python3 -c 'print("A" * 9)')
"$LAB_BIN/vulnerable" "$LAB_PAYLOAD"
"$LAB_BIN/fixed" "$LAB_PAYLOAD"
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" Alice

# A larger input crosses the whole stack object, for sanitizer evidence.
./exercises/c_security/build-asan/01_admin_flag_overwrite/vulnerable "$(python3 -c 'print("A" * 64)')"
```

On the layout described above, the first two vulnerable runs print
`admin=0` and `admin=1`. The fixed program prints
`rejected: username too long`, exits 1, and still prints `admin=0` for `Alice`.
The last command should report `stack-buffer-overflow`.

A small overwrite inside a struct can escape AddressSanitizer because it
stays within the enclosing object. C does not guarantee the result of this
out-of-bounds copy; use the debugger below to check your compiler's actual
layout rather than treating the offset table as a portable ABI guarantee.

## Inspect the overwritten variable with GDB

This optional command stops just after the copy in the current source and
inspects the victim's state. GDB is an observer here, not the attack payload.

```sh
gdb -q -batch \
  -ex 'set disable-randomization off' \
  -ex 'break 01_admin_flag_overwrite/vulnerable.c:18' \
  -ex 'run AAAAAAAAA' \
  -ex 'print (char *)&account.is_admin - (char *)&account' \
  -ex 'print account.is_admin' \
  -ex 'x/12bx &account' \
  ./exercises/c_security/build/01_admin_flag_overwrite/vulnerable
```

On the ABI above, the first two expressions produce 8 and 65. This explains
exactly which variable changed instead of inferring it from a crash.

## What the attacker gains

**Demonstrated:** corruption of one application variable, making its toy
admin decision true. This program only prints that decision; it has no
protected admin operation to invoke.

The process's Linux UID, filesystem permissions, and ability to execute
commands do not change. This is not a root shell. In a larger application,
such a flag could authorize operations if later code trusted it. Turning a
different overwrite into instruction-pointer control would require a separate
exploit involving a reachable target and the relevant memory layout and
mitigations; this command does not demonstrate that.

## Why the patch stops this attack

`fixed.c` checks `length >= sizeof account.username` before copying.
Rejecting equality reserves space for the terminator. Copying exactly
`length + 1` checked bytes cannot reach the admin flag.

## Verify the result

Lengths 0 and 7 fit. Lengths 8 and 9 must be rejected. With eight `A`
characters the vulnerable terminator may overwrite a flag byte with zero,
leaving `admin=0`; an unchanged output does not prove that no overflow occurred.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
