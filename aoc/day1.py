def elf_totals(data):
    total = 0
    for line in data.split("\n"):
        if not line:
            yield total
            total = 0
            continue
        total += int(line)


def part1(data):
    return max(elf_totals(data))


def part2(data):
    return sum(sorted(elf_totals(data))[-3:])
