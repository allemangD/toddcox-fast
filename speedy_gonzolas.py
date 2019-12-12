from typing import List


class Cosets:
    def __init__(self, ngens, data=()):
        assert len(data) % ngens == 0, 'invalid length starting row'

        self.ngens = ngens
        self.data = list(data)
        self.len = len(data) // ngens

    def add_row(self):
        self.len += 1
        self.data.extend(-1 for _ in range(self.ngens))

    def put(self, idx, target):
        coset, gen = divmod(idx, self.ngens)
        self.data[idx] = target
        self.data[target * self.ngens + gen] = coset

    def get(self, idx):
        return self.data[idx]

    def __getitem__(self, key):
        coset, gen = key
        return self.data[coset * self.ngens + gen]

    def __setitem__(self, key, target):
        coset, gen = key
        self.data[coset * self.ngens + gen] = target
        self.data[target * self.ngens + gen] = coset

    def __len__(self):
        return self.len

    def __repr__(self):
        return '\n'.join(
            f'{i // self.ngens:>3} | ' +
            ' '.join(
                f'{e:>3}' for e in self.data[i:i + self.ngens])
            for i in range(0, len(self.data), self.ngens))


class RelTable:
    def __init__(self, gens: List[int], mul: int):
        self.gens = gens
        self.mul = mul

        self.fam = []
        self.gen = []
        self.lst = []

    def add_row(self):
        idx = len(self.fam)
        self.fam.append(-1)
        self.gen.append(-1)
        self.lst.append(-1)
        return idx


def solve(cosets: Cosets, rel_tables: List[RelTable]):
    if len(cosets) < 1:
        cosets.add_row()

    for rel in rel_tables:
        idx = rel.add_row()

        count = 0
        for g in rel.gens:
            if cosets.get(g) == 0:
                count += 1

        rel.fam[idx] = 0
        rel.gen[idx] = 0
        rel.lst[idx] = 0

        if count == 1:
            rel.gen[idx] = -1

    idx = 0
    while True:
        while idx < len(cosets.data) and cosets.get(idx) >= 0:
            idx += 1

        if idx == len(cosets.data):
            break

        coset, gen = divmod(idx, cosets.ngens)
        target = len(cosets)

        cosets.add_row()

        for rel in rel_tables:
            rel.add_row()

        facts = [(coset, gen)]

        while facts:
            coset, gen = facts.pop()
            cosets[coset, gen] = target

            for rel in rel_tables:
                if gen in rel.gens and rel.fam[target] == -1:
                    rel.fam[target] = rel.fam[coset]
                    rel.gen[target] = rel.gen[coset] + 1

                    if rel.gen[coset] < 0:
                        rel.gen[target] -= 2

                    if rel.gen[target] == rel.mul:  # forward learn
                        lst = rel.lst[rel.fam[target]]
                        gen_ = rel.gens[rel.gens[0] == gen]
                        facts.append((lst, gen_))
                    elif rel.gen[target] == -rel.mul:  # stationary learn
                        gen_ = rel.gens[rel.gens[0] == gen]
                        facts.append((target, gen_))
                    elif rel.gen[target] == rel.mul - 1:
                        rel.lst[rel.fam[target]] = target

            facts.sort(reverse=True)

        for rel in rel_tables:
            if rel.fam[target] == -1:
                rel.fam[target] = target
                rel.gen[target] = 0

                count = 0
                for g in rel.gens:
                    if cosets[target, g] == target:
                        count += 1

                if count == 1:
                    rel.gen[target] = -1


if __name__ == '__main__':
    # cosets = Cosets(3)
    # mults = [((0, 1), 50000), ((1, 2), 2), ((0, 2), 2)]

    cosets = Cosets(4)
    n = 100
    mults = [((0, 1), 5), ((1, 2), 3), ((2, 3), 3),
             ((0, 2), 2), ((1, 3), 2), ((0, 3), 2)]

    rel_tables = [RelTable(*args) for args in mults]

    solve(cosets, rel_tables)

    print(len(cosets))
    if len(cosets) < 20:
        print(cosets)
    else:
        print('--')
