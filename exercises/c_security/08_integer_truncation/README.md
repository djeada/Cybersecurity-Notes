# 08 — Choosing a count that shrinks the allocation

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-197](https://cwe.mitre.org/data/definitions/197.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the record count, not the bytes written into the
records. The victim allows 1–10,000 records, with sixteen bytes per record.
The objective is to make the allocation size disagree with the write size
while passing that superficial count limit.

## How the attack works

1. The attacker chooses `4100`, which passes the vulnerable count check.
2. Multiplication in `unsigned long` produces `4100 * 16 = 65600`.
3. Casting that result to `uint16_t` keeps it modulo 65,536:
   `65600 % 65536 = 64`. `malloc()` therefore receives 64.
4. `memset()` uses the original, untruncated expression and writes 65,600
   `X` bytes. The last 65,536 bytes fall outside the allocation.

The narrowing conversion itself is defined. The invalid write follows from
using the reduced value for allocation and the full value for the write.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/08_integer_truncation
"$LAB_BIN/vulnerable" 4100
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" 4100
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" 4096
```

Before the invalid write, the vulnerable program prints:

```text
allocated=64 requested=65600
```

AddressSanitizer then reports `heap-buffer-overflow`, normally a write of
size 65,600. The patched program rejects `4100`, while `4096` prints
`allocated=65536` and succeeds without wrapping to zero.

## What the attacker gains

**Demonstrated:** control over the size mismatch and an out-of-bounds
heap write that aborts under instrumentation. The attacker chooses the count;
the code fixes every written byte to `X`. It does not demonstrate a chosen
address, useful object corruption, disclosure, or command execution.

In a real parser, an undersized allocation could place other objects in the
overwrite's path. A stronger claim would require identifying such an object
and showing how corrupting it changes later behavior. There is no such
target or later security decision in this example.

## Why the patch stops this attack

Parse the complete decimal input with error checks, enforce the resource
limit 1–4096, keep sizes in `size_t`, and check `count > SIZE_MAX / 16` before
multiplication. Reuse the resulting `bytes` for both allocation and writing.
The resource cap and the consistent size calculation serve different purposes;
rejecting this single payload alone is not a general arithmetic fix.

## Verify the result

Test 0, 4, 4096, 4100, a negative count, trailing text, and an overflowing
numeric conversion. The fixed code must allocate the full 65,536 bytes for
the valid boundary input 4096 and reject malformed or excessive values.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux strtoul manual](https://man7.org/linux/man-pages/man3/strtoul.3.html).
