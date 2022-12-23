from collections import defaultdict
from itertools import product
from re import findall


def parse_data(data):
    board, steps = data.split("\n\n")

    walls = set()
    for r, line in enumerate(board.split("\n")):
        if not line:
            continue
        for c, char in enumerate(line):
            if char == "#":
                walls.add((r, c))

    steps = [
        (int(steps), turn or None) for steps, turn in findall(r"(\d+)(R|L|$)", steps)
    ]

    return walls, steps


# map of facing to (change in r, change in c) for each step
FACINGS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}

# this is specific to the user's input :(
START_SECTOR = 1


class Board:
    def __init__(self, walls, dim, transitions):
        self.walls = walls
        self.dim = dim

        # when we walk off the edge of a sector, this mapping from
        # (current_sector, facing) to (n_turns, new_sector) tells us which new
        # sector we've walked into, and how many left-hand turns the board
        # makes under us as we do so - essentially, this fully specifies the
        # sector-edge connectivity
        self.transitions = transitions

    def _sector(self, pos):
        """Calculate the sector of a position, where the sector is one of the
        six square regions. The sectors are labeled with 0-based row and column
        indices.
        """
        r, c = pos
        return 3 * (r // self.dim) + c // self.dim

    def _reorient(self, pos, facing, current_sector):
        """Calculates a new position and new facing when moving between
        sectors.
        """
        n_turns, new_sector = self.transitions[current_sector, facing]

        # n_turns is the number of left-hand turns that the board makes under
        # our feet as we enter a new sector - each turn moves our relative
        # facing to the _right_, and modifies our row/column indices
        for _ in range(n_turns):
            facing = (facing + 1) % 4
            pos = pos[1], self.dim - 1 - pos[0]

        # compute a new position relative to this new sector
        return (
            self.dim * (new_sector // 3) + pos[0] % self.dim,
            self.dim * (new_sector % 3) + pos[1] % self.dim,
        ), facing

    def move(self, pos, steps, facing):
        """Move a certain number of steps with the given facing, or until a
        wall is reached.
        """
        # keep track of which sector we're in so when know when to reorient
        current_sector = self._sector(pos)
        new_facing = facing

        for step in range(steps):
            dr, dc = FACINGS[facing]

            # note that if our new position is outside of the current sector,
            # the calculated sector may not exist if we stepped into empty
            # space on the board, but that's okay because we're only using this
            # as a check to see if we need to compute a new position based on
            # the sector connectivity
            new_pos = (pos[0] + dr, pos[1] + dc)
            new_sector = self._sector(new_pos)

            # if this step moves us out of our sector, we potentially need to
            # reorient ourselves and move into a new sector
            if new_sector != current_sector:
                new_pos, new_facing = self._reorient(new_pos, facing, current_sector)
                current_sector = self._sector(new_pos)

            if new_pos in self.walls:
                break

            pos, facing = new_pos, new_facing

        return pos, facing


def run(data, transitions):
    walls, steps = parse_data(data)

    board = Board(walls, 50, transitions)

    pos = (50 * (START_SECTOR // 3), 50 * START_SECTOR)
    facing = 0
    for steps, turn in steps:
        pos, facing = board.move(pos, steps, facing)

        if turn:
            facing = (facing + (1 if turn == "R" else -1)) % 4

    r, c = pos
    return 1000 * (r + 1) + 4 * (c + 1) + facing


def part1(data):
    # specific to user's input :(
    transitions = {
        (1, 0): (0, 2),
        (1, 1): (0, 4),
        (1, 2): (0, 2),
        (1, 3): (0, 7),
        (2, 0): (0, 1),
        (2, 1): (0, 2),
        (2, 2): (0, 1),
        (2, 3): (0, 2),
        (4, 0): (0, 4),
        (4, 1): (0, 7),
        (4, 2): (0, 4),
        (4, 3): (0, 1),
        (6, 0): (0, 7),
        (6, 1): (0, 9),
        (6, 2): (0, 7),
        (6, 3): (0, 9),
        (7, 0): (0, 6),
        (7, 1): (0, 1),
        (7, 2): (0, 6),
        (7, 3): (0, 4),
        (9, 0): (0, 9),
        (9, 1): (0, 6),
        (9, 2): (0, 9),
        (9, 3): (0, 6),
    }

    return run(data, transitions)


def part2(data):
    # specific to user's input :(
    transitions = {
        (1, 0): (0, 2),
        (1, 1): (0, 4),
        (1, 2): (2, 6),
        (1, 3): (1, 9),
        (2, 0): (2, 7),
        (2, 1): (1, 4),
        (2, 2): (0, 1),
        (2, 3): (0, 9),
        (4, 0): (3, 2),
        (4, 1): (0, 7),
        (4, 2): (3, 6),
        (4, 3): (0, 1),
        (6, 0): (0, 7),
        (6, 1): (0, 9),
        (6, 2): (2, 1),
        (6, 3): (1, 4),
        (7, 0): (2, 2),
        (7, 1): (1, 9),
        (7, 2): (0, 6),
        (7, 3): (0, 4),
        (9, 0): (3, 7),
        (9, 1): (0, 2),
        (9, 2): (3, 1),
        (9, 3): (0, 6),
    }

    return run(data, transitions)
