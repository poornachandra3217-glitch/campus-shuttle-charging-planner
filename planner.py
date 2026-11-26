"""Minimum charging stops on a fixed, one-way shuttle route."""
import argparse
from dataclasses import dataclass
from itertools import combinations
import json
from pathlib import Path
from time import perf_counter_ns

BRUTE_FORCE_LIMIT = 18


@dataclass(frozen=True)
class Route:
    destination: int
    battery_range: int
    stations: tuple[int, ...]

    def __post_init__(self):
        if type(self.destination) is not int or self.destination < 1:
            raise ValueError("destination_km must be a positive integer")
        if type(self.battery_range) is not int or self.battery_range < 1:
            raise ValueError("range_km must be a positive integer")
        if any(type(km) is not int or not 0 < km < self.destination
               for km in self.stations):
            raise ValueError("stations must be integer km strictly inside the route")
        if len(set(self.stations)) != len(self.stations):
            raise ValueError("station locations must be unique")
        object.__setattr__(self, "stations", tuple(sorted(self.stations)))

    @property
    def points(self):
        return (0, *self.stations, self.destination)

    def leg_distances(self, stops):
        points = (0, *stops, self.destination)
        return tuple(end - start for start, end in zip(points, points[1:]))


def brute_force(route):
    """Try subsets by increasing size and return the first feasible subset."""
    if len(route.stations) > BRUTE_FORCE_LIMIT:
        raise ValueError(f"brute force supports up to {BRUTE_FORCE_LIMIT} stations")
    for count in range(len(route.stations) + 1):
        for stops in combinations(route.stations, count):
            if max(route.leg_distances(stops)) <= route.battery_range:
                return stops
    return None


def dynamic_programming(route):
    """Find the shortest path in the graph of reachable forward legs."""
    points = route.points
    unreachable = len(points)
    legs = [0] + [unreachable] * (len(points) - 1)
    previous = [-1] * len(points)
    for end in range(1, len(points)):
        for start in range(end - 1, -1, -1):
            if points[end] - points[start] > route.battery_range:
                break
            if legs[start] + 1 < legs[end]:
                legs[end] = legs[start] + 1
                previous[end] = start
    if previous[-1] == -1:
        return None
    stops = []
    index = previous[-1]
    while index > 0:
        stops.append(points[index])
        index = previous[index]
    return tuple(reversed(stops))


def greedy(route):
    """Take the farthest reachable point on each charge."""
    points = route.points
    current = 0
    stops = []
    while points[-1] - points[current] > route.battery_range:
        farthest = current
        while (farthest + 1 < len(points)
               and points[farthest + 1] - points[current] <= route.battery_range):
            farthest += 1
        if farthest == current:
            return None
        stops.append(points[farthest])
        current = farthest
    return tuple(stops)


def divide_and_conquer(route):
    """Compose equal-length blocks of legs using binary lifting."""
    points = route.points
    destination = len(points) - 1
    one_leg = []
    farthest = 0
    for start in range(len(points)):
        while (farthest < destination
               and points[farthest + 1] - points[start] <= route.battery_range):
            farthest += 1
        one_leg.append(farthest)

    # A block of 2**k legs is two consecutive blocks of 2**(k-1) legs.
    jumps = [one_leg]
    for _ in range(1, destination.bit_length()):
        half = jumps[-1]
        jumps.append([half[half[start]] for start in range(len(points))])

    # Find the largest leg budget below len(points) that falls short.
    current = used = 0
    for level in range(len(jumps) - 1, -1, -1):
        block = 1 << level
        reached = jumps[level][current]
        if used + block <= destination and reached < destination:
            current = reached
            used += block
    if used == destination or one_leg[current] != destination:
        return None

    # Reconstruct the route by expanding its one-leg choices.
    stops = []
    current = 0
    for _ in range(used):
        current = one_leg[current]
        stops.append(points[current])
    return tuple(stops)


SOLVERS = {
    "brute-force": brute_force,
    "divide-and-conquer": divide_and_conquer,
    "dynamic-programming": dynamic_programming,
    "greedy": greedy,
}


def read_route(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"destination_km", "range_km", "station_km"}
    if not isinstance(data, dict) or data.keys() != required:
        raise ValueError("JSON must contain destination_km, range_km and station_km")
    if not isinstance(data["station_km"], list):
        raise ValueError("station_km must be a list")
    return Route(data["destination_km"], data["range_km"], tuple(data["station_km"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route", type=Path, help="JSON route file")
    parser.add_argument("--method", choices=("all", *SOLVERS), default="all")
    args = parser.parse_args()
    try:
        route = read_route(args.route)
        if args.method == "brute-force" and len(route.stations) > BRUTE_FORCE_LIMIT:
            raise ValueError(f"brute force supports up to {BRUTE_FORCE_LIMIT} stations")
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Route: {route.destination} km | Full-charge range: {route.battery_range} km")
    print(f"Stations (km): {list(route.stations)}")
    methods = SOLVERS if args.method == "all" else (args.method,)
    for name in methods:
        if name == "brute-force" and len(route.stations) > BRUTE_FORCE_LIMIT:
            print(f"{name}: skipped (more than {BRUTE_FORCE_LIMIT} stations)")
            continue
        started = perf_counter_ns()
        stops = SOLVERS[name](route)
        elapsed = (perf_counter_ns() - started) / 1000
        if stops is None:
            print(f"{name}: unreachable | {elapsed:.1f} us")
        else:
            print(f"{name}: {len(stops)} stops | stations {list(stops)} km | "
                  f"legs {list(route.leg_distances(stops))} km | {elapsed:.1f} us")


if __name__ == "__main__":
    main()
