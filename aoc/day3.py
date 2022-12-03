from functools import reduce
from operator import and_
from string import ascii_lowercase, ascii_uppercase


def shared_object_value(*collections):
    """Gets the "value" of the object shared between all collections. Assumes exactly one such
    object exists.
    """
    sets = [set(collection) for collection in collections]
    shared_obj = reduce(and_, sets).pop()

    if shared_obj in ascii_lowercase:
        return ascii_lowercase.index(shared_obj) + 1
    return ascii_uppercase.index(shared_obj) + 27


def part1(data):
    return sum(
        shared_object_value(
            rucksack[: len(rucksack) // 2], rucksack[len(rucksack) // 2 :]
        )
        for rucksack in data.split()
    )


def part2(data):
    rucksacks = data.split()
    return sum(
        shared_object_value(*rucksacks[3 * i : 3 * (i + 1)])
        for i in range(len(rucksacks) // 3)
    )
