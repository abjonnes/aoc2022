import re


def parse_data(data):
    for line in data.split("\n"):
        if not line:
            continue
        x1, y1, x2, y2 = [int(token) for token in re.findall(r"-?\d+", line)]
        yield (x1, y1), (x2, y2)


class Sensor:
    def __init__(self, pos, beacon_pos):
        self.pos = pos
        self.distance = abs(pos[0] - beacon_pos[0]) + abs(pos[1] - beacon_pos[1])

    def width(self, y):
        return self.distance - abs(self.pos[1] - y)

    def overlaps(self, y):
        return self.width(y) > 0

    def interval(self, y):
        """Returns the start and end of the range of x positions covered by
        this sensor at the given y position.
        """
        return (self.pos[0] - self.width(y), self.pos[0] + self.width(y))


def part1(data):
    target = 2000000

    sensors, beacons = zip(*parse_data(data))
    sensors = [Sensor(*x) for x in zip(sensors, beacons)]

    covered = set()
    for sensor in sensors:
        if not sensor.overlaps(target):
            continue

        interval = sensor.interval(target)
        covered.update(range(interval[0], interval[1] + 1))

    beacons_at_target = {x for x, y in beacons if y == target}
    return len(covered - beacons_at_target)


def part2(data):
    sensors, beacons = zip(*parse_data(data))
    sensors = [Sensor(*x) for x in zip(sensors, beacons)]

    def gap(intervals):
        """Return the gap in the intervals, if present. Assumes only one such
        gap may exist.
        """
        intervals = sorted(intervals)

        if not intervals:
            return

        last_end = max(intervals[0][-1], 0)
        for interval in intervals[1:]:
            # `interval` is subsumed by the intervals already encountered
            if interval[1] < last_end:
                continue

            # `interval` starts too far after the previously seen intervals end
            # gap!
            if interval[0] > last_end + 1:
                return last_end + 1

            last_end = interval[1]
            if last_end > 4000000:
                return

    for y in range(4000001):
        x_gap = gap(sensor.interval(y) for sensor in sensors if sensor.overlaps(y))

        if x_gap is not None:
            return 4000000 * x_gap + y
