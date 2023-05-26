from math import gcd, prod
from tabulate import tabulate
from singularite import isJStrict, group, isJStrict_
from itertools import product


# print(isJ((7, 5, 3, 2)))
# print(all(map(isJ, gen_singularite())))

# for bs in gen_singularite(upto=50, m=2):
#     a, b, c = bs
#     s = b + c + gcd(a - b, a - c)
#     if a < s and (s == a + 1) != isJStrict(bs):
#         print(bs, s, s == a + 1, isJStrict(bs))

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


def is_nice3d(n: int):
    g = group(n)
    pts = [p for p in product(g, repeat=3) if isJStrict((n, *p))]
    phi = len(g)
    return len(pts) == 6*phi-8


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


def main():
    for n in range(2, 100):
        g = group(n)
        pts = [xs for xs in product(g, repeat=3) if isJStrict(n, xs)]
        print(n, len(pts))
        # for xs in pts:
        #     if isJStrict(n, xs):
        #         assert len([x for x in xs if x == 1]) >= 2

        # print(i, phi(i), is_nice(i), is_nice3d(i))
        # assert is_nice(i) == is_nice3d(i)
    print(isJStrict_.cache_info())


if __name__ == '__main__':
    main()

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
