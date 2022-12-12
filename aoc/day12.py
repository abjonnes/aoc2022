from itertools import product
from string import ascii_lowercase


HEIGHTS = {char: height for height, char in enumerate(ascii_lowercase)}
HEIGHTS["S"] = 0
HEIGHTS["E"] = 25


def find(map_, start_char, target_char, reverse=False):
    width = len(map_)
    height = len(map_[0])

    start = next(
        (i, j)
        for i, row in enumerate(map_)
        for j, char in enumerate(row)
        if char == start_char
    )

    def get_neighbors(pos):
        i, j = pos
        candidates = [
            (i + 1, j),
            (i - 1, j),
            (i, j + 1),
            (i, j - 1),
        ]
        return [(i, j) for i, j in candidates if 0 <= i < width and 0 <= j < height]

    def valid_heights(site, neighbor):
        if reverse:
            site, neighbor = neighbor, site
        return (
            HEIGHTS[map_[site[0]][site[1]]] + 1
            >= HEIGHTS[map_[neighbor[0]][neighbor[1]]]
        )

    # Dijkstra's algorithm
    # width * height is just a value guaranteed to be larger than any result path length
    distances = {pos: width * height for pos in product(range(width), range(height))}
    distances[start] = 0

    while distances:
        site = min(distances, key=distances.__getitem__)
        site_distance = distances.pop(site)

        if map_[site[0]][site[1]] == target_char:
            return site_distance

        for neighbor in get_neighbors(site):
            if not valid_heights(site, neighbor) or neighbor not in distances:
                continue
            distances[neighbor] = min(distances[neighbor], site_distance + 1)


def part1(data):
    return find(data.split(), "S", "E")


def part2(data):
    return find(data.split(), "E", "a", reverse=True)
