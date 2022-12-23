from collections import Counter
from itertools import count, product


def parse_data(data):
    return {
        (r, c)
        for r, row in enumerate(data.split())
        for c, char in enumerate(row)
        if char == "#"
    }


# map of direction indicator to (vertical, change in row or col)
DIRECTIONS = {"N": (True, -1), "S": (True, 1), "W": (False, -1), "E": (False, 1)}
ORDER = ("N", "S", "W", "E")


def timestep(elves, t):
    proposals = dict()

    # first half of the round
    for elf in elves:
        r, c = elf

        # if all the surrounding spots are empty, don't move
        if all(
            (r + dr, c + dc) not in elves
            for dr, dc in product((-1, 0, 1), repeat=2)
            if (dr, dc) != (0, 0)
        ):
            continue

        # consider each direction in the prescribed order
        for direction_idx in range(4):
            vertical, delta = DIRECTIONS[ORDER[(t + direction_idx) % 4]]

            # check the three spots in this direction
            candidates = [
                (r + delta, c + dcr) if vertical else (r + dcr, c + delta)
                for dcr in (-1, 0, 1)
            ]

            # if any of them are occupied, bail on this direction
            if any(candidate in elves for candidate in candidates):
                continue

            # otherwise, propose moving in this direction and don't consider
            # any other directions
            proposals[elf] = (r + delta, c) if vertical else (r, c + delta)
            break

    # find which sites are proposed by more than one elf
    conflicts = {
        site for site, count in Counter(proposals.values()).items() if count > 1
    }

    # an elf moves to its proposed location if _has_ a proposed location and it
    # was the only elf to propose it, otherwise it stays put
    return {
        proposals[elf] if elf in proposals and proposals[elf] not in conflicts else elf
        for elf in elves
    }


def run(data, time=None):
    elves = parse_data(data)

    for t in count():
        new_elves = timestep(elves, t)
        if new_elves == elves or (time and t == time - 1):
            return new_elves, t + 1
        elves = new_elves


def part1(data):
    elves, _ = run(data, 10)
    rows, cols = zip(*elves)
    return (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1) - len(elves)


def part2(data):
    _, t = run(data)
    return t
