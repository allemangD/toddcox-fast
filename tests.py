import math
from time import time

from groups import *


def perm(a, b):
    return math.factorial(a) // math.factorial(b)


def simple_n_gens(n: int, p: int):
    """
    :param n: Maximum number of generators
    :param p: Order of root I2
    """

    return [
        (f'{g} gens', I2(n * perm(p - 1, g - 1)) * A(g - 2))
        for g in range(2, p)
    ]


if __name__ == '__main__':
    # benchmark with increasing number of generators
    gs = simple_n_gens(2, 9)

    # benchmark original groups
    gs += [
        ('T(50)', T(50)),
        ('T(100)', T(100)),
        ('T(150)', T(150)),
        ('T(200)', T(200)),
        ('T(250)', T(250)),
        ('B(5)', B(5)),
        ('H(4)', H(4)),
        ('B(6)', B(6)),
        ('E(6)', E(6)),
        ('B(7)', B(7)),
        ('E(7)', E(7)),
    ]

    print('group, cosets, time, speed')
    for name, g in gs:
        s = time()
        result = g.solve()
        e = time()

        cosets = len(result)
        diff = e - s
        speed = cosets / diff

        print(f'{name}, {cosets :,}, {diff:,.3g}, {speed:,.2g}')
