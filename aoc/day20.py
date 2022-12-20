from itertools import chain, repeat


def run(data, key=1, n_mix=1):
    seq = [(idx, int(x) * key) for idx, x in enumerate(data.split())]
    data = list(seq)

    l = len(seq)

    for idx, n in chain.from_iterable(repeat(seq, n_mix)):
        old_idx = data.index((idx, n))
        data.pop(old_idx)
        new_idx = (old_idx + n) % (l - 1)
        data.insert(new_idx, (idx, n))

    ref_idx = data.index(next((idx, n) for idx, n in seq if n == 0))
    return sum(data[(ref_idx + offset) % l][1] for offset in (1000, 2000, 3000))


def part1(data):
    return run(data)


def part2(data):
    return run(data, 811589153, 10)
