from itertools import product


def parse_data(data):
    return {tuple(int(x) for x in line.split(",")) for line in data.split()}


def area(grid):
    """Counts how many neighbors are empty space for each voxel in the grid."""

    def neighbor_empty(voxel, dim, dx):
        voxel = list(voxel)
        voxel[dim] += dx
        return tuple(voxel) not in grid

    return sum(neighbor_empty(*args) for args in product(grid, range(3), (-1, 1)))


def part1(data):
    return area(parse_data(data))


def part2(data):
    grid = parse_data(data)

    def find_bounds(dim):
        """Return lower and upper bounds of the grid for the given dimension, with 1 unit of
        padding.
        """
        values = {voxel[dim] for voxel in grid}
        return min(values) - 1, max(values) + 1

    bounds = [find_bounds(dim) for dim in range(3)]

    # DFS to find all "air-accessible" positions on the perimeter of the grid starting from an
    # air-occupied corner of the bounding box
    start = tuple(bound[0] for bound in bounds)
    queue = [start]
    accessible = {start}

    while queue:
        voxel = queue.pop()
        for dim, dx in product(range(3), (-1, 1)):
            test_voxel = list(voxel)
            test_voxel[dim] += dx
            test_voxel = tuple(test_voxel)
            if (
                # ensure neighbor is within bounds
                not all(
                    lower_bound <= pos <= upper_bound
                    for pos, (lower_bound, upper_bound) in zip(test_voxel, bounds)
                )
                # and not in the grid or one we've already seen
                or test_voxel in grid | accessible
            ):
                continue

            queue.append(test_voxel)
            accessible.add(test_voxel)

    # construct a new "filled" grid by starting with a solid rectangular prism and subtracting out
    # the "air-accessible" locations - this is equivalent to the starting grid with the closed
    # cavities filled in
    filled_grid = set(product(*[range(*bound) for bound in bounds])) - accessible

    return area(filled_grid)
