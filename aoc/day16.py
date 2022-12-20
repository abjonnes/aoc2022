from collections import defaultdict, deque
from itertools import chain, combinations, product
import re


def parse_data(data):
    """Generate an unweighted graph structure from the input."""
    edges = defaultdict(set)
    nodes = dict()
    for line in data.split("\n"):
        if not line:
            continue

        node, *neighbors = re.findall(r"[A-Z]{2}", line)
        rate = int(re.search(r"\d+", line).group(0))

        for neighbor in neighbors:
            edges[node].add(neighbor)
            edges[neighbor].add(node)

        if rate:
            nodes[node] = rate

    return edges, nodes


def consolidate(all_edges, nodes):
    """Generate a new (almost) complete, weighted graph where every functional
    valve is a node and the edge weight represents the distance between the two
    valves.
    """
    edges = defaultdict(dict)
    # BFS to get the shortest distance between pairs of valves
    for node in list(nodes) + ["AA"]:
        to_visit = deque((edge, 1) for edge in all_edges[node])
        visited = {node}

        while to_visit:
            neighbor, weight = to_visit.popleft()
            visited.add(neighbor)

            if neighbor in nodes:
                edges[node].setdefault(neighbor, weight)

            to_visit.extend(
                (edge, weight + 1)
                for edge in all_edges[neighbor]
                if edge not in visited
            )

    return edges, nodes


# copied from itertools docs, modified to return frozensets
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return [
        frozenset(x)
        for x in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    ]


def run(data, time):
    edges, nodes = consolidate(*parse_data(data))

    # list of dict of dicts to represent the currently-determined maximum
    # possible pressure release:
    #  - first "key" (index) is time
    #  - second key is current location (valve)
    #  - third key is which valves are open
    #
    # e.g. pressures[15]["BB"][{"CC", "DD"}] holds the maximum so-far-observed
    # pressure released at the 15th minute while located at valve BB if valves
    # CC and DD are already opened
    pressures = [
        {valve: defaultdict(lambda: -1e10) for valve in nodes} for _ in range(time + 1)
    ]

    # the earliest we can get to and open any valves
    for valve, distance in edges["AA"].items():
        pressures[distance + 1][valve][frozenset({valve})] = 0

    # iterate over all the keys _minute by minute_ (order of time is important)
    for minute, valve, open_valves in product(
        range(1, time + 1), nodes, powerset(nodes)
    ):
        # update with pressure released since the previous minute
        pressures[minute][valve][open_valves] = max(
            pressures[minute][valve][open_valves],
            pressures[minute - 1][valve][open_valves]
            + sum(nodes[x] for x in open_valves),
        )

        # if current valve isn't open, no reason to consider other valves
        if valve not in open_valves:
            continue

        # consider jumping to every remaining closed valve from here
        for other_valve in set(nodes) - open_valves:
            distance = edges[valve][other_valve]

            # unreachable in the remaining time
            if minute + distance + 1 > time:
                continue

            new_open_valves = frozenset(open_valves | {other_valve})

            # update with pressure released during travel to new valve
            pressures[minute + distance + 1][other_valve][new_open_valves] = max(
                pressures[minute + distance + 1][other_valve][new_open_valves],
                pressures[minute][valve][open_valves]
                + sum(nodes[x] for x in open_valves) * (distance + 1),
            )

    # we're interested in the maximum pressure released at the final minute,
    # regardless of final position, but the set of open valves to achieve it is
    # useful for part 2 so we keep the data separated by that
    return {
        open_valves: max(pressures[-1][valve][open_valves] for valve in nodes)
        for open_valves in powerset(nodes)
    }


def part1(data):
    return max(run(data, 30).values())


def part2(data):
    # consider the sum of maximum pressures released for two paths which have
    # _disjoint_ sets of opened valves only
    return max(
        pressure1 + pressure2
        for (ov1, pressure1), (ov2, pressure2) in product(
            run(data, 26).items(), repeat=2
        )
        if ov1.isdisjoint(ov2)
    )
