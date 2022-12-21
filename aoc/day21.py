from operator import add, floordiv, mul, sub


OPERATORS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": floordiv,
}


def parse_data(data):
    monkeys = list()  # unresolved monkeys
    bank = dict()  # a mapping of monkeys to the number they ultimately yelled

    for line in data.split("\n"):
        if not line:
            continue

        monkey, data = line.split(" ", 1)
        monkey = monkey[:4]

        if data.isnumeric():
            bank[monkey] = int(data)
        else:
            op1, op, op2 = data.split(" ")
            monkeys.append(Monkey(monkey, OPERATORS[op], op1, op2))

    return monkeys, bank


class Monkey:
    """An unresolved monkey. It stores its two monkey "operands" and the
    operation it performs.
    """

    def __init__(self, name, op, op1, op2):
        self.name = name
        self.op = op
        self.op1 = op1
        self.op2 = op2

    def ready(self, bank):
        return self.op1 in bank and self.op2 in bank

    def operate(self, bank):
        """Perform the operation and store the result in the bank."""
        bank[self.name] = self.op(bank[self.op1], bank[self.op2])


class X:
    """Representation of the unknown number that the human must shout for part
    2. The idea is to store a list of the _inverse_ operations on which it's
    been operated, so that it can play those operations back on the required
    output to generate the necessary input.
    """

    def __init__(self):
        self.ops = list()

    def __add__(self, other):
        self.ops.append(lambda x: x - other)
        return self

    def __radd__(self, other):
        self.ops.append(lambda x: x - other)
        return self

    def __sub__(self, other):
        self.ops.append(lambda x: x + other)
        return self

    def __rsub__(self, other):
        self.ops.append(lambda x: other - x)
        return self

    def __mul__(self, other):
        self.ops.append(lambda x: x // other)
        return self

    def __rmul__(self, other):
        self.ops.append(lambda x: x // other)
        return self

    def __floordiv__(self, other):
        self.ops.append(lambda x: x * other)
        return self

    def __rfloordiv__(self, other):
        self.ops.append(lambda x: other // x)
        return self

    def playback(self, target):
        for op in reversed(self.ops):
            target = op(target)
        return target


def run(monkeys, bank):
    while monkeys:
        new_monkeys = list()
        for monkey in monkeys:
            if monkey.ready(bank):
                monkey.operate(bank)
            else:
                new_monkeys.append(monkey)
        monkeys = new_monkeys


def part1(data):
    monkeys, bank = parse_data(data)
    run(monkeys, bank)
    return bank["root"]


def part2(data):
    monkeys, bank = parse_data(data)

    # replace the human number with the unknown
    bank["humn"] = X()

    # find the root and remove it from the list of unresolved monkeys
    root = next(monkey for monkey in monkeys if monkey.name == "root")
    monkeys = [monkey for monkey in monkeys if monkey.name != "root"]

    run(monkeys, bank)

    # one of the root's operands has the unknown: determine which, and run the
    # playback algorithm
    if isinstance(bank[root.op1], X):
        return bank[root.op1].playback(bank[root.op2])
    else:
        return bank[root.op2].playback(bank[root.op1])
