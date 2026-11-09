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

Requirements: Linux, GCC or Clang with C11 support, GNU Make, and Python 3.10 or
newer. The tests use only Python's standard library. The random-token fix uses
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

## Working through an exercise

Read the exploit explanation, run the reproduction, and compare the two code
versions. Repeat the failing input against the fixed version, then try the
boundary cases described in its README. Exercises 04 and 15 include a temporary
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
