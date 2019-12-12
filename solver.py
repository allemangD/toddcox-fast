from typing import List


def cons(it, elem):
    yield from it
    yield elem


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


class Group:
    def __init__(self, ngens, rels=()):
        self._mults = [[2] * ngens for _ in range(ngens)]

        for (f, t), m in rels:
            self._mults[f][t] = m
            self._mults[t][f] = m

        self.ngens = ngens

    @property
    def mults(self):
        for i in range(self.ngens - 1):
            for j in range(i + 1, self.ngens):
                yield ((i, j), self._mults[i][j])

    def __setitem__(self, key, value):
        f, t = key
        self._mults[f][t] = value
        self._mults[t][f] = value

    def __mul__(self, other):
        assert isinstance(other, Group)
        off = self.ngens

        g = Group(self.ngens + other.ngens)

        for (i, j), m in self.mults:
            g[i, j] = m

        for (i, j), m in other.mults:
            g[off + i, off + j] = m

        return g

    def __pow__(self, p, modulo=None):
        if modulo is not None: raise NotImplemented

        assert isinstance(p, int), 'p must be an integer'
        assert p >= 0, 'p must be a nonnegative integer'

        g = Group(self.ngens * p)

        for (i, j), m in self.mults:
            for off in range(0, g.ngens, self.ngens):
                g[off + i, off + j] = m

        return g

    @classmethod
    def schlafli(cls, *mults):
        ngens = len(mults) + 1
        return Group(ngens, (((i, i + 1), mult) for i, mult in enumerate(mults)))

    def solve(self, sub_gens=()):
        initial_row = [-1] * self.ngens
        for s in sub_gens:
            initial_row[s] = 0

        cosets = Cosets(self.ngens, initial_row)
        rel_tables = [RelTable(*a) for a in self.mults]

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

        return cosets
