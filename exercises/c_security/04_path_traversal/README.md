# 04 — Reading outside the notes directory

[All C security exercises](../README.md)

**Weakness:** [CWE-22](https://cwe.mitre.org/data/definitions/22.html) ·
**Before the patch:** [vulnerable.c](vulnerable.c) ·
**After the patch:** [fixed.c](fixed.c)

## Exploit

Prefixing input with `notes/` does not confine path resolution. Supplying
`../private.txt` makes `fopen()` resolve `notes/../private.txt`, outside the
intended directory. A symlink inside `notes/` can also lead outside it.

## Reproduce

Run these commands from the repository root in an unprivileged Linux lab.
Commands that expose a memory error or reject input are expected to exit nonzero.

```sh
make -C exercises/c_security all
BIN="$(pwd)/exercises/c_security/build/04_path_traversal"
WORK="$(mktemp -d)"
(
  cd "$WORK" || exit 1
  mkdir notes
  printf 'PUBLIC\n' > notes/hello.txt
  printf 'PRIVATE-DEMO\n' > private.txt
  "$BIN/vulnerable" ../private.txt
  "$BIN/fixed" ../private.txt
  "$BIN/fixed" hello.txt
  ln -s ../private.txt notes/link
  "$BIN/fixed" link
)
rm -rf -- "$WORK"
```

The vulnerable version prints `PRIVATE-DEMO`. The fixed version rejects
`../private.txt`, reads `PUBLIC` for `hello.txt`, and fails to open `link`.
All files in this demonstration are dummy files inside the temporary directory.

## Fix

Require one nonempty filename, rejecting `/`, `.` and `..`. Open the
trusted `notes` directory once and use `openat()` relative to its descriptor.
`O_NOFOLLOW` prevents following a symlink in the final filename component.

This patch deliberately supports only one filename, not nested paths.
The working directory and `notes` directory must be trusted: the initial
directory open does not establish confinement against a hostile parent
directory or prevent hard links created by someone who controls it.

## Check the patch

Check a normal filename, an empty name, `.`, `..`, a name containing `/`,
an absolute path, and the symlink above. Only the normal existing file should
be read under this exercise's input contract.

The [regression suite](../tests/test_exercises.py) checks the fixed behavior.
See the [exercise guide](../README.md#build-and-check) for build and test commands.

## Reference

[Linux open/openat manual: directory descriptors and O_NOFOLLOW](https://man7.org/linux/man-pages/man2/open.2.html).
