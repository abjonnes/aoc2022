from collections import defaultdict
from itertools import count, product


def parse_data(data):
    rocks = set()
    for line in data.split("\n"):
        if not line:
            continue

        points = [
            tuple(int(token) for token in pair.split(","))
            for pair in line.strip().split(" -> ")
        ]

        for point_a, point_b in zip(points, points[1:]):
            coords, depths = zip(point_a, point_b)
            start_coord, end_coord = sorted(coords)
            start_depth, end_depth = sorted(depths)

            rocks.update(
                product(
                    range(start_coord, end_coord + 1), range(start_depth, end_depth + 1)
                )
            )

    return rocks, max(depth for _, depth in rocks)


def part1(data):
    blocked, rock_depth = parse_data(data)

    def next_position():
        """Return the position of the next grain of sand by simulation, or
        `None` if it falls off the map.
        """
        depth = 0
        coord = 500
        while depth <= rock_depth:
            if (coord, depth + 1) not in blocked:
                depth += 1
            elif (coord - 1, depth + 1) not in blocked:
                coord -= 1
                depth += 1
            elif (coord + 1, depth + 1) not in blocked:
                coord += 1
                depth += 1
            else:
                return (coord, depth)

    for i in count():
        position = next_position()
        if not position:
            break
        blocked.add(position)

    return i


def part2(data):
    rocks, rock_depth = parse_data(data)

    # keys are depths, values are sets of coordinates occupied by sand
    sand = defaultdict(set)
    sand[0].add(500)

    # iterate from the top, where each grain of sand at a depth spawns three
    # directly beneath it, unless a position is blocked by rocks
    for idx in range(0, rock_depth + 1):
        for grain_coord in sand[idx]:
            sand[idx + 1].update(
                coord
                for coord in range(grain_coord - 1, grain_coord + 2)
                if (coord, idx + 1) not in rocks
            )

    return sum(len(grains) for grains in sand.values())
