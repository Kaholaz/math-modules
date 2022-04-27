from functools import reduce
import numpy as np


def get_euklid_elements(a: int, b: int) -> tuple[list[int], list[int]]:
    """
    This method runs the euklid GCD algorithm and returns a list of all partial
    remainders and quotients.

    The last element of the first list returned is the GCD
    """
    # Inizialize AB and Q. AB are all the numbers used in the division.
    # Q contains all the quotients used.
    AB, Q = [a, b], []

    # Rund the algorithm to a solution is found.
    while not (AB[-1] == 0):
        Q.append(AB[-2] // AB[-1])  # Append the quotient to Q.
        AB.append(AB[-2] % AB[-1])  # Append the remainder to AB

    # Last element is 0 (not needed)
    AB.pop()
    # Last element is the quotient used to get 0 as the remainder (not needed)
    Q.pop()
    return AB, Q


def gcd(a: int, b: int) -> int:
    """
    Runs euclids algorithm and returns the greatest common denominator
    """
    AB, _ = get_euklid_elements(a, b)
    return AB[-1]


def lcm(a: int, b: int) -> int:
    """
    Finds the least common multiple of two integers a and b.
    """
    return int(a * b / gcd(a, b))


def inv_mod(integer: int, mod: int) -> int:
    """
    Uses the extended euclids algorithm to find the multiplicative
    inverse of an integer in modular arithmetics.
    """
    _, Q = get_euklid_elements(integer, mod)
    m, n = 0, 1

    # iterate over the reversed Q
    for q in Q[-1::-1]:
        m, n = n, m + n * -q

    return m % mod


def prime_sive(n: int) -> list[int]:
    """
    Uses the sieve of eratosthenes to find all primes less than or equal to a given number.
    """
    is_prime = [True] * (n + 1)

    # All odd numbers up to the sqrt of the
    for i in range(2, int(n**0.5 + 1)):
        if is_prime[i]:
            is_prime[i * i :: i] = [False] * (n // i + 1 - i)

    integers = np.linspace(0, n, n + 1, True, dtype=int)
    return [prime for prime in (integers * is_prime)[2:] if prime]


def factorize(n: int) -> list[int]:
    """
    Reduces a number to its prime factors and returns the list of prime factors.
    """
    primes = prime_sive(int(n**0.5))
    remainder = n
    factors = []
    for prime in primes:
        while remainder % prime == 0:
            remainder //= prime
            factors.append(prime)
            if remainder == 1:
                # break out of the inner and outer loop
                break
        else:
            # remainder is not 1
            # we want to continue searching
            continue
        # remainder is 1
        # we are done so we can exit the loop
        break
    else:
        # remainder is not 1
        # the remainder is a factor of n
        factors.append(remainder)

    return factors


def totient(n: int) -> int:
    """
    Retuns the result of eulers totient function of a number
    with unique prime factors.
    """
    if n < 2:
        raise ValueError("The number provided has to be greater than or equal to 2.")

    factors = factorize(n)
    # The function will not work with duplicate factors
    if n < 2 or len(set(factors)) != len(factors):
        raise ValueError("The number provided have duplicate prime factors.")

    # The product of all the factors with one subtracted
    return reduce(lambda a, b: a * b, map(lambda c: c - 1, factors))


def mod_pow(base: int, pow: int, mod: int) -> int:
    """
    Retuns the result of an exponent operation in a given modular base.
    """
    if pow == 0:
        return 1
    if pow < 0:
        raise ValueError("The exponent needs to be positive")

    binary_pow = f"{pow:b}"  # The binary digits of the exponent
    result = base % mod
    for digit in binary_pow[1:]:
        # Square
        result = (result * result) % mod

        # Fix digit
        if digit == "1":
            result = (result * base) % mod

    return result


def decrypt_encrypt(message: list[int], key: tuple[int, int]) -> list[int]:
    """
    Encrypts or decrypts a message given a key.
    The key should be written in the form (n, e)/(n, d)
    """
    return [mod_pow(element, key[1], key[0]) for element in message]


def find_private_key(public_key: tuple[int, int]):
    """
    Finds a private key to a public key using a brute force method.
    The puplic key should be written in the form (n, e)
    """
    tot = totient(public_key[0])
    return public_key[0], inv_mod(public_key[1], tot)


def crack_encrypted_message(message: list[int], public_key: tuple[int, int]):
    """
    Finds the private key given a public key and encrypts a message.
    The puplic key should be written in the form (n, e)
    """
    private_key = find_private_key(public_key)
    return decrypt_encrypt(message, private_key)
