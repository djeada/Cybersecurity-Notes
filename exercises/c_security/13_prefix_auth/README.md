# 13 — Authenticating a password prefix

[All C security exercises](../README.md)

**Weakness:** [CWE-187](https://cwe.mitre.org/data/definitions/187.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

`strncmp(input, password, strlen(input))` lets the caller choose how many
bytes are checked. `sec` matches the first three bytes of the toy password
`secret42`, so the vulnerable program grants access. An empty input chooses
a zero-byte comparison and also passes.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
./exercises/c_security/build/13_prefix_auth/vulnerable sec
./exercises/c_security/build/13_prefix_auth/fixed sec
./exercises/c_security/build/13_prefix_auth/vulnerable ''
./exercises/c_security/build/13_prefix_auth/fixed ''
./exercises/c_security/build/13_prefix_auth/fixed secret42
```

The vulnerable version prints `ACCESS GRANTED` for `sec` and the empty
input. The fixed version prints `DENIED` for both and `ACCESS GRANTED` only
for `secret42`. These programs report the decision in stdout and return 0
for either decision, so check the text rather than the exit status.

## Fix

Use `strcmp(input, password) == 0` to require equality of both complete
strings. The caller can no longer shorten the comparison. This repairs the
comparison bug in the local exercise; the hardcoded password and ordinary
string comparison remain teaching simplifications, not a complete
authentication system.

## Check the patch

Check the empty input, a correct prefix, a wrong password, the exact
password, and the correct password with an extra suffix. Only the exact
password should be accepted.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.
