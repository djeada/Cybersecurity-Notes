# C Security Exercises

[Repository home](../../README.md) · [Secure programming notes](../../notes/basics/developing_secure_apps.md)

Fifteen small C exercises show how a vulnerability works and how its patch
removes the cause. Each exercise contains exactly two code versions:

- `vulnerable.c`: the program before the patch, with an intentional weakness.
- `fixed.c`: the program after the patch.
- `README.md`: the exploit mechanism, reproduction commands, expected results,
  fix explanation, and boundary cases to check.

Use dummy data in an unprivileged Linux lab. The examples target only their own
local programs; the filesystem demonstrations create and remove temporary lab
directories. Memory-unsafe programs have undefined behavior, so ordinary output
and crashes can vary with the compiler, optimization level, and memory layout.
A sanitizer report establishes a memory error, not arbitrary code execution.

## Build and check

Requirements: Linux, GCC or Clang with C11 support, GNU Make, Bash, standard
Linux utilities (`id`, `date`, `seq`, `mktemp`), and Python 3.10 or newer.
The tests use only Python's standard library. The random-token fix uses
Linux `getrandom()`; the filesystem fixes use POSIX descriptor-relative APIs.

Run from the repository root:

```sh
make -C exercises/c_security all        # build all 30 ordinary executables
make -C exercises/c_security test       # check fixes and deterministic demonstrations
make -C exercises/c_security asan       # build all 30 with AddressSanitizer and UBSan
make -C exercises/c_security test-asan  # check fixes and intentional memory errors
```

The ordinary suite avoids executing the deliberately invalid memory accesses.
The sanitizer suite repeats the functional checks with instrumented binaries
and checks diagnostics for nine vulnerable memory examples. Expected vulnerable
failures are captured by the test harness, so a passing suite still exits 0.
Both suites run in the repository's GitHub Actions workflow.

For example, compare the authentication decision before and after the patch:

```sh
./exercises/c_security/build/13_prefix_auth/vulnerable sec  # ACCESS GRANTED
./exercises/c_security/build/13_prefix_auth/fixed sec       # DENIED
./exercises/c_security/build/13_prefix_auth/fixed secret42  # ACCESS GRANTED
```

Compare the code with:

```sh
git diff --no-index exercises/c_security/13_prefix_auth/vulnerable.c exercises/c_security/13_prefix_auth/fixed.c
```

`git diff --no-index` returns 1 when the two versions differ. Individual programs
that reject input or trigger a sanitizer also commonly exit nonzero; follow each
exercise's documented output rather than assuming all commands should succeed.

## Exercise index

