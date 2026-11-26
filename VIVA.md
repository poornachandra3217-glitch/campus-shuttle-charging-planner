# Presentation and viva notes

## Five-minute presentation

1. **Problem.** “My project plans an electric visitor shuttle route through a wildlife reserve. The shuttle starts fully charged. Each chosen stop restores full battery range. The goal is to minimize the number of charging stops.”
2. **Inputs.** Show the 25 km route, range of 10 km, and stations at km 4, 8, 12 and 17. Separate the number of legs from the number of charging stops.
3. **Four methods.** Brute force enumerates subsets. DP remembers the best predecessor. Greedy goes to the farthest reachable point. Divide and conquer builds bigger travel blocks by composing two half blocks.
4. **Run the demo.** Run `python planner.py examples/reserve_route.json`. Point out stops at km 8 and 17 and leg distances of 8, 9 and 8 km.
5. **Prove the result.** One stop would supply only two charges, for at most 20 km. Show `examples/unreachable.json` to demonstrate the range check.

## Individual viva questions

**Why is the destination never a charging stop?** The shuttle has completed the trip once it reaches the destination. A route with three travel legs has two interior stops.

**What does the DP state hold?** The fewest travel legs needed to reach one point, plus a predecessor so the program can reconstruct a plan.

**Why can the DP scan break when a predecessor is too far away?** Points are sorted and scanned backwards. Earlier points are at least as far from the current end point.

**How is divide and conquer implemented?** A two-leg jump from km 0 first goes to km 8 and then to km 17. More generally, a block of 2ᵏ legs uses one half block to find an intermediate point and a second half block from that point. The method shares the farthest-reachable choice with the greedy solver.

**What is the difference between greedy and dynamic programming here?** Greedy takes one farthest option. DP evaluates possible predecessors and stores the best for each point.

**What happens with no reachable charger?** If the destination is within range, the shuttle finishes directly. Otherwise the route is unreachable.

**Can two optimal schedules differ?** Yes. The goal is minimum stop count. A test should validate both feasibility and the count, with exact station equality reserved for a sample that has a unique optimum.

**Why cap the brute-force demo?** The candidate count doubles for each extra station in the worst case. The exact DP, greedy and divide-and-conquer methods can still run on the larger input.

**When could farthest-stop greedy fail for a different objective?** With unequal charging times, minimizing minutes can favour stopping earlier at a faster charger. This project minimizes stop count with full recharges.
