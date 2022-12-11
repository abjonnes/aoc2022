import re


PATTERN = re.compile(
    r"""Monkey \d+:
  Starting items: (.*?)
  Operation: new = (.*?)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""
)


class Item:
    def __init__(self, value, _):
        self.value = value

    def add(self, operand):
        self.value += operand

    def multiply(self, operand):
        self.value *= operand

    def square(self):
        self.value **= 2

    def is_divisible(self, divisor):
        return self.value % divisor == 0

    def reduce_worry(self, worry_factor):
        self.value //= worry_factor


class BigItem:
    """Separate class to efficiently handle operations on large item values. By inspection of the
    monkey data, all monkeys are testing whether the item is divisible by a _prime_ divisor. Using
    that information, the approach here is to maintain the `value (mod p)` value, which is smaller
    than p, for each potential prime divisor (p). Modular arithmetic is "compatible" with normal
    addition and multiplication, so this effectively is maintaining `operation(value) % p` for those
    two operations.
    """

    def __init__(self, value, primes):
        self.values = {prime: value % prime for prime in primes}

    def add(self, operand):
        self.values = {
            prime: (value + operand) % prime for prime, value in self.values.items()
        }

    def multiply(self, operand):
        self.values = {
            prime: (value * operand) % prime for prime, value in self.values.items()
        }

    def square(self):
        self.values = {
            prime: (value * value) % prime for prime, value in self.values.items()
        }

    def is_divisible(self, divisor):
        return self.values[divisor] == 0

    def reduce_worry(self, worry_factor):
        """The floor division is more complicated and we don't need it if we're using big items, so
        let's skip it.
        """
        if worry_factor != 1:
            raise NotImplementedError("Can't reduce worry on a BigItem")


class Monkey:
    # class attribute to maintain a list of all observed divisors
    all_divisors = set()

    def __init__(
        self, item_string, operation, divisor, throw_true, throw_false, worry_factor
    ):
        self.raw_items = item_string

        if operation == "old * old":
            self.operate = lambda item: item.square()
        elif operation.startswith("old + "):
            self.operate = lambda item: item.add(int(operation[6:]))
        elif operation.startswith("old * "):
            self.operate = lambda item: item.multiply(int(operation[6:]))

        self.divisor = int(divisor)
        self.all_divisors.add(self.divisor)

        self.throw_true = int(throw_true)
        self.throw_false = int(throw_false)
        self.worry_factor = worry_factor
        self.n = 0

    def setup_items(self):
        """This has to be invoked after all monkeys have been created so that we have the full set
        of divisors available.
        """
        item_class = Item if self.worry_factor > 1 else BigItem
        self.items = [
            item_class(item_value, self.all_divisors)
            for item_value in (int(x.strip()) for x in self.raw_items.split(","))
        ]

    def run(self, monkeys):
        while self.items:
            item = self.items.pop(0)
            self.operate(item)
            item.reduce_worry(self.worry_factor)

            recipient = monkeys[
                self.throw_true if item.is_divisible(self.divisor) else self.throw_false
            ]
            recipient.items.append(item)

            self.n += 1


def parse_monkeys(data, worry_factor):
    monkeys = [Monkey(*groups, worry_factor) for groups in PATTERN.findall(data)]
    for monkey in monkeys:
        monkey.setup_items()
    return monkeys


def run(data, worry_factor, iterations):
    monkeys = parse_monkeys(data, worry_factor)
    for _ in range(iterations):
        for monkey in monkeys:
            monkey.run(monkeys)
    counts = sorted((monkey.n for monkey in monkeys), reverse=True)
    return counts[0] * counts[1]


def part1(data):
    return run(data, 3, 20)


def part2(data):
    return run(data, 1, 10000)
