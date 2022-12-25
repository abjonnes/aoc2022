CHAR_MAP = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
REV_CHAR_MAP = {v: k for k, v in CHAR_MAP.items()}


def decode(s):
    return sum(CHAR_MAP[char] * 5**i for i, char in enumerate(reversed(s)))


def encode(n):
    if not n:
        return ""
    return encode((n + 2) // 5) + REV_CHAR_MAP[(n + 2) % 5 - 2]


def part1(data):
    return encode(sum(decode(line) for line in data.split()))
