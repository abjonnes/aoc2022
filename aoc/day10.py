from itertools import count, islice


def get_signals(data):
    x = 1
    counter = count(start=1)
    for line in (line.strip() for line in data.split("\n")):
        if line == "noop":
            yield next(counter), x
        elif line.startswith("addx"):
            yield next(counter), x
            yield next(counter), x
            x += int(line[5:])


def part1(data):
    return sum(
        cycle * signal for cycle, signal in islice(get_signals(data), 19, None, 40)
    )


def part2(data):
    return "".join(
        ("#" if abs((cycle - 1) % 40 - signal) <= 1 else ".")
        + ("" if cycle % 40 else "\n")
        for cycle, signal in get_signals(data)
    )
