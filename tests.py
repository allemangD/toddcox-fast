import time

import groups

if __name__ == '__main__':
    g = groups.T(100)

    s = time.time()
    table = g.solve()
    e = time.time()

    print(f'elapsed = {e - s:.3g}s')

    print(len(table))
    if len(table) < 20:
        print(table)
