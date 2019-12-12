def cons(it, elem):
    yield from it
    yield elem


def ezmults(ngens, rels):
    mults = [[2] * ngens for _ in range(ngens)]

    for (f, t), m in rels:
        mults[f][t] = m
        mults[t][f] = m

    for i in range(ngens - 1):
        for j in range(i + 1, ngens):
            yield ((i, j), mults[i][j])


def schlafli(*mults):
    ngens = len(mults) + 1
    return ngens, ezmults(ngens, (((i, i + 1), mult) for i, mult in enumerate(mults)))


def torus(n):
    return schlafli(n, 2, n)


def cube(dim):
    return schlafli(4, *[3] * (dim - 2))


def icos(dim):
    assert 2 <= dim <= 4

    return schlafli(5, *[3] * (dim - 2))


def E(n):
    ngens, mults = schlafli(*[3] * (n - 2), 2)
    mults = cons(mults, ((2, n - 1), 3))
    return ngens, ezmults(ngens, mults)


if __name__ == '__main__':
    a, b = E(8)
    print(list(b))
