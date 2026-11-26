# Campus Shuttle Charging Planner

Poorna Chandra · 250200322  
Design and Analysis of Algorithms

## Abstract

A campus shuttle has a fixed range and can recharge at selected stations along a one-way route. This project finds the fewest charging stops and reconstructs the corresponding route. It compares subset enumeration, dynamic programming, greedy farthest-stop selection, and a divide-and-conquer construction that composes blocks of travel legs. The program checks feasibility, validates input and reports the result for each algorithm.

## Problem formulation

Let the ordered route points be p₀ (entrance), p₁ through pₙ (charging stations), and pₙ₊₁ (destination). If the battery range is R, a forward leg is feasible when its distance is greater than zero and at most R. A feasible plan with L legs uses L − 1 charging stops. The destination is not counted as a charging stop.

## Algorithms and correctness

### Brute force

Enumerate station subsets from size zero through size n. For each subset, insert the entrance and destination, then check every gap. Every possible increasing charging plan corresponds to a subset. The first feasible subset has the fewest stops because all smaller sizes were already rejected.

### Dynamic programming

Set `legs[0] = 0` and mark the other entries unreachable. For each point j in increasing order, use the recurrence `legs[j] = min(legs[i] + 1)` over reachable earlier points i within range of j. Every valid plan to j has one such final predecessor i. If an optimal plan to j uses i, replacing its prefix with the shortest plan to i cannot increase the final leg count. Store the minimizing predecessor when updating each entry and follow the predecessor chain backwards from the destination.

### Greedy

Take the farthest reachable point each time. If the destination is reachable, drive straight there. The farthest reachable point cannot move backwards when the current location moves forward. Suppose greedy has travelled at least as far as another plan after k legs. The other plan's next point is either already behind greedy or within the range of greedy’s current point. Greedy can therefore match or exceed that next point. By induction, after any number of legs greedy is at least as far as any feasible plan. It reaches the destination in the fewest legs or detects an impassable gap.

### Divide and conquer by leg count

The base case `jump[0][i]` is the farthest point reachable from i in one leg. It can equal i when a gap blocks travel. A block of two to the power k legs is two consecutive half blocks:

```text
jump[k][i] = jump[k-1][jump[k-1][i]]
```

The code builds those blocks bottom up. By the same reachability argument as the greedy proof, the composed endpoint is the farthest reachable with **at most** that many legs. Test the blocks from largest to smallest to find the largest leg budget that still falls short. One more leg reaches the finish on a feasible route. A route through n stations can require at most n+1 legs, which gives the search bound. Expand the one-leg choices to print the complete plan. This algorithm shares the greedy forward rule and compares a different way to compute the answer.

## Complexity

Let n be the station count. Input normalization sorts positions once in O(n log n) time. Solver bounds below assume sorted positions and include the space for the points and returned plan.

| Solver | Worst-case time | Space |
|---|---:|---:|
| Brute force | O(n × 2ⁿ) | O(n) |
| Dynamic programming | O(n²) | O(n) |
| Greedy | O(n) | O(n) |
| Divide and conquer | O(n log n) | O(n log n) |

## Verification

The normal, impossible and exact-range examples check charging stops and feasibility. The test suite also compares all methods on 1,024 combinations of station sets and battery ranges, validates returned stops and leg distances, and checks error handling at the command line. Because brute force enumerates every smaller subset first, it serves as the reference optimum for these small cases.

## Conclusion

On the demonstration route, two stops are both feasible and necessary. With one stop, the shuttle could cover at most 20 km. Greedy is suitable for solving a single route under the model because each station is examined a constant number of times.
