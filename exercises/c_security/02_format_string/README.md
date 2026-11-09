# 02 — Interpreting input as a printf format

[All C security exercises](../README.md)

**Weakness:** [CWE-134](https://cwe.mitre.org/data/definitions/134.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

`printf(argv[1])` lets the caller supply formatting instructions. `%%`
changes the output even without extra arguments. Conversions such as `%p`
would try to consume arguments that the program never supplied, causing
undefined behavior that may expose process data or crash the program.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
./exercises/c_security/build/02_format_string/vulnerable 'hello %%'
./exercises/c_security/build/02_format_string/fixed 'hello %%'
./exercises/c_security/build/02_format_string/fixed 'hello %p'
```

The vulnerable program prints `hello %`; the fixed program prints the
literal `hello %%`. It also prints `hello %p` literally. The `%%` example
demonstrates interpretation without relying on a missing variadic argument
or claiming that a particular address can be leaked.

## Fix

Keep the format string constant: `printf("%s\n", argv[1])`. The input is
supplied only as the string argument, so percent sequences inside it are data.

## Check the patch

Check plain text, `%%`, `%p`, and `%n` against the fixed version. Each must
be printed literally. Compile with `-Wformat-security` to identify the unsafe
call in the vulnerable source.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux printf manual: format conversions and untrusted formats](https://man7.org/linux/man-pages/man3/printf.3.html).
