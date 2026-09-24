# FastBox Delivery Simulator

A Python-based logistics simulator for the FastBox delivery system. The program assigns packages to the nearest delivery agent, simulates package deliveries, calculates travel distances and agent efficiency, and generates a final performance report.

## Features

* Parses delivery data from JSON.
* Validates the input data before running the simulation.
* Assigns each package to the nearest available agent.
* Tracks the changing position of every agent.
* Calculates Euclidean delivery distances.
* Calculates package count, total distance, and efficiency for every agent.
* Identifies the most efficient agent.
* Generates a JSON performance report.
* Generates ASCII-style delivery routes.
* Generates a CSV containing active agents ranked by efficiency.
* Includes an automated test runner for all 10 provided test cases.

## Project Structure

```text
fastbox-delivery-simulator/
│
├── data.json
├── main.py
├── report.json
├── routes.txt
├── top_performers.csv
├── test_runner.py
├── Readme.md
├── .gitignore
│
└── test_cases/
    ├── test_case_1.json
    ├── test_case_2.json
    ├── test_case_3.json
    ├── test_case_4.json
    ├── test_case_5.json
    ├── test_case_6.json
    ├── test_case_7.json
    ├── test_case_8.json
    ├── test_case_9.json
    └── test_case_10.json
```

## How the Simulation Works

For every package, the program performs the following steps:

1. Read the package's warehouse and destination.
2. Check the current position of every delivery agent.
3. Calculate the Euclidean distance from each agent to the package's warehouse.
4. Assign the package to the nearest agent.
5. Calculate the distance from the agent to the warehouse.
6. Calculate the distance from the warehouse to the destination.
7. Add both distances to obtain the total distance for that delivery.
8. Update the agent's current position to the package destination.
9. Update the agent's delivery statistics.

The route for a package is therefore:

```text
Agent's current position → Warehouse → Destination
```

## Distance Calculation

Euclidean distance is calculated using:

```text
distance = √((x2 - x1)² + (y2 - y1)²)
```

The total distance for a package is:

```text
Agent → Warehouse + Warehouse → Destination
```

Full floating-point precision is retained during the simulation. Distances are rounded to two decimal places when written to the final report.

## Agent Efficiency

Agent efficiency is calculated as:

```text
efficiency = total_distance / packages_delivered
```

A lower efficiency value represents less distance travelled per delivered package.

Agents that do not receive any packages are given an efficiency value of `0` in the report. However, they are excluded when determining the best agent.

## Logic Assumptions

The assignment allows some interpretation, so the following assumptions are used:

1. Packages are processed in the order in which they appear in the input JSON.
2. The nearest agent is determined using the agent's current position when the package is processed.
3. After delivering a package, the agent's current position becomes that package's destination.
4. An agent does not return to their original position before handling another package.
5. The route is:
   `Current Agent Position → Warehouse → Destination`.
6. Euclidean distance is used for route calculations.
7. If multiple agents are equally close to a warehouse, the agent appearing first in the input JSON is selected.
8. Efficiency is calculated as total distance divided by packages delivered.
9. Agents receiving no packages have an efficiency value of `0`.
10. The best agent is the agent with the lowest efficiency among agents that delivered at least one package.
11. If there is a tie for the best agent, the first agent in input order is selected.
12. Input coordinates are expected to contain two numeric values.

## Input

The program reads `data.json`.

Example structure:

```json
{
    "warehouses": {
        "W1": [10, 20],
        "W2": [30, 40]
    },
    "agents": {
        "A1": [15, 25],
        "A2": [50, 50]
    },
    "packages": [
        {
            "id": "P1",
            "warehouse": "W1",
            "destination": [60, 70]
        }
    ]
}
```

## Output Files

### `report.json`

Contains the performance statistics for every agent:

```json
{
    "A1": {
        "packages_delivered": 3,
        "total_distance": 69.96,
        "efficiency": 23.32
    },
    "A2": {
        "packages_delivered": 3,
        "total_distance": 69.17,
        "efficiency": 23.06
    },
    "best_agent": "A3"
}
```

### `routes.txt`

Contains the simulated route for every package.

Example:

```text
P1: A2 -> W4 -> Destination(97,43)
P2: A3 -> W2 -> Destination(39,29)
```

### `top_performers.csv`

Contains agents who delivered at least one package, sorted by efficiency.

```text
agent_id,packages_delivered,total_distance,efficiency
A3,6,137.77,22.96
A2,3,69.17,23.06
A1,3,69.96,23.32
```

## Input Validation

The program validates the input before starting the simulation.

It checks for:

* Required top-level fields.
* Correct data types for warehouses, agents, and packages.
* At least one delivery agent.
* Valid warehouse coordinates.
* Valid agent coordinates.
* Required package fields.
* Valid warehouse references.
* Valid package destinations.

The program also verifies after simulation that the total number of delivered packages matches the number of packages in the input.

## Testing

An automated test runner is included in `test_runner.py`.

Run:

```bash
python test_runner.py
```

The implementation was tested against all 10 provided test cases.

```text
Test 1: PASS - 12 packages delivered
Test 2: PASS - 10 packages delivered
Test 3: PASS - 6 packages delivered
Test 4: PASS - 12 packages delivered
Test 5: PASS - 10 packages delivered
Test 6: PASS - 9 packages delivered
Test 7: PASS - 10 packages delivered
Test 8: PASS - 11 packages delivered
Test 9: PASS - 8 packages delivered
Test 10: PASS - 11 packages delivered

Passed: 10
Failed: 0
```

## Running the Project

Make sure Python 3 is installed.

Run the simulator:

```bash
python main.py
```

or:

```bash
python3 main.py
```

The program generates:

```text
report.json
routes.txt
top_performers.csv
```

To run all test cases:

```bash
python test_runner.py
```

## Technical Approach

The implementation is organized into separate functions for loading and validating input, calculating distances, finding the nearest agent, simulating deliveries, calculating efficiency, validating the final package count, and generating output files.

The simulation maintains a separate current position for each agent so that package assignment reflects the agent's location after previous deliveries.

No external Python packages are required; the project uses Python's standard library, including:

* `json`
* `math`
* `copy`
* `csv`
