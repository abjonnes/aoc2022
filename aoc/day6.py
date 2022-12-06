from itertools import count


def run(data, n):
    for i in count(start=n):
        if len(set(data[i - n : i])) == n:
            return i


def part1(data):
    return run(data, 4)


def part2(data):
    return run(data, 14)
