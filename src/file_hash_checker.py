"""Calculate file digests and compare them with trusted expected values."""

import argparse
import hashlib
import hmac
import re
import sys


ALGORITHMS = ("sha256", "sha384", "sha512", "sha3_256", "sha3_384", "sha3_512", "blake2b", "blake2s")


def calculate_file_hash(file_path: str, hash_algorithm: str = "sha256") -> str:
    """Hash a file in bounded chunks; propagate input and filesystem errors."""
    if hash_algorithm not in ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    digest = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as source:
        while chunk := source.read(8192):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file_integrity(file_path: str, known_hash: str, hash_algorithm: str = "sha256") -> bool:
    """Compare a digest with an expected hexadecimal value, ignoring letter case."""
    calculated = calculate_file_hash(file_path, hash_algorithm)
    expected = known_hash.strip().lower()
    if len(expected) != len(calculated) or not re.fullmatch(r"[0-9a-f]+", expected):
        return False
    return hmac.compare_digest(calculated, expected)


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_path", help="File to hash")
    parser.add_argument("known_hash", nargs="?", help="Trusted hexadecimal digest to compare")
    parser.add_argument("--algorithm", choices=ALGORITHMS, default="sha256")
    options = parser.parse_args(args)

    expected = options.known_hash
    if expected is not None:
        expected = expected.strip().lower()
        length = hashlib.new(options.algorithm).digest_size * 2
        if len(expected) != length or not re.fullmatch(r"[0-9a-f]+", expected):
            parser.error(f"expected a {length}-character hexadecimal {options.algorithm} digest")

    try:
        calculated = calculate_file_hash(options.file_path, options.algorithm)
    except (OSError, ValueError) as error:
        print(f"Cannot hash {options.file_path}: {error}", file=sys.stderr)
        return 2

    print(f"{options.algorithm}: {calculated}")
    if expected is None:
        return 0
    if hmac.compare_digest(calculated, expected):
        print("File integrity verified: The hashes match.")
        return 0
    print("File integrity verification failed: The hashes do not match.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
