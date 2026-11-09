# 14 — Reproducing a token from a guessed seed

[All C security exercises](../README.md)

**Weakness:** [CWE-338](https://cwe.mitre.org/data/definitions/338.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The vulnerable token is the first output of `rand()` after `srand()`.
Its default seed is `time(NULL)`, which an observer can estimate. The optional
seed argument makes the prediction reproducible: the same seed produces the
same sequence on the same C library, so an attacker can reproduce the token
rather than guess its printed value.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
./exercises/c_security/build/14_predictable_token/vulnerable 1234
./exercises/c_security/build/14_predictable_token/vulnerable 1234
./exercises/c_security/build/14_predictable_token/fixed
./exercises/c_security/build/14_predictable_token/fixed
```

The first two commands print identical tokens. The fixed commands each
print `token=` followed by 32 hexadecimal digits encoding sixteen random
bytes. Different outputs alone do not prove unpredictability; the relevant
change is the source of randomness. The exact vulnerable number can differ
between C library implementations.

## Fix

Obtain sixteen bytes from Linux `getrandom()` with flags 0, handling
interrupted calls, partial results, and errors. Encode all bytes as hex
without reducing their range. This removes the guessed seed and the
noncryptographic generator. The exercise does not implement token storage,
expiry, one-time use, or account binding.

## Check the patch

Confirm that the same explicit seed reproduces the vulnerable token and
that the fixed result has the expected byte encoding. Avoid a flaky test
that requires every random output to differ; collisions are possible even
with a correct random source.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux getrandom manual](https://man7.org/linux/man-pages/man2/getrandom.2.html) and [rand manual](https://man7.org/linux/man-pages/man3/rand.3.html).
