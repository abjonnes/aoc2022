ROCK = 1
PAPER = 2
SCISSORS = 3

WIN = 6
DRAW = 3
LOSE = 0


GAME_RULES = {
    ROCK: {ROCK: DRAW, PAPER: WIN, SCISSORS: LOSE},
    PAPER: {ROCK: LOSE, PAPER: DRAW, SCISSORS: WIN},
    SCISSORS: {ROCK: WIN, PAPER: LOSE, SCISSORS: DRAW},
}


def part1(data):
    token_map = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
        "X": ROCK,
        "Y": PAPER,
        "Z": SCISSORS,
    }
    calls = [token_map[token] for token in data.split()]
    return sum(
        call2 + GAME_RULES[call1][call2]
        for call1, call2 in zip(calls[::2], calls[1::2])
    )


def part2(data):
    token_map = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
        "X": LOSE,
        "Y": DRAW,
        "Z": WIN,
    }
    calls = [token_map[token] for token in data.split()]

    reverse_rules = {
        key1: {value2: key2 for key2, value2 in value1.items()}
        for key1, value1 in GAME_RULES.items()
    }

    return sum(
        call2 + reverse_rules[call1][call2]
        for call1, call2 in zip(calls[::2], calls[1::2])
    )
