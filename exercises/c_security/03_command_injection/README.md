# 03 — Turning a filename into a shell command

[All C security exercises](../README.md)

**Weakness:** [CWE-78](https://cwe.mitre.org/data/definitions/78.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The program builds `test -e USER_INPUT && echo EXISTS` and passes it to
`system()`. The shell parses user-controlled semicolons and comments as
command syntax. A filename argument can therefore run an additional command
with the program's privileges; the lab only prints a marker.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
./exercises/c_security/build/03_command_injection/vulnerable 'missing; echo INJECTED; #'
./exercises/c_security/build/03_command_injection/fixed 'missing; echo INJECTED; #'
```

The vulnerable output includes `INJECTED`, showing that the extra command
ran. In a fresh lab directory the fixed program prints `MISSING`: it checks
a filename containing those characters and never invokes the shell.

## Fix

Call `stat()` directly for the file-existence check. This removes the
interpreter that gave the filename command semantics. Checking the formatted
command's buffer length, as the vulnerable version already does, cannot
prevent shell injection.

## Check the patch

Test an existing filename containing spaces and a nonexistent filename.
The fixed version should print `EXISTS` and `MISSING` respectively. The
marker must never run, regardless of the filename's metacharacters.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
