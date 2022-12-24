from collections import defaultdict
from heapq import heappop, heappush
from itertools import product
from functools import cache
from math import lcm


def parse_data(data):
    dir_map = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    # map of direction (in dr, dc format) to list of starting positions for
    # blizzards moving in that direction
    blizzards = defaultdict(list)

    height = width = 0
    for r, row in enumerate(data.split()[1:-1]):
        for c, char in enumerate(row[1:-1]):
            width = max(width, c + 1)
            if char == ".":
                continue
            blizzards[dir_map[char]].append((r, c))
        height = max(height, r + 1)

    return blizzards, height, width


def run(data, n):
    blizzards, height, width = parse_data(data)

    # the blizzard pattern repeats this often
    period = lcm(height, width)

    start = (-1, 0)
    target = (height, width - 1)

    @cache
    def open_positions(t, rotated=False):
        """Returns positions on the map which are available to be moved into.
        The time parameter must be modulo the period - can't do that operation
        in this method because it would break the cache. If rotated is True,
        "rotate" the map by 180 degrees, so when we're backtracking, we can
        simply treat the end as the start and vice versa.
        """
        if rotated:
            return {
                (height - r - 1, width - c - 1) for r, c in open_positions(t, False)
            }

        # start with the full rectangle and subtract out positions occupied by
        # blizzards
        positions = set(product(range(height), range(width)))
        for (dr, dc), dir_blizzards in blizzards.items():
            positions -= {
                ((r + dr * t) % height, (c + dc * t) % width) for r, c in dir_blizzards
            }

        # add in the start and end positions since they are outside the
        # rectangle but still legal
        positions |= {start, target}

        return positions

    #######################
    ### A* pathfinding! ###
    ######################

    # treat this as a 4D map, where the third dimension is time and wraps
    # around every `period` steps (since the board changes over time through
    # blizzards at that period) and the fourth "dimension" is the index of the
    # trip: 0 for the first trek across the board, 1 for the second, etc. if
    # we've reached the target but have more treks to do, we can rotate the
    # board 180 degrees so that we're at the start again, and just make another
    # pass - the next trek is the same process, only now the blizzards are rotated!

    # f-scores is a min-heap which will store, for each 4D point, the current
    # best-guess of the ultimate cost of a path through the point: use 1 -
    # Manhattan distance from the start (accounting for the "trip index") as
    # the heuristic since the goal is always the furthest point from the
    # starting position as possible. this heuristic will never overestimate the
    # real cost, so we're guaranteed to find the shortest path
    f_scores = [(1, (start, 0, 0))]

    # g-scores is a mapping of 4D point to lowest cost path to the point
    # currently known
    g_scores = defaultdict(lambda: height * width * period * n)
    g_scores[start, 0, 0] = 0

    queue = {(start, 0, 0)}
    while queue:
        f_score, (pos, t, trek) = heappop(f_scores)
        queue.remove((pos, t, trek))

        next_trek = trek
        if pos == target:
            next_trek += 1
            if next_trek == n:
                break

        # if we've reached the target, rotate back to the start and find
        # available neighboring spots from there
        r, c = start if pos == target else pos

        next_t = (t + 1) % period

        for next_pos in {
            (r, c),
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1),
        } & open_positions(next_t, bool(next_trek % 2)):
            next_r, next_c = next_pos

            # if this is a new fastest path to the neighboring spot, update the
            # g-score of this 4D point, calculate its f-score (estimated
            # ultimate cost of a path through this 4D point), and add it to the
            # queue
            trial_g_score = g_scores[pos, t, trek] + 1
            if trial_g_score < g_scores[next_pos, next_t, next_trek]:
                heappush(
                    f_scores,
                    (
                        trial_g_score
                        - next_r  # Manhattan distance
                        - next_c
                        - height * width * next_trek,  # trek adjustment
                        (next_pos, next_t, next_trek),
                    ),
                )
                g_scores[next_pos, next_t, next_trek] = trial_g_score
                queue.add((next_pos, next_t, next_trek))

    # the real cost of the final 4D point
    return g_scores[pos, t, trek]


def part1(data):
    return run(data, 1)


def part2(data):
    return run(data, 3)
