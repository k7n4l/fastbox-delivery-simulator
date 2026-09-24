import json
import math
import copy
import csv


def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    required_keys = ["warehouses", "agents", "packages"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")

    if not isinstance(data["warehouses"], dict):
        raise ValueError("'warehouses' must be an object")

    if not isinstance(data["agents"], dict):
        raise ValueError("'agents' must be an object")

    if not isinstance(data["packages"], list):
        raise ValueError("'packages' must be a list")

    if not data["agents"]:
        raise ValueError("At least one agent is required")

    # Validate warehouse coordinates
    for warehouse_id, position in data["warehouses"].items():
        if not isinstance(position, list) or len(position) != 2:
            raise ValueError(
                f"Invalid coordinates for warehouse {warehouse_id}"
            )

    # Validate agent coordinates
    for agent_id, position in data["agents"].items():
        if not isinstance(position, list) or len(position) != 2:
            raise ValueError(
                f"Invalid coordinates for agent {agent_id}"
            )

    # Validate packages
    for package in data["packages"]:
        required_package_keys = ["id", "warehouse", "destination"]

        for key in required_package_keys:
            if key not in package:
                raise ValueError(
                    f"Package is missing required field: {key}"
                )

        warehouse_id = package["warehouse"]

        if warehouse_id not in data["warehouses"]:
            raise ValueError(
                f"Package {package['id']} references unknown warehouse "
                f"{warehouse_id}"
            )

        destination = package["destination"]

        if not isinstance(destination, list) or len(destination) != 2:
            raise ValueError(
                f"Invalid destination for package {package['id']}"
            )

    return data


def calculate_distance(point1, point2):
    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_agent(current_positions, warehouse_position):
    min_distance = float("inf")
    nearest_agent = None

    for agent_id, agent_position in current_positions.items():
        distance = calculate_distance(
            agent_position,
            warehouse_position
        )

        if distance < min_distance:
            min_distance = distance
            nearest_agent = agent_id

    return nearest_agent, min_distance


def simulate_deliveries(data):
    report = {}

    for agent_id in data["agents"]:
        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0
        }

    current_positions = copy.deepcopy(data["agents"])
    routes = []

    for package in data["packages"]:
        warehouse_id = package["warehouse"]
        warehouse_position = data["warehouses"][warehouse_id]
        destination = package["destination"]

        nearest_agent, agent_to_warehouse = find_nearest_agent(
            current_positions,
            warehouse_position
        )

        warehouse_to_destination = calculate_distance(
            warehouse_position,
            destination
        )

        total_distance = (
            agent_to_warehouse + warehouse_to_destination
        )

        # Update agent's current position after delivery
        current_positions[nearest_agent] = destination

        # Update report
        report[nearest_agent]["packages_delivered"] += 1
        report[nearest_agent]["total_distance"] += total_distance

        # Store route information
        routes.append(
            f'{package["id"]}: {nearest_agent} -> {warehouse_id} '
            f'-> Destination({destination[0]},{destination[1]})'
        )

    return report, routes


def calculate_efficiency(report):
    best_agent = None
    best_efficiency = float("inf")

    for agent_id, stats in report.items():
        packages = stats["packages_delivered"]
        distance = stats["total_distance"]

        if packages > 0:
            efficiency = distance / packages

            stats["efficiency"] = round(efficiency, 2)

            if efficiency < best_efficiency:
                best_efficiency = efficiency
                best_agent = agent_id

        else:
            stats["efficiency"] = 0

    return best_agent


def validate_package_count(report, expected_count):
    total_delivered = sum(
        stats["packages_delivered"]
        for stats in report.values()
    )

    if total_delivered != expected_count:
        raise ValueError(
            f"Package delivery count mismatch: "
            f"expected {expected_count}, got {total_delivered}"
        )


def save_report(report, best_agent):
    final_report = {}

    for agent_id, stats in report.items():
        final_report[agent_id] = {
            "packages_delivered": stats["packages_delivered"],
            "total_distance": round(stats["total_distance"], 2),
            "efficiency": stats["efficiency"]
        }

    final_report["best_agent"] = best_agent

    with open("report.json", "w") as file:
        json.dump(final_report, file, indent=4)


def save_routes(routes):
    with open("routes.txt", "w") as file:
        file.write("\n".join(routes))


def save_top_performers(report):
    performers = []

    for agent_id, stats in report.items():
        if stats["packages_delivered"] > 0:
            performers.append({
                "agent_id": agent_id,
                "packages_delivered": stats["packages_delivered"],
                "total_distance": round(stats["total_distance"], 2),
                "efficiency": stats["efficiency"]
            })

    performers.sort(key=lambda x: x["efficiency"])

    with open("top_performers.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "agent_id",
                "packages_delivered",
                "total_distance",
                "efficiency"
            ]
        )

        writer.writeheader()
        writer.writerows(performers)


def main():
    data = load_data("data.json")

    report, routes = simulate_deliveries(data)

    best_agent = calculate_efficiency(report)

    validate_package_count(
        report,
        len(data["packages"])
    )

    save_report(report, best_agent)
    save_routes(routes)
    save_top_performers(report)

    print("Simulation completed successfully.")
    print(f"Packages processed: {len(data['packages'])}")
    print(f"Best agent: {best_agent}")


if __name__ == "__main__":
    main()