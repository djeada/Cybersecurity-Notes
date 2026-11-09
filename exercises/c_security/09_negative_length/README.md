# 09 — Making a negative length pass an upper-bound check

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-195](https://cwe.mitre.org/data/definitions/195.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the text parsed as a copy length. The source
bytes are the program's fixed `example` buffer. The objective is to pass a
check written for a signed number and then trigger a huge unsigned copy.

## How the attack works

1. `atoi("-1")` returns the signed integer -1.
2. `if (length > 32)` does not reject it: -1 is smaller than 32.
3. Converting -1 to unsigned `size_t` produces `SIZE_MAX`. On 64-bit Linux
   that is 18,446,744,073,709,551,615.
4. `memcpy(output, source, (size_t)length)` receives that enormous length
   even though both arrays have only 32 bytes. The invalid range affects
   the source and destination, rather than selecting a single useful byte.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/09_negative_length
python3 -c 'import ctypes; print("size_t(-1)=", ctypes.c_size_t(-1).value)'
"$LAB_BIN/vulnerable" -1
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" -1
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" 7
```

The Python command displays the conversion on your platform. The
vulnerable run normally reports `negative-size-param: (size=-1)` from
AddressSanitizer's copy interceptor, which recognizes the huge size. The
patched run prints `rejected: invalid length`, exits 1, and prints `example`
for the valid length 7. Other runtimes can diagnose the invalid copy differently.

## What the attacker gains

**Demonstrated:** a validation bypass that supplies an invalid size to a
memory operation, followed by sanitizer termination. It does not copy a
chosen secret to an attacker, choose destination bytes, or run a command.

Without instrumentation, this attempt can crash during invalid reads or
writes. Whether a deployed service exposes that path and loses availability
is a separate question. No controlled write target or execution chain is
implemented here, so a full-system-control claim is unsupported.

## Why the patch stops this attack

Parse with `strtol()` so conversion errors and trailing text are
detectable. Validate the complete conversion and `0 <= length <= 32` before
converting to `size_t`. A 33-byte zero-initialized destination also preserves
room for NUL termination when all 32 source bytes are copied.

## Verify the result

Lengths 0, 7, and 32 should succeed; -1 and 33 must fail. Empty text,
trailing garbage, and an out-of-range number must also fail before the copy.
Validate the signed value before conversion, not after it has become huge.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
