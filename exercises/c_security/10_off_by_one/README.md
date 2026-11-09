# 10 — Writing the seventeenth byte of a sixteen-byte array

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-193](https://cwe.mitre.org/data/definitions/193.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

This executable accepts no input. Running it triggers the bad loop
unconditionally; there is no attacker-selected index or byte. The objective
is to establish exactly where a seemingly small loop-bound error writes
outside its object.

## How the attack works

1. `buffer` contains sixteen `char` elements, indexed 0–15.
2. The loop condition is `i <= sizeof buffer`, and `sizeof buffer` is 16.
3. The body therefore runs for 0 through 16 inclusive: seventeen writes.
4. The final store is `buffer[16] = 'A'`, one byte beyond the array. The value
   and location are fixed by the program, rather than chosen by its caller.

The `volatile` array keeps the demonstration's stores observable to the
compiler. It does not make out-of-bounds accesses valid.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/10_off_by_one
"$LAB_BIN/vulnerable"
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed"
printf 'fixed exit=%s\n' "$?"
```

UBSan may first report an index or store outside the object, followed
by AddressSanitizer's `stack-buffer-overflow` for a one-byte write. The patched
version prints `done` and the status line prints `fixed exit=0`. An ordinary
build can print `done` after corrupting memory; that message is not evidence
of memory safety.

## What the attacker gains

**Demonstrated:** one fixed out-of-bounds stack write and sanitizer
termination. No named security variable is shown to change, and there is no
attacker-controlled parameter or demonstrated gain beyond triggering failure.

One-byte corruption can matter when it reaches a useful adjacent target in
another program. This example has not established such a target, a useful
byte value, or a later operation that turns corruption into access. It does
not show a shell or a change of privileges.

## Why the patch stops this attack

Change `<=` to `<`, restricting the loop to indices 0–15. The byte size
equals the element count only because this is a `char` array. For a wider
element type, use `sizeof buffer / sizeof buffer[0]` as the element count.

## Verify the result

The fixed sanitizer build should complete all sixteen valid stores and
print `done`. Count the iterations explicitly before and after the patch;
there is no special input that can repair or worsen this fixed loop.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
