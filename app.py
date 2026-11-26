from flask import Flask, request, jsonify, render_template
from planner import Route, SOLVERS, BRUTE_FORCE_LIMIT
from time import perf_counter_ns

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/plan")
def plan():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("station_km"), list):
            raise ValueError("Provide destination, range and station list.")
        if len(data["station_km"]) > 500:
            raise ValueError("Maximum 500 stations.")
        route = Route(data.get("destination_km"), data.get("range_km"), tuple(data["station_km"]))
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc)), 400
    results = []
    for name, solve in SOLVERS.items():
        if name == "brute-force" and len(route.stations) > BRUTE_FORCE_LIMIT:
            results.append(dict(method=name, status="skipped"))
            continue
        start = perf_counter_ns()
        stops = solve(route)
        elapsed = (perf_counter_ns() - start) / 1000
        results.append(dict(method=name, status="unreachable" if stops is None else "reachable",
                            stops=stops, count=None if stops is None else len(stops),
                            legs=None if stops is None else route.leg_distances(stops), runtime_us=elapsed))
    return jsonify(destination=route.destination, battery_range=route.battery_range, stations=route.stations, results=results)

if __name__ == "__main__":
    app.run(port=5000)
