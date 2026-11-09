# 04 — Reading a file outside the allowed directory

[All exercises and impact guide](../README.md#what-an-attacker-actually-gains)

**Weakness:** [CWE-22](https://cwe.mitre.org/data/definitions/22.html) ·
**Before:** [vulnerable.c](vulnerable.c) · **After:** [fixed.c](fixed.c)

## Attacker control and objective

The attacker controls the requested note name. The application intends
to expose only files inside `notes/`. The objective is to read a file that
the victim can access but that its note-viewing interface should not expose.
The lab uses `private.txt` containing only a dummy marker.

## How the attack works

1. The victim joins `notes/` and the supplied name without validation.
2. The attacker submits `../private.txt`.
3. The operating system resolves `notes/../private.txt` to `private.txt` in
   the parent directory. A textual prefix does not constrain resolution.
4. `fopen()` opens that file, and `fgets()` sends its first line to stdout.

A second route is an attacker-created `notes/link` symlink pointing at the
same outside file: the input need not contain `..` if filesystem resolution
follows a link.

## Run the attack and compare the patch

Use Bash from the repository root. These are local programs run as your
ordinary account. Rejection and sanitizer failures intentionally return nonzero;
run the commands individually or in a shell without `set -e`.

```sh
make -C exercises/c_security all
LAB_BIN="$(pwd)/exercises/c_security/build/04_path_traversal"
LAB_WORK="$(mktemp -d)"
(
  cd "$LAB_WORK" || exit 1
  # Instructor/victim setup: public data and a dummy outside file.
  mkdir notes
  printf 'PUBLIC\n' > notes/hello.txt
  printf 'PRIVATE-DEMO\n' > private.txt
  "$LAB_BIN/vulnerable" hello.txt
  # Attacker: replace the requested note name with a parent traversal.
  "$LAB_BIN/vulnerable" ../private.txt
  "$LAB_BIN/fixed" ../private.txt
  "$LAB_BIN/fixed" hello.txt
  # Additional route, if the attacker can create entries inside notes/.
  ln -s ../private.txt notes/link
  "$LAB_BIN/vulnerable" link
  "$LAB_BIN/fixed" link
)
rm -rf -- "$LAB_WORK"
```

The vulnerable runs print `PUBLIC`, then `PRIVATE-DEMO` for traversal,
and later `PRIVATE-DEMO` for the symlink. The fixed version rejects traversal,
still reads `PUBLIC`, and reports an `openat` error for the symlink.

## What the attacker gains

**Demonstrated:** disclosure of the outside file's first line, up to 127
bytes with this reader. It does not write that file or run a command.
The term “private” describes the application's intended boundary: the lab
does not change Unix permissions, and both roles run as your account.

A victim process cannot bypass the operating system's access checks merely
by traversing a path. The real-world concern is that the victim may already
have read access that its untrusted caller should not receive through this
interface. This example does not grant a shell or root privileges.

## Why the patch stops this attack

Reject empty names, `.`, `..`, and any `/`, so only one filename remains.
Resolve it with `openat()` relative to an opened, trusted `notes` directory.
`O_NOFOLLOW` rejects a symlink in that final component.

The initial directory and its parent must be trusted. This patch is not a
general nested-path sandbox and does not prevent malicious hard links in a
directory controlled by an attacker.

## Verify the result

A normal file must remain readable. Traversal, an absolute path, a nested
path, and the symlink above must fail. A failed open on a genuinely unreadable
file is OS enforcement; the vulnerable interface's missing path restriction
is a separate application-level issue.

The [regression suite](../tests/test_exercises.py) checks the corresponding
fixed behavior. Run `make -C exercises/c_security test test-asan` for all exercises.

## References

[Linux open/openat manual](https://man7.org/linux/man-pages/man2/open.2.html).
