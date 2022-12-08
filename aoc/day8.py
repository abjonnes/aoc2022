from collections import defaultdict


def parse_data(data):
    return [[int(x) for x in row.strip()] for row in data.split()]


def apply_by_direction(data, func, initial_value):
    """Applies a function to the data in all four directions, collecting the results in an
    accumulator dictionary with a given initial value.
    """
    accumulator = defaultdict(lambda: initial_value)

    for row_idx, row in enumerate(data):
        # left to right
        func(row, accumulator, lambda col_idx: (row_idx, col_idx))

        # right to left
        func(
            reversed(row),
            accumulator,
            lambda col_idx: (row_idx, len(row) - col_idx - 1),
        )

    for col_idx, col in enumerate(
        [row[i] for row in data] for i in range(len(data[0]))
    ):
        # up to down
        func(col, accumulator, lambda row_idx: (row_idx, col_idx))

        # down to up
        func(
            reversed(col),
            accumulator,
            lambda row_idx: (len(col) - row_idx - 1, col_idx),
        )

    return accumulator


def part1(data):
    data = parse_data(data)

    def mark_visible(seq, visible, key_func):
        max_ = -1

        for idx, tree in enumerate(seq):
            # a tree is visible if it's taller than any other tree already encountered in this
            # direction
            visible[key_func(idx)] |= tree > max_

            max_ = max(max_, tree)

    is_visible = apply_by_direction(data, mark_visible, False)

    return sum(is_visible.values())


def part2(data):
    data = parse_data(data)

    def multiply_visibility(seq, visible_product, key_func):
        # trees on edges can't see any trees in this direction
        visible_product[key_func(0)] *= 0

        idx_by_height = {idx: 0 for idx in range(10)}

        for idx, tree in enumerate(seq):
            # don't care about the edge trees
            if not idx:
                continue

            # multiply in the number of trees visible in this direction from
            # this tree
            visible_product[key_func(idx)] *= idx - idx_by_height[tree]

            # update the index of the most recent tree of at most a given
            # height in this direction
            for height in range(tree + 1):
                idx_by_height[height] = idx

    visible_trees = apply_by_direction(data, multiply_visibility, 1)

    return max(visible_trees.values())
