DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def steps_from_data(data):
    tokens = data.split()
    for dir_, steps in zip(tokens[::2], tokens[1::2]):
        for _ in range(int(steps)):
            yield DIRS[dir_]


def steps_from_steps(steps):
    head = tail = (0, 0)
    visited = {tail}
    new_steps = list()

    for dx, dy in steps:
        # move the head knot
        head = (head[0] + dx, head[1] + dy)

        # calculate the x and y distance from the tail knot
        x_diff = head[0] - tail[0]
        y_diff = head[1] - tail[1]

        # if within 1 in both dimensions, the tail knot doesn't move
        if abs(x_diff) <= 1 and abs(y_diff) <= 1:
            continue

        # in either dimension, if the head knot is at a different position, the
        # tail moves 1 step towards it. the funny math just returns the "sign"
        # of the difference in position: +1, 0, or -1
        tail_dx = x_diff // (abs(x_diff) or 1)  # avoid division by 0
        tail_dy = y_diff // (abs(y_diff) or 1)

        tail = (tail[0] + tail_dx, tail[1] + tail_dy)
        visited.add(tail)
        new_steps.append((tail_dx, tail_dy))

    return new_steps, len(visited)


def run(data, n_following):
    # steps for the head knot comes from input data
    steps = steps_from_data(data)

    # the movement (steps) of following knots is generated from the movement of
    # the leading knot. repeat the generation of steps for every remaining knot
    # in the chain
    for _ in range(n_following):
        steps, n_visited = steps_from_steps(steps)
    return n_visited


def part1(data):
    return run(data, 1)


def part2(data):
    return run(data, 9)
