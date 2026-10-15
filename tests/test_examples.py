"""Offline regression coverage for the file integrity and textbook RSA examples."""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


file_hash = load_example("file_hash_checker")
rsa = load_example("rsa")


class FileHashTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "sample.bin"
        self.data = bytes(range(256)) * 100
        self.path.write_bytes(self.data)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "src/file_hash_checker.py"), *map(str, args)],
            capture_output=True, text=True, check=False,
        )

    def test_hash_spans_multiple_read_chunks(self):
        self.assertEqual(file_hash.calculate_file_hash(self.path), hashlib.sha256(self.data).hexdigest())

    def test_empty_file(self):
        self.path.write_bytes(b"")
        self.assertEqual(file_hash.calculate_file_hash(self.path), hashlib.sha256(b"").hexdigest())

    def test_alternate_algorithm(self):
        expected = hashlib.sha512(self.data).hexdigest()
        self.assertEqual(file_hash.calculate_file_hash(self.path, "sha512"), expected)
        result = self.run_cli(self.path, expected, "--algorithm", "sha512")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_hashes_without_comparison(self):
        result = self.run_cli(self.path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(hashlib.sha256(self.data).hexdigest(), result.stdout)

    def test_matching_digest_is_case_insensitive(self):
        digest = hashlib.sha256(self.data).hexdigest().upper()
        self.assertTrue(file_hash.verify_file_integrity(self.path, digest))
        self.assertEqual(self.run_cli(self.path, digest).returncode, 0)

    def test_mismatch_has_failing_exit_status(self):
        result = self.run_cli(self.path, "0" * 64)
        self.assertEqual(result.returncode, 1)
        self.assertIn("do not match", result.stdout)

    def test_missing_file_is_reported_without_traceback(self):
        result = self.run_cli(self.path.with_name("missing"))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_digest_and_algorithm(self):
        for arguments in ((self.path, "not-a-digest"), (self.path, "--algorithm", "shake_128")):
            with self.subTest(arguments=arguments):
                self.assertEqual(self.run_cli(*arguments).returncode, 2)


class RsaTests(unittest.TestCase):
    def test_private_exponent_and_signing_direction(self):
        signature, private = rsa.sign_message(42, 3233, 17, 61, 53)
        self.assertEqual(private, 2753)
        self.assertEqual(signature, pow(42, 2753, 3233))
        self.assertTrue(rsa.verify_signature(42, signature, 17, 3233))

    def test_edge_and_non_coprime_messages(self):
        for message in (0, 1, 42, 53, 61, 3232):
            with self.subTest(message=message):
                signature, _ = rsa.sign_message(message, 3233, 17, 61, 53)
                self.assertTrue(rsa.verify_signature(message, signature, 17, 3233))

    def test_tampering_and_wrong_public_key_fail(self):
        signature, _ = rsa.sign_message(42, 3233, 17, 61, 53)
        self.assertFalse(rsa.verify_signature(43, signature, 17, 3233))
        self.assertFalse(rsa.verify_signature(42, signature + 1, 17, 3233))
        self.assertFalse(rsa.verify_signature(42, signature, 7, 3233))

    def test_invalid_key_parameters(self):
        for params in ((42, 3233, 17, 61, 61), (42, 3233, 17, 60, 53),
                       (42, 3234, 17, 61, 53), (42, 3233, 6, 61, 53)):
            with self.subTest(params=params), self.assertRaises(ValueError):
                rsa.sign_message(*params)

    def test_out_of_range_values(self):
        for message in (-1, 3233):
            with self.subTest(message=message), self.assertRaises(ValueError):
                rsa.sign_message(message, 3233, 17, 61, 53)
        self.assertFalse(rsa.verify_signature(42, -1, 17, 3233))
        self.assertFalse(rsa.verify_signature(42, 3233, 17, 3233))

    def test_modular_exponentiation(self):
        for base, exponent, modulus in ((0, 0, 7), (123, 0, 17), (42, 2753, 3233)):
            self.assertEqual(rsa.mod_exp(base, exponent, modulus), pow(base, exponent, modulus))
        with self.assertRaises(ValueError):
            rsa.mod_exp(2, -1, 7)


if __name__ == "__main__":
    unittest.main()