| Exercise | Weakness | Before | After |
| --- | --- | --- | --- |
| [01 — Adjacent admin flag overwrite](01_admin_flag_overwrite/README.md) | [CWE-787](https://cwe.mitre.org/data/definitions/787.html) | [vulnerable.c](01_admin_flag_overwrite/vulnerable.c) | [fixed.c](01_admin_flag_overwrite/fixed.c) |
| [02 — Untrusted printf format](02_format_string/README.md) | [CWE-134](https://cwe.mitre.org/data/definitions/134.html) | [vulnerable.c](02_format_string/vulnerable.c) | [fixed.c](02_format_string/fixed.c) |
| [03 — Shell command injection](03_command_injection/README.md) | [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | [vulnerable.c](03_command_injection/vulnerable.c) | [fixed.c](03_command_injection/fixed.c) |
| [04 — Directory traversal](04_path_traversal/README.md) | [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | [vulnerable.c](04_path_traversal/vulnerable.c) | [fixed.c](04_path_traversal/fixed.c) |
| [05 — Heap buffer overflow](05_heap_overflow/README.md) | [CWE-122](https://cwe.mitre.org/data/definitions/122.html) | [vulnerable.c](05_heap_overflow/vulnerable.c) | [fixed.c](05_heap_overflow/fixed.c) |
| [06 — Use after free](06_use_after_free/README.md) | [CWE-416](https://cwe.mitre.org/data/definitions/416.html) | [vulnerable.c](06_use_after_free/vulnerable.c) | [fixed.c](06_use_after_free/fixed.c) |
| [07 — Double free](07_double_free/README.md) | [CWE-415](https://cwe.mitre.org/data/definitions/415.html) | [vulnerable.c](07_double_free/vulnerable.c) | [fixed.c](07_double_free/fixed.c) |
| [08 — Truncated allocation size](08_integer_truncation/README.md) | [CWE-197](https://cwe.mitre.org/data/definitions/197.html) | [vulnerable.c](08_integer_truncation/vulnerable.c) | [fixed.c](08_integer_truncation/fixed.c) |
| [09 — Signed length converted to size_t](09_negative_length/README.md) | [CWE-195](https://cwe.mitre.org/data/definitions/195.html) | [vulnerable.c](09_negative_length/vulnerable.c) | [fixed.c](09_negative_length/fixed.c) |
| [10 — Off-by-one array write](10_off_by_one/README.md) | [CWE-193](https://cwe.mitre.org/data/definitions/193.html) | [vulnerable.c](10_off_by_one/vulnerable.c) | [fixed.c](10_off_by_one/fixed.c) |
| [11 — Missing string terminator](11_unterminated_string/README.md) | [CWE-170](https://cwe.mitre.org/data/definitions/170.html) | [vulnerable.c](11_unterminated_string/vulnerable.c) | [fixed.c](11_unterminated_string/fixed.c) |
| [12 — Packet length beyond received data](12_packet_length/README.md) | [CWE-125](https://cwe.mitre.org/data/definitions/125.html) | [vulnerable.c](12_packet_length/vulnerable.c) | [fixed.c](12_packet_length/fixed.c) |
| [13 — Password prefix comparison](13_prefix_auth/README.md) | [CWE-187](https://cwe.mitre.org/data/definitions/187.html) | [vulnerable.c](13_prefix_auth/vulnerable.c) | [fixed.c](13_prefix_auth/fixed.c) |
| [14 — Predictable random token](14_predictable_token/README.md) | [CWE-338](https://cwe.mitre.org/data/definitions/338.html) | [vulnerable.c](14_predictable_token/vulnerable.c) | [fixed.c](14_predictable_token/fixed.c) |
| [15 — Symlink report overwrite](15_temp_file_symlink/README.md) | [CWE-59](https://cwe.mitre.org/data/definitions/59.html) | [vulnerable.c](15_temp_file_symlink/vulnerable.c) | [fixed.c](15_temp_file_symlink/fixed.c) |

## What an attacker actually gains

These programs model a victim processing untrusted input. In this local lab,
you play both roles: the attack is the argument or filesystem entry you supply;
launching the executable stands in for the victim handling it. None of these
programs listens on a network, changes its UID, or implements a real login or
password-reset service. Keep the lab unprivileged and use the dummy files shown
in the walkthroughs.

Read each outcome at the boundary it actually crosses:

- **Application state or authorization:** a flag or password check changes what
  the application would allow. An application's admin role is separate from the
  operating system's root account.
- **Information disclosure:** bytes reach attacker-visible output. Reading beyond
  an object is a memory error; it becomes a demonstrated disclosure only when
  those extra bytes are actually exposed.
- **File access:** a victim reads or overwrites a path using its existing file
  permissions. This can violate its interface's policy without bypassing Unix
  access checks.
- **Command execution:** attacker-selected commands run with the authority
  available to the process executing them. `id` shows that authority in exercise 03.
- **Process failure:** a sanitizer or allocator terminates the program. This
  establishes a failing operation; a remote denial of service needs an exposed
  service and a reachable trigger that these CLI programs do not provide.

| Exercise | What the attacker supplies or triggers | Demonstrated result | What is not established |
| --- | --- | --- | --- |
| [01](01_admin_flag_overwrite/README.md) | Nine-byte username | Adjacent toy admin flag becomes true on the documented ABI | Linux root, a shell, or a protected admin action |
| [02](02_format_string/README.md) | `private=%s` format text | Reads the supplied internal dummy string through printf | An arbitrary-address read, a write, or code execution |
| [03](03_command_injection/README.md) | Filename containing `; id; ...; #` | Shell commands execute and write a proof file as the lab account | Automatic elevation beyond that account |
| [04](04_path_traversal/README.md) | `../private.txt` or a symlink name | First line of a readable file outside the intended directory | Reading files the victim cannot open, writing, or a shell |
| [05](05_heap_overflow/README.md) | Thirty-byte message | Heap write beyond a sixteen-byte allocation; sanitizer abort | A chosen neighboring target or instruction-pointer control |
| [06](06_use_after_free/README.md) | Any contact name | Read after free; sanitizer abort | Controlled allocation reuse or a chosen secret leak |
| [07](07_double_free/README.md) | Invocation of an unconditional cleanup path | A duplicate free; sanitizer/allocator abort | An attacker-controlled argument or allocator takeover |
| [08](08_integer_truncation/README.md) | Count `4100` | Allocates 64 bytes, attempts a 65,600-byte write of `X` | Attacker-selected write contents or a useful target |
| [09](09_negative_length/README.md) | Length `-1` | Huge invalid copy length; sanitizer abort | A controlled memory disclosure or execution primitive |
| [10](10_off_by_one/README.md) | Invocation of an unconditional loop | One-byte out-of-bounds write of `A` | Attacker-selected byte/index or a changed security decision |
| [11](11_unterminated_string/README.md) | Eight-character username | Out-of-bounds string read; sanitizer abort | Reliable disclosure of a named secret |
| [12](12_packet_length/README.md) | Claimed payload length `200` | Read beyond a three-byte payload; sanitizer abort | Data exfiltration: the copied bytes are never output |
| [13](13_prefix_auth/README.md) | Empty or prefix password | Toy check prints `ACCESS GRANTED` | A real account session, shell, or root privileges |
| [14](14_predictable_token/README.md) | Guessed token-generation time | A short seed search reproduces a generated token | Account takeover without a reset verifier and accepted guesses |
| [15](15_temp_file_symlink/README.md) | Pre-created report symlink | Victim replaces a chosen writable lab file's contents with `REPORT` | Arbitrary contents, elevated permissions, or command execution |

The memory-corruption rows describe the demonstrated read/write and failure.
A memory bug can support a stronger exploit in a larger program, but that
requires a useful target, attacker influence over the relevant state, and a
working chain to an unauthorized effect. “Buffer overflow” alone is not evidence
of full system control. The individual READMEs say which pieces are absent.

For a class, start with 13, 02, 03, 04, and 15 to establish visible authorization,
disclosure, command, and filesystem outcomes. Then use 01 and the memory examples
to trace bytes, sizes, and object lifetimes. The READMEs for 07 and 10 explicitly
identify unconditional bugs rather than inventing malicious inputs they do not
accept.

## Working through an exercise

Identify what the attacker controls and the intended boundary. Follow the
walkthrough and compare its observed output with the stated gain, then compare
the two code versions. Repeat the failing input against the fixed version, then
try the boundary cases described in its README. Exercises 04 and 15 include a temporary
directory setup because their programs resolve paths relative to the current
working directory; keep that setup when reproducing them.

The fixes address the demonstrated weakness under each exercise's stated
assumptions. In particular, the filesystem exercises assume a trusted base
directory, and the authentication example retains a toy hardcoded credential.

## Compiler and sanitizer behavior

Both build modes default to `-O0 -g -Wall -Wextra -Wpedantic`. Keeping optimization
off preserves deliberately invalid operations whose results are otherwise unused,
such as the toy packet copy. The instrumented mode adds
`-fsanitize=address,undefined -fno-omit-frame-pointer`. Warnings in intentionally
vulnerable sources are expected; keep them visible.

AddressSanitizer does not catch every memory error. In exercise 01, a small
intra-struct overwrite may corrupt the admin flag without crossing the enclosing
object's redzone. That README also provides a larger input for an instrumented
out-of-bounds demonstration. Exact addresses and diagnostic wording can vary.

To switch compilers or flags, clean first because Make does not track flag changes:

```sh
make -C exercises/c_security clean
make -C exercises/c_security CC=clang test test-asan
```

See the [AddressSanitizer documentation](https://clang.llvm.org/docs/AddressSanitizer.html)
for instrumentation and diagnostics. `make -C exercises/c_security clean` removes
only the generated `build/` and `build-asan/` directories.
