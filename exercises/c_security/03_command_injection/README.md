# 03 — Executing shell commands through a filename

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-78](https://cwe.mitre.org/data/definitions/78.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker supplies a purported filename. The objective is to execute
another command inside a program that is supposed to check file existence.
The injected commands below print the executing identity and create a dummy
proof file in a temporary lab directory.

## How the attack works

1. The victim interpolates the filename into
   `test -e INPUT && echo EXISTS`.
2. `system()` sends that entire string to `/bin/sh -c`.
3. The attacker includes `;` to end the file test, then supplies `id` and
   `printf`. A trailing `#` comments out the victim's appended text.
4. The shell executes the injected commands even when `missing` does not exist.

For the payload below, the shell receives:

```text
test -e missing; id; printf "CONTROLLED\n" > proof.txt; # && echo EXISTS
```

The outer single quotes in the attack command are important: they make your
terminal pass one argument to the victim. The victim's new shell then
interprets the embedded semicolons and redirection.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all
LAB_BIN="$(pwd)/exercises/c_security/build/03_command_injection"
LAB_WORK="$(mktemp -d)"
(
  cd "$LAB_WORK" || exit 1
  # Attacker: submit one filename argument containing shell syntax.
  "$LAB_BIN/vulnerable" 'missing; id; printf "CONTROLLED\n" > proof.txt; #'
  cat proof.txt
  rm proof.txt
  # Repeat the same attack through the patched victim.
  "$LAB_BIN/fixed" 'missing; id; printf "CONTROLLED\n" > proof.txt; #'
  test ! -e proof.txt && printf 'fixed: no proof file created\n'
)
rm -rf -- "$LAB_WORK"
```

The vulnerable run prints an `id` result such as
`uid=1000(student) gid=1000(student) ...`. Reading `proof.txt` prints
`CONTROLLED`. The fixed run prints `MISSING`, followed by the check's
`fixed: no proof file created`. Exact user and group names depend on the lab.

## What the attacker gains

**Demonstrated:** execution of attacker-selected shell commands and a
file write, with the permissions available to the shell launched by the
victim. `id` measures that identity directly.

In this unprivileged lab, those are your existing account permissions. No
root access or persistence is gained. A vulnerable service could expose its
own service-account access to an external caller, but this CLI is not a
network service and does not establish that deployment scenario. Host-wide
control would depend on that account's authority and other restrictions.

## Why the patch stops this attack

The patched program calls `stat()` on the filename directly. There is no
shell to reinterpret `;`, `#`, or `>`. Buffer-length validation in the original
program only prevents truncation of its command buffer; it cannot separate
shell instructions from the filename.

## Verify the result

The same payload must create no proof file through `fixed.c`. Also check
an existing filename containing spaces: it should print `EXISTS` without
treating any part of the name as a command.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux system manual: shell execution](https://man7.org/linux/man-pages/man3/system.3.html).
