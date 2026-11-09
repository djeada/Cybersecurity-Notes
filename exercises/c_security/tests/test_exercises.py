"""Exercise regressions with dummy data; intentional memory errors need ASan."""
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / os.environ.get("C_SECURITY_BUILD", "build")
SANITIZED = os.environ.get("C_SECURITY_SANITIZED") == "1"


def program(slug, variant, *args, cwd=None):
    binary = BUILD / slug / variant
    result = subprocess.run([str(binary), *args], cwd=cwd,
                            capture_output=True, text=True, timeout=5)
    if variant == "fixed" and SANITIZED:
        if "AddressSanitizer" in result.stderr or "runtime error:" in result.stderr:
            raise AssertionError(f"sanitizer error in {slug}/fixed: {result.stderr}")
    return result


class SecurityExerciseTests(unittest.TestCase):
    def test_admin_checked_input(self):
        slug = "01_admin_flag_overwrite"
        for name in ("", "hello", "A" * 7):
            self.assertEqual("admin=0\n", program(slug, "fixed", name).stdout)
        for name in ("A" * 8, "A" * 9, "A" * 64):
            self.assertNotEqual(0, program(slug, "fixed", name).returncode)

    def test_format_string_is_literal(self):
        slug = "02_format_string"
        self.assertEqual("hello %\n", program(slug, "vulnerable", "hello %%").stdout)
        for text in ("hello %%", "test %p", "test %n"):
            result = program(slug, "fixed", text)
            self.assertEqual(0, result.returncode)
            self.assertEqual(text + "\n", result.stdout)

    def test_shell_injection_is_removed(self):
        slug = "03_command_injection"
        attack = "missing; echo INJECTED; #"
        with tempfile.TemporaryDirectory() as directory:
            self.assertIn("INJECTED", program(slug, "vulnerable", attack, cwd=directory).stdout)
            self.assertEqual("MISSING\n", program(slug, "fixed", attack, cwd=directory).stdout)
            (pathlib.Path(directory) / "file with spaces").touch()
            self.assertEqual("EXISTS\n", program(slug, "fixed", "file with spaces", cwd=directory).stdout)

    def test_directory_traversal_rejected(self):
        slug = "04_path_traversal"
        with tempfile.TemporaryDirectory() as directory:
            here = pathlib.Path(directory)
            (here / "notes").mkdir()
            (here / "private.txt").write_text("SECRET-DEMO\n")
            (here / "notes" / "hello.txt").write_text("PUBLIC\n")
            self.assertIn("SECRET-DEMO", program(slug, "vulnerable", "../private.txt", cwd=here).stdout)
            self.assertNotEqual(0, program(slug, "fixed", "../private.txt", cwd=here).returncode)
            self.assertIn("PUBLIC", program(slug, "fixed", "hello.txt", cwd=here).stdout)
            for name in ("", ".", "..", "nested/name", str(here / "private.txt")):
                self.assertNotEqual(0, program(slug, "fixed", name, cwd=here).returncode)
            (here / "notes" / "link").symlink_to("../private.txt")
            self.assertNotEqual(0, program(slug, "fixed", "link", cwd=here).returncode)

    def test_heap_copy_is_bounded(self):
        slug = "05_heap_overflow"
        for length in (0, 15):
            self.assertEqual(0, program(slug, "fixed", "A" * length).returncode)
        for length in (16, 30):
            self.assertNotEqual(0, program(slug, "fixed", "A" * length).returncode)

    def test_contact_lifetime(self):
        self.assertIn("Ada", program("06_use_after_free", "fixed", "Ada").stdout)

    def test_double_free_fixed(self):
        self.assertEqual(0, program("07_double_free", "fixed").returncode)

    def test_integer_size(self):
        slug = "08_integer_truncation"
        self.assertEqual("allocated=64\n", program(slug, "fixed", "4").stdout)
        self.assertEqual("allocated=65536\n", program(slug, "fixed", "4096").stdout)
        for count in ("0", "-1", " -1", "+4", " 4", "4100", "4garbage", "", "9" * 100):
            self.assertNotEqual(0, program(slug, "fixed", count).returncode)

    def test_signed_size(self):
        slug = "09_negative_length"
        for count in ("0", "7", "32"):
            self.assertEqual(0, program(slug, "fixed", count).returncode)
        for count in ("-1", "33", "garbage", "7garbage", "", "9" * 100):
            self.assertNotEqual(0, program(slug, "fixed", count).returncode)

    def test_loop_boundary(self):
        self.assertEqual(0, program("10_off_by_one", "fixed").returncode)

    def test_terminated_string(self):
        slug = "11_unterminated_string"
        for name in ("", "ABCDEFG"):
            self.assertEqual("user=" + name + "\n", program(slug, "fixed", name).stdout)
        for name in ("ABCDEFGH", "A" * 64):
            self.assertNotEqual(0, program(slug, "fixed", name).returncode)

    def test_packet_length(self):
        slug = "12_packet_length"
        for count in ("0", "3"):
            self.assertEqual("copied=" + count + "\n", program(slug, "fixed", count).stdout)
        for count in ("4", "200", "256", "259", "-1", " -0", "+3", "garbage", "3garbage", "", "9" * 100):
            self.assertNotEqual(0, program(slug, "fixed", count).returncode)

    def test_complete_password(self):
        slug = "13_prefix_auth"
        self.assertIn("ACCESS GRANTED", program(slug, "vulnerable", "sec").stdout)
        self.assertIn("DENIED", program(slug, "fixed", "sec").stdout)
        self.assertIn("DENIED", program(slug, "fixed", "").stdout)
        self.assertIn("ACCESS GRANTED", program(slug, "fixed", "secret42").stdout)
        self.assertIn("DENIED", program(slug, "fixed", "wrong").stdout)
        self.assertIn("DENIED", program(slug, "fixed", "secret42suffix").stdout)

    def test_csprng_token(self):
        slug = "14_predictable_token"
        x = program(slug, "vulnerable", "1234")
        y = program(slug, "vulnerable", "1234")
        self.assertEqual(x.stdout, y.stdout)
        fixed = program(slug, "fixed")
        self.assertEqual(0, fixed.returncode)
        self.assertRegex(fixed.stdout, r"^token=[0-9a-f]{32}\n$")

    def test_tempfile_rejects_symlink(self):
        slug = "15_temp_file_symlink"
        with tempfile.TemporaryDirectory() as directory:
            here = pathlib.Path(directory)
            (here / "scratch").mkdir()
            (here / "victim.txt").write_text("ORIGINAL\n")
            (here / "scratch" / "report.tmp").symlink_to("../victim.txt")
            self.assertNotEqual(0, program(slug, "fixed", cwd=here).returncode)
            self.assertEqual("ORIGINAL\n", (here / "victim.txt").read_text())
            self.assertEqual(0, program(slug, "vulnerable", cwd=here).returncode)
            self.assertEqual("REPORT\n", (here / "victim.txt").read_text())
            (here / "scratch" / "report.tmp").unlink()
            self.assertEqual(0, program(slug, "fixed", cwd=here).returncode)
            report = here / "scratch" / "report.tmp"
            self.assertEqual("REPORT\n", report.read_text())
            self.assertEqual(0, report.stat().st_mode & 0o077)
            report.write_text("KEEP\n")
            self.assertNotEqual(0, program(slug, "fixed", cwd=here).returncode)
            self.assertEqual("KEEP\n", report.read_text())

    @unittest.skipUnless(SANITIZED, "intentional memory errors require make test-asan")
    def test_vulnerable_memory_errors(self):
        cases = (
            ("01_admin_flag_overwrite", ("A" * 64,), "stack-buffer-overflow"),
            ("05_heap_overflow", ("A" * 30,), "heap-buffer-overflow"),
            ("06_use_after_free", ("Ada",), "heap-use-after-free"),
            ("07_double_free", (), "double-free"),
            ("08_integer_truncation", ("4100",), "heap-buffer-overflow"),
            ("09_negative_length", ("-1",), "negative-size-param"),
            ("10_off_by_one", (), "stack-buffer-overflow"),
            ("11_unterminated_string", ("ABCDEFGH",), "stack-buffer-overflow"),
            ("12_packet_length", ("200",), "stack-buffer-overflow|memcpy-param-overlap"),
        )
        for slug, args, diagnostic in cases:
            with self.subTest(exercise=slug):
                result = program(slug, "vulnerable", *args)
                self.assertNotEqual(0, result.returncode)
                self.assertRegex(result.stderr, diagnostic)


if __name__ == "__main__":
    unittest.main()
