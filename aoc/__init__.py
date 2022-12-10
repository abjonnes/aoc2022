from importlib import import_module
import os

import click
import requests


INPUT_URL = "https://adventofcode.com/2022/day/{day}/input"


def get_input(day):
    response = requests.get(
        INPUT_URL.format(day=day), cookies={"session": os.environ["AOC_SESSION"]}
    )
    response.raise_for_status()
    return response.text


def format_output(output):
    if isinstance(output, str):
        return "\n" + output
    return str(output)


@click.command()
@click.argument("day", type=int, required=True)
def aoc(day):
    module = import_module(f"aoc.day{day}")

    data = get_input(day)

    print(f"Part 1: {format_output(module.part1(data))}")

    if hasattr(module, "part2"):
        print(f"Part 2: {format_output(module.part2(data))}")
