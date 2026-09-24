import json
import shutil
import subprocess


DATA_FILE = "data.json"
TEST_FOLDER = "test_cases"


def run_test(test_file):
    # Save the current data.json
    backup_file = "data_backup.json"
    shutil.copy(DATA_FILE, backup_file)

    # Use the test case as data.json
    shutil.copy(test_file, DATA_FILE)

    try:
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False, f"Program crashed:\n{result.stderr}"

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        with open("report.json", "r") as file:
            report = json.load(file)

        # Check package count
        total_delivered = sum(
            stats["packages_delivered"]
            for agent_id, stats in report.items()
            if agent_id != "best_agent"
        )

        expected_packages = len(data["packages"])

        if total_delivered != expected_packages:
            return False, (
                f"Package mismatch: expected {expected_packages}, "
                f"got {total_delivered}"
            )

        # Check best agent
        best_agent = report["best_agent"]

        if best_agent not in data["agents"]:
            return False, f"Invalid best agent: {best_agent}"

        if report[best_agent]["packages_delivered"] == 0:
            return False, f"Best agent {best_agent} delivered 0 packages"

        return True, f"{expected_packages} packages delivered"

    finally:
        # Restore original data.json
        shutil.move(backup_file, DATA_FILE)


def main():
    passed = 0
    failed = 0

    for number in range(1, 11):
        test_file = f"{TEST_FOLDER}/test_case_{number}.json"

        success, message = run_test(test_file)

        if success:
            print(f"Test {number}: PASS - {message}")
            passed += 1
        else:
            print(f"Test {number}: FAIL - {message}")
            failed += 1

    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()