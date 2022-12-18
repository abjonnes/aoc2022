from itertools import cycle
from functools import cached_property


class Block:
    def __init__(self, coords):
        self.coords = coords

    def positions(self, x, y):
        """Generates the positions occupied by the block relative to the given point."""
        yield from ((x + coord_x, y - coord_y) for coord_x, coord_y in self.coords)

    def check(self, x, y, occupied):
        """Returns `True` if the block fits in the given position."""
        return (
            0 <= x <= 7 - self.width
            and 0 <= y - self.height + 1
            and not any(pos in occupied for pos in self.positions(x, y))
        )

    @cached_property
    def height(self):
        return max(y for _, y in self.coords) + 1

    @cached_property
    def width(self):
        return max(x for x, _ in self.coords) + 1


BLOCK1 = Block(((0, 0), (1, 0), (2, 0), (3, 0)))
BLOCK2 = Block(((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)))
BLOCK3 = Block(((0, 2), (1, 2), (2, 0), (2, 1), (2, 2)))
BLOCK4 = Block(((0, 0), (0, 1), (0, 2), (0, 3)))
BLOCK5 = Block(((0, 0), (0, 1), (1, 0), (1, 1)))


def stack_hash(occ, height):
    """Calculates a unique value for the stack which considers all positions which are _reachable_
    from the top. Anything "unreachable" has no impact on the repeating pattern.
    """
    # graph search to find all "reachable" positions
    seen = set()
    x = 0
    y = min_y = height + 1  # start just above the height of the stack
    to_visit = {(x, y)}
    while to_visit:
        pos = to_visit.pop()
        seen.add((pos[0], pos[1] - height))

        if pos[0] + 1 < 7 and (pos[0] + 1, pos[1]) not in occ:
            to_visit.add((pos[0] + 1, pos[1]))

        if (pos[0], pos[1] - 1) not in occ and pos[1] > 0:
            to_visit.add((pos[0], pos[1] - 1))

    return hash(frozenset(seen))


def run(data, n):
    blocks = cycle(enumerate((BLOCK1, BLOCK2, BLOCK3, BLOCK4, BLOCK5)))

    data = data.strip()
    gusts = cycle(enumerate(1 if char == ">" else -1 for char in data))

    # we maintain a cache of encountered states (block index, gust index, and stack configuration)
    # and associated heights, so that if we come across a state that we've seen before, we know
    # we're in a repeating pattern and can calculate its height
    cache = dict()

    heights = list()
    occupied = set()
    height = -1  # 0-based height of stack
    gust_idx = None
    for idx, (block_idx, block) in enumerate(blocks):
        if idx == n:
            return heights[-1]

        # check cache
        stack_configuration = stack_hash(occupied, height)
        cache_hit = cache.get((stack_configuration, block_idx, gust_idx))

        if cache_hit:
            previous_idx, previous_height = cache_hit

            # number of blocks and height added in each repeating unit
            repeat_idx = idx - previous_idx
            repeat_height = height - previous_height

            # calculate how many additional repeating units are required
            remaining_blocks = n - idx
            added_repeats = remaining_blocks // repeat_idx

            # calculate index into list of encountered heights based on repeating pattern
            height_idx = (
                remaining_blocks - 1 - added_repeats * repeat_idx + previous_idx
            )

            # +1 here because we've already gone through one repeating unit
            return heights[height_idx] + (1 + added_repeats) * repeat_height

        cache[stack_configuration, block_idx, gust_idx] = (idx, height)

        # simulation of falling blocks
        x = 2
        y = height + block.height + 3

        while True:
            gust_idx, dx = next(gusts)
            if block.check(x + dx, y, occupied):
                x += dx

            if block.check(x, y - 1, occupied):
                y -= 1
            else:
                positions = list(block.positions(x, y))
                height = max(height, *(y for _, y in positions))
                occupied.update(positions)
                break

        heights.append(height + 1)


def part1(data):
    return run(data, 2022)


def part2(data):
    return run(data, 1000000000000)
