from math import gcd, prod
from typing import List
from functools import cache
from itertools import combinations


def coprime(x: int, y: int) -> bool:
    """Tells if two given numbers are coprime, that is if their gcd is 1"""
    return gcd(x, y) == 1


def all_coprime(xs: List[int]) -> bool:
    """Tells if all elements of a list are 2-by-2 coprime"""
    return all(coprime(*pair) for pair in combinations(xs, 2))


def singularite(b0: int, m: int):
    # bs is a m-uple of rep mod b0
    # gonna yield phi(b0)^m tuples
    # for bs in product(*repeat(range(1, b0), m)):
    #     if all(coprime(b0, bi) for bi in bs):
    #         yield (b0, *bs)  # m + 1 elements
    # yields fewer elements to account for (b0, a, b) ~ (b0, b a) symmetry
    if m == 0:
        return {(b0,)}
    return ((*init, last, b)
            for (*init, last) in singularite(b0, m - 1)
            for b in range(1, last)
            if coprime(b0, b))


def gen_singularite(upto=10, m=2):
    return (bs for b0 in range(2, upto) for bs in singularite(b0, m))


def change(bs, j, v):
    rest = list(enumerate(bs))[1:]
    return tuple([bs[0]] + [bi if i != j else v for (i, bi) in rest])


def choix(bs):
    yield bs
    m = len(bs) - 1
    k = 1
    i = 1
    while True:
        bs = change(bs, i, k*bs[0]+bs[i])
        yield bs
        i += 1
        if i > m:
            i = 1
            k += 1


def choix_coprime(bs):
    return filter(all_coprime, choix(bs))


def eclatements(n, xs):
    assert all_coprime([n, *xs])  # condition 1
    return {(bi, tuple((-n if i == j else bj) % bi for (j, bj) in enumerate(xs)))
            for (i, bi) in enumerate(xs) if bi > 1}


assert eclatements(5, (3, 2, 1)) == {(2, (1, 1, 1)), (3, (1, 2, 1))}


@cache
def isJStrict_(n, xs):
    # if lisse(bs):
    #     return True
    # if not all_coprime(bs):
    #     return False
    # return all(isJStrict(cs) for cs in eclatements(bs))
    stack = [(n, xs)]
    while len(stack) > 0:
        ni, bs = stack.pop()
        if not all_coprime([ni, *bs]):
            return False
        if set(bs) != {1}:  # not lisse
            for cs in eclatements(ni, bs):
                stack.append(cs)
    return True


def isJStrict(n, xs):
    xs = tuple(x for x in sorted(xs) if x > 1)
    if not xs:
        return True
    if len(xs) == 2:
        a, b = xs[:2]
        if n == a + b:  # prop 1
            return True
        if n < a + b:  # prop 4
            return False
    return isJStrict_(n % prod(xs), xs)


assert isJStrict(2, (1, 1, 1))
assert isJStrict(3, (1, 2, 1))
assert isJStrict(5, (3, 2, 1))


@cache
def group(n: int):
    return [i for i in range(1, n) if coprime(n, i)]
