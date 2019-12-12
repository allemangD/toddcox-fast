from solver import Group


def A(n):
    """"""
    assert 0 <= n

    if n == 0:
        return Group(0)

    return Group.schlafli(*[3] * (n - 1))


def B(n):
    """Hypercube Irreducible Coxeter Group"""
    assert 2 <= n

    return Group.schlafli(4, *[3] * (n - 2))


def D(n):
    """Demicube Irreducible Coxeter Groups"""
    assert 4 <= n

    g = Group.schlafli(*[3] * (n - 2), 2)
    g[1, n - 1] = 3
    return g


def E(n):
    """E_6, E_7, and E_8 Irreducible Coxeter Groups"""
    assert 6 <= n <= 8

    g = Group.schlafli(*[3] * (n - 2), 2)
    g[2, n - 1] = 3
    return g


def F4():
    """24-cell Irreducible Coxeter Group"""

    return Group.schlafli(3, 4, 3)


def G2():
    """G2 Irreducible Coxeter Group"""

    return Group.schlafli(6)


def H(n):
    """Icosahedral Irreducible Coxeter Group"""
    assert 2 <= n <= 4

    return Group.schlafli(5, *[3] * (n - 2))


def I2(n):
    """Polygon Irreducible Coxeter Groups"""
    assert 2 <= n

    return Group.schlafli(n)


def T(n):
    """Toroidal Coxeter Group: I_2(n) x I_2(n)"""
    assert 2 <= n

    return I2(n) ** 2
