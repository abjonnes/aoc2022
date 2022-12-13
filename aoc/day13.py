class Wrapper:
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.is_integer = True
        else:
            self.value = [Wrapper(x) for x in value]
            self.is_integer = False

    def as_wrapped_list(self):
        return Wrapper([self.value])

    def __lt__(self, other):
        if self.is_integer == other.is_integer:
            return self.value < other.value
        if self.is_integer:
            return self.as_wrapped_list() < other
        return self < other.as_wrapped_list()

    def __eq__(self, other):
        if self.is_integer == other.is_integer:
            return self.value == other.value
        if self.is_integer:
            return self.as_wrapped_list() == other
        return self == other.as_wrapped_list()

    def __repr__(self):
        return repr(self.value)


def parse_data(data):
    # is `eval` cheating? :)
    return [Wrapper(eval(packet)) for packet in data.split()]


def part1(data):
    packets = parse_data(data)
    pairs = zip(packets[::2], packets[1::2])
    return sum(
        idx
        for idx, (packet_a, packet_b) in enumerate(pairs, start=1)
        if packet_a < packet_b
    )


def part2(data):
    dividers = [Wrapper([[2]]), Wrapper([[6]])]
    packets = sorted(parse_data(data) + dividers)
    return (packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1)
