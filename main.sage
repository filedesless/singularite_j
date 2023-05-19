def coprime(a, b):
    return gcd(a, b) == 1


def pairwise_coprime(xs):
    if xs:
        h, *t = xs
        return all(coprime(h, x) for x in t) and pairwise_coprime(t)
    return True


def solve(n, xs):
    ys = []
    for (i, a) in enumerate(xs):
        residues = [a] + [1] * i
        moduli = [n] + ys
        r = crt(residues, moduli)
        print(residues, moduli, r)
        ys.append(r)
    return ys


def speed(n, xs):
    if xs:
        h, *t = xs
        ys = [h]
        for x in t:
            y = x
            while not pairwise_coprime([y, *ys]):
                y += n
            ys.append(y)
        return ys
    return []


n = 20
# xs = [3, 7, 9]
xs = [9] * 20

assert all(coprime(n, x) for x in xs)
ys = speed(n, xs)
show(ys)
assert pairwise_coprime(ys)
