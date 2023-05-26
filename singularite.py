from math import gcd, prod
from functools import cache
from itertools import combinations


def coprime(a: int, b: int) -> bool:
    """Tells if two given numbers are coprime, that is if their gcd is 1"""
    return gcd(a, b) == 1

assert coprime(8, 9)

def pairwise_coprime(*xs) -> bool:
    """Tells if all elements of a list are 2-by-2 coprime"""
    return all(coprime(*pair) for pair in combinations(*xs, 2))

assert pairwise_coprime([3, 5, 7])
assert not pairwise_coprime([4, 3, 3])


def eclatements(n, xs):
    assert pairwise_coprime((n, *xs))  # condition 1
    return {(bi, tuple((-n if i == j else bj) % bi for (j, bj) in enumerate(xs)))
            for (i, bi) in enumerate(xs) if bi > 1}


assert eclatements(5, (3, 2, 1)) == {(2, (1, 1, 1)), (3, (1, 2, 1))}


@cache
def isJStrict_(n, xs):
    if set(xs) == {1}:
        return True
    if not pairwise_coprime((n, *xs)):
        return False
    return all(isJStrict(*ys) for ys in eclatements(n, xs))


def isJStrict(n, xs):
    # symmetry and removing ones
    xs = tuple(x for x in sorted(xs) if x > 1)
    if not xs:
        return True
    if len(xs) == 1:
        return coprime(n, xs[0]) # ex 8
    if len(xs) == 2:
        if n == sum(xs):  # habib 1
            return True
        if n < sum(xs):  # triangle
            return False
    return isJStrict_(n % prod(xs), xs) # habib 2


assert isJStrict(2, (1, 1, 1))
assert isJStrict(3, (1, 2, 1))
assert isJStrict(5, (3, 2, 1))
assert not isJStrict(5, (4, 3))

@cache
def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)

# habib 1
for i in range(3, 15):
    assert isJStrict(fib(i), (fib(i-1), fib(i-2)))

@cache
def group(n: int):
    return [i for i in range(1, n) if coprime(n, i)]
