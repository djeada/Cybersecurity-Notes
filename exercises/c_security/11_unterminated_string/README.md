# 11 — Reading beyond a username while printing it

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-170](https://cwe.mitre.org/data/definitions/170.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the username text. The objective is to fill all
eight destination bytes without a NUL terminator, then make the victim's
string printer continue reading beyond that array. The attacker controls the
eight initial bytes, not the memory that happens to follow them.

## How the attack works

1. The attacker submits exactly `ABCDEFGH`.
2. `strncpy(username, input, sizeof username)` copies eight non-NUL bytes.
   Unlike a string operation that reserves space, it adds no terminator
   when the input fills the destination.
3. `printf("user=%s\n", username)` uses a fixed format, but `%s` still needs
   a properly terminated string.
4. The printer reads `A` through `H`, then searches outside `username` for
   a NUL. A normal execution could expose some of those extra bytes on stdout
   or fault while reading them.

The bounded copy itself fits; the later unbounded string read is the
failing operation. Format-string injection is not needed.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security asan
LAB_BIN=./exercises/c_security/build-asan/11_unterminated_string
"$LAB_BIN/vulnerable" ABCDEFG
"$LAB_BIN/vulnerable" ABCDEFGH
printf 'vulnerable exit=%s\n' "$?"
"$LAB_BIN/fixed" ABCDEFGH
printf 'fixed rejection exit=%s\n' "$?"
"$LAB_BIN/fixed" ABCDEFG
```

Seven characters produce `user=ABCDEFG`. Eight characters produce a
`stack-buffer-overflow` read report from AddressSanitizer's string/printf
handling. The fixed program rejects eight characters with exit 1 and still
prints the valid seven-character value.

The sanitizer can stop the invalid read before ordinary output is flushed.
Its diagnostic is evidence of an over-read, not a transcript of a leaked
secret. Exact read sizes and stack traces vary with the runtime.

## What the attacker gains

**Demonstrated:** an attacker-triggered out-of-bounds read during a
string-output operation, ending in sanitizer termination. In an ordinary
run, bytes after the username may be printed, but their identities and
length depend on memory layout and the next NUL. No specific neighboring
secret is deliberately placed there, so this walkthrough does not claim
reliable disclosure of a named variable.

There is no out-of-bounds write in this copy and no command interpreter in
this path. A stronger disclosure claim would require showing sensitive
bytes reaching the caller. Exercise 02 provides a controlled, observable
example of reading a specific dummy internal value.

## Why the patch stops this attack

Reject input with `length >= sizeof username`, then copy the checked
`length + 1` bytes including the NUL. Choosing rejection also avoids silently
turning different long usernames into the same truncated name. A fixed
`printf` format alone would not fix this termination bug.

## Verify the result

Check empty, seven-character, eight-character, and longer usernames.
Every accepted value must contain a NUL inside the eight-byte array; every
value that cannot fit must be rejected before copying.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux strncpy manual: nonstring copies and missing terminators](https://man7.org/linux/man-pages/man3/strncpy.3.html).
