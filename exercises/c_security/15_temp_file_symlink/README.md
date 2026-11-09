# 15 — Making the victim overwrite a chosen file

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-59](https://cwe.mitre.org/data/definitions/59.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker can create an entry named `scratch/report.tmp` before the
victim writes its report. The objective is to redirect the victim's write
to a chosen file. The attacker chooses the target path through a symlink;
the victim must already have permission to open and truncate that target.
The demonstration uses only a temporary dummy `victim.txt`.

## How the attack works

1. The attacker creates `scratch/report.tmp -> ../victim.txt`.
2. The victim later calls `fopen("scratch/report.tmp", "w")`.
3. Path resolution follows the symlink. Its relative target is resolved from
   `scratch/`, so `../victim.txt` names the file in the lab directory.
4. Opening in mode `w` truncates the target. The victim writes its fixed
   `REPORT` line, destroying the previous `ORIGINAL` contents.

The attacker does not have to win a tightly timed race in this exercise:
planting the predictable name before the victim starts is sufficient.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all
LAB_BIN="$(pwd)/exercises/c_security/build/15_temp_file_symlink"
LAB_WORK="$(mktemp -d)"
(
  cd "$LAB_WORK" || exit 1
  # Instructor setup: a directory and a disposable target file.
  mkdir scratch
  printf 'ORIGINAL\n' > victim.txt
  # Attacker: plant the report name before the victim opens it.
  ln -s ../victim.txt scratch/report.tmp
  # Victim: write the report; observe which file changes.
  "$LAB_BIN/vulnerable"
  cat victim.txt
  # Instructor: reset the dummy target, keeping the malicious symlink.
  printf 'ORIGINAL\n' > victim.txt
  "$LAB_BIN/fixed"
  printf 'fixed rejection exit=%s\n' "$?"
  cat victim.txt
  # The fixed writer can still create a genuinely new report.
  rm scratch/report.tmp
  "$LAB_BIN/fixed"
  cat scratch/report.tmp
)
rm -rf -- "$LAB_WORK"
```

The vulnerable run changes the target, so its first `cat` prints
`REPORT`. With the planted symlink still present, the fixed run reports an
`openat` error, exits 1, and leaves the target as `ORIGINAL`. After the link
is removed, the fixed writer creates a report whose contents are `REPORT`.
Both the planted link and its dummy target stay inside the temporary lab.

## What the attacker gains

**Demonstrated:** a write to an attacker-chosen path, using the victim's
permission, with attacker-uncontrolled contents: exactly `REPORT` plus a
newline. This is a destructive file overwrite, not an arbitrary-content
write, a read of the target, or command execution.

Both roles run as your account, so the lab does not demonstrate crossing a
real Unix permission boundary. The security concern in a larger application
is redirecting a more trusted writer toward a file its caller cannot modify
directly. Success still requires the writer's existing access; a symlink
does not override an OS denial. No privilege escalation is established here.

## Why the patch stops this attack

Open the intended directory and use `openat()` with
`O_CREAT | O_EXCL | O_NOFOLLOW`. The creation atomically fails if any entry
already occupies the report name, including a symlink or a regular file.
Write using the returned descriptor, with no later pathname resolution.
Mode `0600` grants no group or other-user permissions, subject to the umask.

The initial directory path must resolve to the intended directory; these
flags protect the final report entry, not hostile replacements of its parent
components. The fixed exercise intentionally refuses to replace an existing
report and can leave a partial new report after an I/O failure.

## Verify the result

Check a planted symlink, an existing regular report, and a fresh name.
The fixed version must preserve both existing targets and create the fresh
file without group or other-user permissions. Removing `scratch/report.tmp`
in the walkthrough removes the symlink itself, not its target.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux open/openat manual: exclusive creation and symlink behavior](https://man7.org/linux/man-pages/man2/open.2.html).
