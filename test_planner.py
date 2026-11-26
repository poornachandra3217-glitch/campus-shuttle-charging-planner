import itertools
from pathlib import Path
import subprocess
import sys
import unittest

from planner import Route, SOLVERS


class PlannerTests(unittest.TestCase):
    def test_known_routes(self):
        cases = [
            (Route(25, 10, (17, 12, 8, 4)), (8, 17)),
            (Route(25, 10, (4, 8, 20)), None),
            (Route(10, 10, ()), ()),
            (Route(11, 10, ()), None),
            (Route(20, 10, (10,)), (10,)),
            (Route(30, 10, (10, 20)), (10, 20)),
        ]
        for route, expected in cases:
            for name, solve in SOLVERS.items():
                with self.subTest(route=route, solver=name):
                    self.assertEqual(solve(route), expected)

    def test_cross_check_exhaustively(self):
        # 2^7 station sets × 8 battery ranges = 1,024 routes.
        for mask, battery_range in itertools.product(range(128), range(1, 9)):
            stations = tuple(km for km in range(1, 8) if mask & (1 << (km - 1)))
            route = Route(8, battery_range, stations)
            expected = SOLVERS["brute-force"](route)
            for name, solve in SOLVERS.items():
                with self.subTest(route=route, solver=name):
                    actual = solve(route)
                    if expected is None:
                        self.assertIsNone(actual)
                        continue
                    self.assertIsNotNone(actual)
                    self.assertEqual(len(actual), len(expected))
                    self.assertEqual(tuple(sorted(set(actual))), actual)
                    self.assertTrue(set(actual).issubset(stations))
                    self.assertTrue(all(0 < leg <= battery_range
                                        for leg in route.leg_distances(actual)))

    def test_invalid_routes(self):
        cases = [(0, 10, ()), (25, 0, ()), (25, 10, (4, 4)),
                 (25, 10, (0,)), (25, 10, (25,)), (25, 10, (True,))]
        for values in cases:
            with self.subTest(values=values), self.assertRaises(ValueError):
                Route(*values)

    def test_brute_force_limit(self):
        with self.assertRaises(ValueError):
            SOLVERS["brute-force"](Route(20, 1, tuple(range(1, 20))))

    def test_cli(self):
        folder = Path(__file__).resolve().parent
        command = [sys.executable, str(folder / "planner.py")]
        result = subprocess.run(command + [str(folder / "examples/campus_route.json")],
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.count("2 stops"), 4)
        missing = subprocess.run(command + [str(folder / "missing.json")],
                                 capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertNotIn("Traceback", missing.stderr)


if __name__ == "__main__":
    unittest.main()
