# 11 — Using an unterminated array as a string

[All C security exercises](../README.md)

**Weakness:** [CWE-170](https://cwe.mitre.org/data/definitions/170.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

`strncpy(username, input, sizeof username)` fills all eight destination
bytes when the input is eight characters or longer. It then leaves no NUL
terminator. `printf("user=%s", username)` reads past the array while searching
for one, potentially printing unrelated memory or crashing.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security asan
./exercises/c_security/build-asan/11_unterminated_string/vulnerable ABCDEFGH
./exercises/c_security/build-asan/11_unterminated_string/fixed ABCDEFGH
./exercises/c_security/build-asan/11_unterminated_string/fixed ABCDEFG
```

AddressSanitizer reports a `stack-buffer-overflow` read when the vulnerable
version formats the eight-character input. The fixed version rejects that
input and prints `user=ABCDEFG` for seven characters. The bounded copy itself
stays within the array; the later string read causes the memory error.

## Fix

Reject input that cannot fit including its terminator, then copy
`length + 1` bytes with `memcpy()`. This exercise chooses rejection rather
than silently truncating a username.

## Check the patch

Check empty, seven-character, eight-character, and longer input. Every
accepted value must have a terminator inside the destination array.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux strncpy manual: fixed-width character sequences and termination](https://man7.org/linux/man-pages/man3/strncpy.3.html).
