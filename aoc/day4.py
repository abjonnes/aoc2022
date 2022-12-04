def parse_ranges(ranges):
    for range_ in ranges:
        if not range_:
            continue
        range1, range2 = range_.split(",")
        range1 = [int(x) for x in range1.split("-")]
        range2 = [int(x) for x in range2.split("-")]
        yield range1, range2


def part1(data):
    return sum(
        start1 <= start2 and end1 >= end2 or start2 <= start1 and end2 >= end1
        for (start1, end1), (start2, end2) in parse_ranges(data.split("\n"))
    )


def part2(data):
    return sum(
        end1 >= start2 and end2 >= start1
        for (start1, end1), (start2, end2) in parse_ranges(data.split("\n"))
    )
