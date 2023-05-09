from math import sqrt
from itertools import takewhile


def is_prime(n):
    return n > 1 and all(n % i != 0 for i in range(2, int(sqrt(n)) + 1))


assert all(map(is_prime, [2, 3, 5, 7, 11]))
assert not any(map(is_prime, [1, 4, 6, 8, 9, 10]))


def primes(l=[2, 3]):
    """Primes generator (with cheeky memoization)"""
    for p in l:
        yield p
    i = l[-1]
    while True:
        i += 2
        if is_prime(i):
            l.append(i)
            yield i


def primes_to(n):
    return takewhile(lambda p: p <= n, primes())


assert list(primes_to(42)) == [2, 3, 5, 7,
                               11, 13, 17, 19, 23, 29, 31, 37, 41]


def prime_fact(n):
    """Prime factorization of n as a list of prime and their respective powers"""
    d = {}
    for p in primes_to(n):
        while n % p == 0:
            d[p] = d.get(p, 0) + 1
            n //= p
    return d


assert prime_fact(100) == {2: 2, 5: 2}
