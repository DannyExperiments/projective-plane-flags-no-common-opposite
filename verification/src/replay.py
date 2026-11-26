"""Finite, exact checks of the construction and the low-order classifications."""

from itertools import combinations, product
from math import comb


def field_tables(order):
    if order == 4:
        # Encode a + b*t by a + 2*b, with t^2 = t + 1 over F_2.
        addition = [[a ^ b for b in range(4)] for a in range(4)]
        multiplication = [
            [0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]
        ]
    else:
        assert order in {2, 3, 5, 7, 11}
        addition = [[(a + b) % order for b in range(order)] for a in range(order)]
        multiplication = [[a * b % order for b in range(order)] for a in range(order)]
    return addition, multiplication


class Plane:
    def __init__(self, order):
        self.order = order
        add, mul = field_tables(order)
        self.coordinates = (
            [(1, a, b) for a, b in product(range(order), repeat=2)]
            + [(0, 1, a) for a in range(order)]
            + [(0, 0, 1)]
        )

        def incident(point, line):
            a, b, c = (mul[x][y] for x, y in zip(point, line))
            return add[add[a][b]][c] == 0

        self.on_line = [
            frozenset(i for i, point in enumerate(self.coordinates) if incident(point, line))
            for line in self.coordinates
        ]
        self.through = [
            frozenset(j for j, points in enumerate(self.on_line) if i in points)
            for i in range(len(self.coordinates))
        ]
        assert len(self.coordinates) == order ** 2 + order + 1
        assert all(len(points) == order + 1 for points in self.on_line + self.through)
        self.lines = set(self.on_line)
        self.pencils = set(self.through)
        self.flags = tuple(
            (point, line)
            for point, lines in enumerate(self.through)
            for line in sorted(lines)
        )
        self.flag_id = {flag: i for i, flag in enumerate(self.flags)}
        self.opposites = tuple(
            sum(
                1 << i
                for i, (other_point, other_line) in enumerate(self.flags)
                if other_point not in self.on_line[line] and other_line not in self.through[point]
            )
            for point, line in self.flags
        )

    def construction(self, line, missing, paired_point, center):
        flags = [(paired_point, line)]
        for point in self.on_line[line] - {missing}:
            through_both = self.through[center] & self.through[point]
            assert len(through_both) == 1
            join = next(iter(through_both))
            flags.append((center if point == paired_point else point, join))
        return tuple(sorted(self.flag_id[flag] for flag in flags))

    def verify_constructions(self):
        family = set()
        tested = 0
        for line, points in enumerate(self.on_line):
            for missing, paired_point in product(points, repeat=2):
                if missing == paired_point:
                    continue
                for center in range(len(self.coordinates)):
                    if center in points:
                        continue
                    flags = self.construction(line, missing, paired_point, center)
                    common = (1 << len(self.flags)) - 1
                    for flag in flags:
                        common &= self.opposites[flag]
                    assert common == 0
                    points_used, lines_used = map(frozenset, zip(*(self.flags[i] for i in flags)))
                    assert len(points_used) == len(lines_used) == self.order + 1
                    assert points_used not in self.lines and lines_used not in self.pencils
                    family.add(flags)
                    tested += 1
        expected = 56 if self.order == 2 else self.order ** 3 * (self.order + 1) * len(self.coordinates)
        assert len(family) == expected
        return tested, family

    def exhaust(self, anchor=None):
        if anchor is None:
            selections = combinations(range(len(self.flags)), self.order + 1)
        else:
            assert anchor == 0
            selections = ((anchor, *rest) for rest in combinations(range(1, len(self.flags)), self.order))
        found = set()
        for selection in selections:
            common = self.opposites[selection[0]]
            for flag in selection[1:]:
                common &= self.opposites[flag]
                if not common:
                    break
            if common:
                continue
            point_entries, line_entries = map(frozenset, zip(*(self.flags[i] for i in selection)))
            if point_entries not in self.lines and line_entries not in self.pencils:
                found.add(selection)
        return found

    def verify_coordinate_example(self):
        witness = (
            ((1, 0, 0), (0, 1, 0)), ((0, 1, 0), (0, 0, 1)),
            ((0, 0, 1), (1, 0, 0)), ((1, 0, 1), (1, 0, 2)),
        )
        selected = tuple(sorted(
            self.flag_id[self.coordinates.index(point), self.coordinates.index(line)]
            for point, line in witness
        ))
        m = self.coordinates.index((0, 1, 0))
        r = self.coordinates.index((1, 0, 2))
        a = self.coordinates.index((1, 0, 0))
        b = self.coordinates.index((0, 1, 0))
        assert selected == self.construction(m, r, a, b)
        uncovered = set(self.coordinates) - {
            self.coordinates[p] for i in selected for p in self.on_line[self.flags[i][1]]
        }
        assert uncovered == {(1, 1, 2), (1, 2, 2)}
        print("PG(2,3) coordinate example: 4 flags, 52 candidates, 2 uncovered points, 0 common opposites")


def main():
    for order in (2, 3, 4, 5, 7, 11):
        plane = Plane(order)
        tested, family = plane.verify_constructions()
        print(f"PG(2,{order}) constructions: {tested} quadruples, {len(family)} distinct qualifying sets")
        if order in {2, 3}:
            found = plane.exhaust()
            assert found == family
            print(f"PG(2,{order}) full search: {comb(len(plane.flags), order + 1)} subsets, {len(found)} qualifying")
        if order == 3:
            plane.verify_coordinate_example()
        if order == 4:
            found = plane.exhaust(anchor=0)
            assert found == {flags for flags in family if 0 in flags}
            # PGL(3,4) is transitive on incident point-line flags.
            total, remainder = divmod(len(found) * len(plane.flags), order + 1)
            assert remainder == 0 and total == len(family)
            print(
                f"PG(2,4) fixed-flag search: {comb(len(plane.flags) - 1, order)} subsets, "
                f"{len(found)} qualifying through the fixed flag, {total} total by flag transitivity"
            )
    print("All finite checks passed.")


if __name__ == "__main__":
    main()
