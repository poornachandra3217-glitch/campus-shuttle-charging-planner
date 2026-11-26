# Campus Shuttle Charging Planner

**Poorna Chandra and Ramya Sree · Design and Analysis of Algorithms**

A campus shuttle travels along a fixed one-way route. The planner finds a minimum-stop charging plan and compares four algorithms on identical input. The example routes are synthetic.

## Run on Windows or macOS/Linux

Install Python 3.10 or newer. No packages or database are required. Open PowerShell or a terminal in the project folder and run:

```text
python planner.py examples/campus_route.json
python planner.py examples/unreachable.json
python planner.py examples/direct.json
python planner.py examples/campus_route.json --method greedy
python -m unittest -v
```

Use `py` on Windows or `python3` on macOS/Linux if your terminal uses that command for Python.

## Input and output

```json
{"destination_km": 25, "range_km": 10, "station_km": [4, 8, 12, 17]}
```

Destination and range are positive integer kilometres. Station positions are unique integer kilometre markers strictly between the entrance (0 km) and destination. Positions can be supplied in any order. The shuttle starts fully charged and recharges to full at each chosen station. The objective is the number of stops. Travel time, charging time, energy consumption changes and station availability are outside this classroom model.

The program prints each algorithm’s stop count, station locations, leg lengths and runtime in microseconds. A successful plan with zero stops is printed as such. An impossible route is printed as unreachable. Optimal plans can differ when there is a tie. Timings vary across runs and machines. Brute force is skipped in the four-method display above 18 stations.

## Results

| Case | Expected result from each method |
|---|---|
| Campus route | 2 stops at km 8 and 17. Leg distances 8, 9 and 8 km |
| Unreachable | Unreachable because the gap from km 8 to km 20 exceeds 10 km |
| Direct | 0 stops because the destination is exactly one full charge away |

## Deliverables

- [Python program](planner.py) and [tests](test_planner.py)
- [Sample inputs](examples/)
- [Project report and algorithm proofs](REPORT.md)
- [Presentation walkthrough and viva questions](VIVA.md)
