# 13 — Passing authentication without the full password

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-187](https://cwe.mitre.org/data/definitions/187.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the submitted password. The objective is to make
the victim choose its `ACCESS GRANTED` branch without submitting `secret42`.
The empty-input attack requires no knowledge of the correct password; the
`sec` example separately shows a matching prefix.

## How the attack works

1. The victim chooses the comparison length with `strlen(argv[1])`.
2. For `sec`, that is three, so `strncmp()` checks only `s`, `e`, and `c`.
   They match the beginning of `secret42`, so it returns zero.
3. For an empty string, the length is zero. `strncmp(a, b, 0)` compares no
   bytes and returns zero regardless of the stored password.
4. The code treats that zero as complete password equality and prints
   `ACCESS GRANTED`.

The caller is selecting how much evidence the authentication decision uses.
A bounded comparison is not a complete equality check when the bound itself
is supplied by the party being authenticated.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all
LAB_BIN=./exercises/c_security/build/13_prefix_auth
"$LAB_BIN/vulnerable" wrong
"$LAB_BIN/vulnerable" sec
"$LAB_BIN/vulnerable" ''
"$LAB_BIN/fixed" sec
"$LAB_BIN/fixed" ''
printf 'denied decision still returns exit=%s\n' "$?"
"$LAB_BIN/fixed" secret42
"$LAB_BIN/fixed" secret42extra
```

In command order, the decisions are:

```text
DENIED
ACCESS GRANTED
ACCESS GRANTED
DENIED
DENIED
denied decision still returns exit=0
ACCESS GRANTED
DENIED
```

Both decision branches return 0 in these toy programs. The decision text,
rather than shell exit status, is the evidence of the bypass.

## What the attacker gains

**Demonstrated:** an unauthorized successful authentication decision in
the toy program. An empty password bypasses it without even guessing a prefix.
The executable only prints a result; it does not create a session, expose
protected data, run an admin action, or grant a Linux shell.

If an application used this exact check to gate an account's operations,
the bypass could grant those application permissions. Such downstream
operations are not implemented here, and an application admin account is
not automatically the operating system's root account.

## Why the patch stops this attack

`strcmp(argv[1], password) == 0` requires equality through both strings'
terminators, including their full lengths. The attacker can no longer make
the comparison vacuously succeed with zero bytes. This repairs the comparison
logic; the hardcoded toy password remains a teaching simplification, not a
complete production authentication design.

## Verify the result

Check an empty password, a correct prefix, a wrong password, the exact
password, and the exact password with a suffix. Only the exact password may
produce `ACCESS GRANTED` in the fixed implementation.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.
