"""Textbook RSA arithmetic for learning only.

These tiny keys and raw operations are insecure: there is no secure padding,
cryptographic key generation, or side-channel protection. Production encryption
and signatures require maintained libraries and schemes such as OAEP and PSS.

Signing applies the private exponent. Verification uses the public exponent.
"""

from math import gcd, isqrt


def mod_exp(base: int, exp: int, mod: int) -> int:
    """Compute base**exp modulo mod by repeated squaring."""
    if exp < 0 or mod <= 1:
        raise ValueError("Exponent must be nonnegative and modulus must exceed one")
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return x, y, g such that a*x + b*y = g = gcd(a, b) for positive inputs."""
    if b == 0:
        return 1, 0, a
    x, y, divisor = extended_gcd(b, a % b)
    return y, x - (a // b) * y, divisor


def _is_prime(value: int) -> bool:
    """Trial division, suitable only for the small educational parameters here."""
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, isqrt(value) + 1))


def sign_message(
    message: int, modulus: int, public_exponent: int, p: int, q: int
) -> tuple[int, int]:
    """Return a textbook signature and private exponent for small teaching keys."""
    if p == q or not _is_prime(p) or not _is_prime(q):
        raise ValueError("p and q must be distinct primes")
    if modulus != p * q:
        raise ValueError("Modulus must equal p * q")
    phi = (p - 1) * (q - 1)
    if not 1 < public_exponent < phi or gcd(public_exponent, phi) != 1:
        raise ValueError("Public exponent must be between 1 and phi and coprime to phi")
    if not 0 <= message < modulus:
        raise ValueError("Message must be in the range [0, modulus)")
    inverse, _, _ = extended_gcd(public_exponent, phi)
    private_exponent = inverse % phi
    return mod_exp(message, private_exponent, modulus), private_exponent


def verify_signature(
    original_message: int, signature: int, public_exponent: int, modulus: int
) -> bool:
    """Verify a textbook signature using the public key, never the private key."""
    if modulus <= 1 or public_exponent <= 1:
        raise ValueError("Modulus and public exponent must exceed one")
    if not 0 <= original_message < modulus or not 0 <= signature < modulus:
        return False
    return mod_exp(signature, public_exponent, modulus) == original_message


def main() -> None:
    p, q = 61, 53
    modulus, public_exponent, message = p * q, 17, 42
    signature, _ = sign_message(message, modulus, public_exponent, p, q)
    print("Educational textbook RSA only; do not use these keys or raw operations for security.")
    print(f"Public key (n, e): ({modulus}, {public_exponent})")
    print(f"Message: {message}; signature: {signature}")
    print(f"Signature verified: {verify_signature(message, signature, public_exponent, modulus)}")


if __name__ == "__main__":
    main()
