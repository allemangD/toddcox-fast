from time import time

from groups import *

if __name__ == '__main__':
    gs = [
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

# group, cosets, time, speed
# T(50), 10,000, 0.0751, 1.3e+05
# T(100), 40,000, 0.304, 1.3e+05
# T(150), 90,000, 0.688, 1.3e+05
# T(200), 160,000, 1.21, 1.3e+05
# T(250), 250,000, 1.89, 1.3e+05
# B(5), 3,840, 0.0495, 7.8e+04
# H(4), 14,400, 0.11, 1.3e+05
# B(6), 46,080, 0.837, 5.5e+04
# E(6), 51,840, 0.944, 5.5e+04
# B(7), 645,120, 17.2, 3.7e+04
# E(7), 2,903,040, 79.4, 3.7e+04
