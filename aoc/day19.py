from dataclasses import dataclass, field
from functools import cache
from re import findall

from frozendict import frozendict


RESOURCE_TYPES = ("ore", "clay", "obsidian", "geode")


def parse_data(data):
    def line_to_recipe(line):
        _, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = [
            int(x) for x in findall(r"\d+", line)
        ]
        return {
            "ore": {"ore": ore_ore},
            "clay": {"ore": clay_ore},
            "obsidian": {"ore": obsidian_ore, "clay": obsidian_clay},
            "geode": {"ore": geode_ore, "obsidian": geode_obsidian},
        }

    return {
        idx: line_to_recipe(line)
        for idx, line in enumerate(data.split("\n"), start=1)
        if line
    }


@dataclass(frozen=True)
class State:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    # frozendicts so we can use a cache
    robots: frozendict = field(default_factory=lambda: frozendict({"ore": 1}))
    time: int = 1

    def generate(self):
        """Generates resources from robots."""
        return self.spawn(
            time=0,
            **{resource: self.robots.get(resource, 0) for resource in RESOURCE_TYPES},
        )

    def spawn(
        self,
        ore=0,
        clay=0,
        obsidian=0,
        geode=0,
        added_robots=frozendict(),
        time=1,
    ):
        """Generates a new state with the given changes in resources and robots. Increments the
        timer by 1 by default.
        """
        return State(
            self.ore + ore,
            self.clay + clay,
            self.obsidian + obsidian,
            self.geode + geode,
            frozendict(
                {
                    resource: self.robots.get(resource, 0)
                    + added_robots.get(resource, 0)
                    for resource in RESOURCE_TYPES
                }
            ),
            self.time + time,
        )


def run(recipe, time):
    """Recursively examines the different ways we can spend resources on robots. Since there's up to
    5^time leaf nodes here, we need to apply a few pruning heuristics to make the problem tractible
    (in addition to utilizing a cache):

    1. Keep track of the maximum geodes observed in any path so far, and if it's ever not possible
       to "catch up" to that value by constructing a geode robot every turn (even if that's not
       possible!), then bail since this path will not improve our output.
    2. If we _can_ construct a geode robot, we _must_ construct a geode robot.
    3. Don't construct a robot if the total production of that resource would exceed the maximum
       possible amount consumed in a single time step.
    """
    # heuristic 1
    max_geode = 0

    # heuristic 3
    max_resources = {
        resource: max(robot.get(resource, 0) for robot in recipe.values())
        for resource in RESOURCE_TYPES
    }

    @cache
    def recurse(state):
        nonlocal max_geode

        if state.time == time:
            geode = state.generate().geode

            # heuristic 1
            if geode > max_geode:
                max_geode = geode

            return geode

        # heuristic 1
        # if we have x geodes, y geode robots and dt time steps remaining, the maximum possible
        # number of geodes we can have at the end is given by x + [dt * (dt - 1) / 2] + y * dt
        dt = time + 1 - state.time
        if (
            state.geode + dt * (dt - 1) // 2 + state.robots.get("geode", 0) * dt
            <= max_geode
        ):
            return 0  # the value here doesn't matter

        robot_plans = [dict()]
        for robot_type in RESOURCE_TYPES:
            if not all(
                getattr(state, resource) >= recipe[robot_type].get(resource, 0)
                for resource in RESOURCE_TYPES
            ):
                continue

            # heuristic 3
            if (
                robot_type != "geode"
                and state.robots.get(robot_type, 0) + 1 > max_resources[robot_type]
            ):
                continue

            plan = {"added_robots": {robot_type: 1}}
            plan.update({resource: -n for resource, n in recipe[robot_type].items()})

            # heuristic 2
            if robot_type == "geode":
                # constructing a geode robot is our only plan
                robot_plans = [plan]
                break

            robot_plans.append(plan)

        state = state.generate()

        # traverse plans starting with geode robot, then obsidian, etc so we can find the maximum
        # geodes faster to aid heuristic 1
        return max(
            recurse(new_state)
            for new_state in [state.spawn(**plan) for plan in reversed(robot_plans)]
        )

    return recurse(State())


def part1(data):
    quality_sum = 0

    for id_, recipe in parse_data(data).items():
        quality_sum += run(recipe, 24) * id_

    return quality_sum


def part2(data):
    prod = 1

    for id_, recipe in parse_data(data).items():
        if id_ > 3:
            break

        prod *= run(recipe, 32)

    return prod
