# 02 — Reading an internal value through printf

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-134](https://cwe.mitre.org/data/definitions/134.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the format text in `argv[1]`. The objective is to
make the logger print an internal value that the attacker did not supply.
This lab deliberately passes one dummy internal string as a formatting
argument so that the disclosure is reproducible without guessing addresses.

## How the attack works

1. The program holds `internal_note = "DEMO_PRIVATE_VALUE"`.
2. It calls `printf(argv[1], internal_note)`, letting untrusted text specify
   how the internal argument is used.
3. The attacker supplies `private=%s`. `%s` consumes the pointer argument and
   reads the pointed-to string until its NUL terminator.
4. The logger prints the internal value to the attacker-visible output.

The attacker never supplied `DEMO_PRIVATE_VALUE` in the command. The bug is
giving input the authority to choose formatting operations.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all
LAB_BIN=./exercises/c_security/build/02_format_string
"$LAB_BIN/vulnerable" hello
"$LAB_BIN/vulnerable" 'private=%s'
"$LAB_BIN/fixed" 'private=%s'
"$LAB_BIN/vulnerable" 'hello %%'
"$LAB_BIN/fixed" 'hello %%'
```

The disclosure and its fixed counterpart are exactly:

```text
private=DEMO_PRIVATE_VALUE
private=%s
```

The last pair prints `hello %` and `hello %%`, respectively. `%s` performs
the read in the vulnerable case; `%%` only changes formatting.

## What the attacker gains

**Demonstrated:** disclosure of one internal dummy string through a valid
pointer already present in the formatting arguments. The process continues;
no memory write, shell, UID change, or arbitrary code execution is shown.

This is not an arbitrary-address read: the attacker does not choose the
pointer argument. Other format-string exploits depend on available arguments,
address knowledge, and writable targets. In particular, `%n` requires an
appropriate writable integer pointer; no such target is provided by this
exercise. Extra conversions without corresponding arguments are undefined
behavior, not a reliable method for reading a named variable.

## Why the patch stops this attack

`printf("%s\n", argv[1])` fixes the format in the program. The attacker
string becomes the data argument, and the internal note is no longer passed
to the formatter. The `%s` inside the attack text is printed literally.

## Verify the result

Try `private=%s`, `hello %%`, and `test %n` against `fixed.c`. All must be
printed literally, and none may reveal `DEMO_PRIVATE_VALUE`. Keep the dummy
value synthetic; the demonstration does not need real credentials.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux printf manual: format argument interpretation](https://man7.org/linux/man-pages/man3/printf.3.html).
