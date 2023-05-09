from math import gcd, prod
from typing import List
from functools import cache
from primes import is_prime, prime_fact
from tabulate import tabulate
import matplotlib.pyplot as plt


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
    h, *t = bs
    ans = isJStrict_((h, *sorted(t)))
    a, b, c = bs
    if ans:
        # conjecture 1
        if a < (s := b + c + gcd(a - b, a - c)):
            assert s == a + 1
        # conjecture 2
        assert a >= b + c
        # conjecture 3
        assert len([(p, q) for p in range(a)
                   for q in range(a) if p*b + q*c == a]) != 0
    return ans


# assert isJStrict((2, 1, 1, 1))
# assert isJStrict((3, 1, 2, 1))
# assert isJStrict((5, 3, 2, 1))


def divisors(n: int):
    return set(prime_fact(n).keys())

# print(isJ((7, 5, 3, 2)))
# print(all(map(isJ, gen_singularite())))

# for bs in gen_singularite(upto=50, m=2):
#     a, b, c = bs
#     s = b + c + gcd(a - b, a - c)
#     if a < s and (s == a + 1) != isJStrict(bs):
#         print(bs, s, s == a + 1, isJStrict(bs))


@cache
def group(n: int):
    return [i for i in range(1, n) if coprime(n, i)]


# count type J of the form (n, _, _)
def count(n: int):
    elem = group(n)
    # expect = {(i, j) for i in elem for j in elem
    #           if 1 in {i, j} or i + j == n}
    actual = [(i, j) for i in elem for j in elem if isJStrict((n, i, j))]
    # return expect == actual
    return len(actual)


# count elements "inside" the triangle
def count2(n: int):
    return count(n) - 3*(phi(n) - 1)

# empty triangle


def is_nice(n: int):
    return count2(n) == 0


def show(n: int):
    header = group(n)
    rows = [[(str(s) if n < (s := a + b + gcd(n - a, n - b)) else 'X') if isJStrict((n, a, b)) else ' '
             for b in header]
            for a in header]
    print(tabulate(rows, headers=[n]+header,
                   showindex=header, tablefmt='simple_grid',
                   numalign='center', stralign='center'))


def phi(n: int):
    return len(group(n))


for i in range(2, 20):
    # print(i, is_nice(i))
    show(i)

# for n in range(1000):
#     if is_nice(n):
#         print(n, phi(n))

# l = sorted([(n, phi(n))
#            for n in range(2, 200) if is_nice(n)], key=lambda t: t[1])
# for i in l:
#     print(i)

# bag = set()
# for n in range(2, 100):
#     if phi(n) == 20:
#         show(n)
#         header = group(n)
#         for (_, a, b) in {(n, a, b) for a in header for b in header}:
#             if isJStrict((n, a, b)):
#                 bag.add((a, b))

# rows = [['X' if (a, b) in bag else ' ' for b in header]
#         for a in header]
# print(tabulate(rows, headers=[' ']+header,
#                showindex=header, tablefmt='simple_grid',
#                numalign='center', stralign='center'))

# print(bag)
# _, axs = plt.subplots(1, 3)
# x = list(range(2, 100))
# phis = [phi(n) for n in x]
# axs[0].plot(x, phis)
# axs[0].set_title("phi")
# counts = [count(i) for i in x]
# axs[1].plot(x, counts)
# axs[1].set_title("#J total")
# counts2 = [count2(i) for i in x]
# axs[2].plot(x, counts2)
# axs[2].set_title("#J inside")
# plt.show()

# for n in range(2, 20):
#     print(n, count(n))

# print(show(7))
# print(isJStrict.cache_info())

# print('some JStrict')
# for bs in gen_singularite(upto=20, m=2):
#     # print(bs, isJStrict(bs))
#     a, b, c = bs
#     s, p = b + c, b * c
#     if isJStrict(bs) != conjecture(bs):
#         print(bs, isJStrict(bs), conjecture(bs))

# if c > 1:
# print(bs, (a+b) % c, (a+c) % b, (b+c) % a, isJStrict(bs))
#     print(bs)
# print((a+b) % c, all_coprime((a, b, c, (a+b) % c)))
# print((b+c) % a, all_coprime((a, b, c, (b+c) % a)))
# if (-a) % b % c != 0 and (-a) % c % b != 0:
# print([i for i in range(a) if gcd(a, i) == 1])
# print(bs, (-a) % b % c, (-a) % c % b)

# print('some non-JStrict')
# Here are the elements of S_2 with b0 up to 10 that are not JStrict
# for bs in gen_singularite(upto=10, m=2):
#     if not isJStrict(bs):
#         print(bs)

# input()
# print('some pyt')
# checking wether pythagorean triples are JStrict
# for bs in gen_singularite(upto=100, m=2):
#     (a, b, c) = bs
#     if a*a == b*b+c*c:
#         print(bs, isJStrict(bs), coprime(b, c))
# if a*a == b*b + c*c:
#     print(bs, isJStrict(bs))
