from math import gcd
from typing import List
from functools import cache


def coprime(x: int, y: int) -> bool:
    """Tells if two given numbers are coprime, that is if their gcd is 1"""
    return gcd(x, y) == 1


def all_coprime(xs: List[int]) -> bool:
    """Tells if all elements of a list are 2-by-2 coprime"""
    if len(xs) < 2:
        return True
    # h, *t = xs
    # return all(coprime(h, x) for x in t) and all_coprime(t)
    for i in range(len(xs)):
        for j in range(i):
            if not coprime(xs[i], xs[j]):
                return False
    return True


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


def eclatements(bs):
    assert all_coprime(bs)  # condition 1
    rest = list(enumerate(bs))[1:]
    # let m = len(bs) - 1, yields up to m elements
    return {tuple([bi] + [(-bs[0] if j == i else bj) % bi for (j, bj) in rest])
            for (i, bi) in rest if bi > 1}


assert eclatements((5, 3, 2, 1)) == {(2, 1, 1, 1), (3, 1, 2, 1)}


def lisse(bs):
    _, *t = bs
    return set(t) == {1}


assert lisse((2, 1, 1, 1))
assert not lisse((3, 1, 2, 1))


@cache
def isJStrict_(bs):
    # if lisse(bs):
    #     return True
    # if not all_coprime(bs):
    #     return False
    # return all(isJStrict(cs) for cs in eclatements(bs))
    stack = [bs]
    while len(stack) > 0:
        current = stack.pop()
        if not all_coprime(current):
            return False
        if not lisse(current):
            for cs in eclatements(current):
                stack.append(cs)
    return True


def isJStrict(bs):
    a, b, c = bs[:3]
    if a < b + c: # conjecture 2
        return False
    h, *t = bs
    ans = isJStrict_((h, *sorted(t)))
    if ans:
        # conjecture 1
        if a < (s := b + c + gcd(a - b, a - c)):
            assert s == a + 1
        # conjecture 3
        assert len([(p, q) for p in range(a)
                   for q in range(a) if p*b + q*c == a]) != 0
    return ans

assert isJStrict((2, 1, 1, 1))
assert isJStrict((3, 1, 2, 1))
assert isJStrict((5, 3, 2, 1))


@cache
def group(n: int):
    return [i for i in range(1, n) if coprime(n, i)]

