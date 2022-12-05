import re


def parse_stacks(stack_data):
    # +1 because the last box doesn't have a space
    n_stacks = (len(stack_data[0]) + 1) // 4
    stacks = [list() for _ in range(n_stacks)]
    for line in stack_data[:-1]:  # don't include the stack numbers
        for idx, box in enumerate(line[1::4]):
            if box == " ":
                continue
            stacks[idx].append(box)
    return [list(reversed(stack)) for stack in stacks]


def run(data, move_func):
    stack_data, moves = data.split("\n\n")
    stacks = parse_stacks(stack_data.split("\n"))

    for move in moves.split("\n"):
        if not move:
            continue

        match = re.match(r"move (\d+) from (\d+) to (\d+)", move)
        n, from_, to = match.groups()
        n = int(n)
        from_idx = int(from_) - 1
        to_idx = int(to) - 1

        move_func(stacks, n, from_idx, to_idx)

    return "".join(stack[-1] for stack in stacks)


def part1(data):
    def move_func(stacks, n, from_idx, to_idx):
        for _ in range(n):
            stacks[to_idx].append(stacks[from_idx].pop())

    return run(data, move_func)


def part2(data):
    def move_func(stacks, n, from_idx, to_idx):
        stacks[to_idx].extend(stacks[from_idx][-n:])
        stacks[from_idx] = stacks[from_idx][:-n]

    return run(data, move_func)
