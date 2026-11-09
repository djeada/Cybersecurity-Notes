# 15 — Following a symlink when writing a report

[All C security exercises](../README.md)

**Weakness:** [CWE-59](https://cwe.mitre.org/data/definitions/59.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

The program writes a predictable `scratch/report.tmp` path with
`fopen(..., "w")`. If someone pre-creates that name as a symlink, opening it
follows the link and truncates its target. The attacker controls the pathname
while the writer supplies permission to modify the target.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
BIN="$(pwd)/exercises/c_security/build/15_temp_file_symlink"
WORK="$(mktemp -d)"
(
  cd "$WORK" || exit 1
  mkdir scratch
  printf 'ORIGINAL\n' > victim.txt
  ln -s ../victim.txt scratch/report.tmp
  "$BIN/vulnerable"
  cat victim.txt
  printf 'ORIGINAL\n' > victim.txt
  "$BIN/fixed"
  cat victim.txt
  rm scratch/report.tmp
  "$BIN/fixed"
  cat scratch/report.tmp
)
rm -rf -- "$WORK"
```

The vulnerable version changes the dummy victim file to `REPORT`.
With the symlink still present, the fixed version fails and preserves
`ORIGINAL`. After removing the link, the fixed version creates a fresh report
containing `REPORT`. All file changes remain in the temporary directory.

## Fix

Open the trusted directory and create the single report name using
`openat()` with `O_CREAT | O_EXCL | O_NOFOLLOW`. Creation fails atomically if
any entry already occupies the name, including a regular file or symlink.
Mode `0600` grants no group or other-user permissions. The open descriptor
then identifies the file to write without resolving its name again.

The working directory and initial `scratch` directory must be trusted;
these flags protect the final filename, not a hostile directory hierarchy.
The fixed exercise deliberately fails on an existing report instead of
overwriting it, and an error may leave a partial newly created report.

## Check the patch

Check an existing symlink, a fresh path, and an existing regular file.
The fixed version must preserve existing content and grant no group or
other-user permissions to a new report.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux open/openat manual: O_CREAT, O_EXCL, and O_NOFOLLOW](https://man7.org/linux/man-pages/man2/open.2.html).
