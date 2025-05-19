import time
import random
import os
import statistics
from datetime import datetime
import sys

# Import your 2SAT solver modules
sys.path.append('.')  # Ensure current directory is in path
from main import parse_input, create_implication_graph, check_satisfiability
from strongconnect import tarjan_scc


def generate_random_2sat(num_literals, num_clauses):
    """Generate a random 2SAT problem with the specified number of literals and clauses."""
    clauses = []
    for _ in range(num_clauses):
        lit1 = random.randint(1, num_literals)
        lit2 = random.randint(1, num_literals)

        # Randomly negate literals
        if random.random() < 0.5:
            lit1 = -lit1
        if random.random() < 0.5:
            lit2 = -lit2

        # Ensure the two literals are different
        while lit1 == lit2 or lit1 == -lit2:
            lit2 = random.randint(1, num_literals)
            if random.random() < 0.5:
                lit2 = -lit2

        clauses.append(f"{lit1} {lit2}")

    return f"{num_literals}\n{';'.join(clauses)}"


def solve_2sat(problem_str):
    """Solve a 2SAT problem and return whether it's satisfiable and the execution time."""
    start_time = time.time()

    # Parse the problem
    num_literals, clauses = parse_input_from_string(problem_str)

    # Create implication graph
    graph = create_implication_graph(num_literals, clauses)

    # Find strongly connected components
    sccs = tarjan_scc(graph)

    # Check satisfiability
    is_satisfiable = check_satisfiability(num_literals, sccs)

    end_time = time.time()
    execution_time = end_time - start_time

    return is_satisfiable, execution_time


def parse_input_from_string(problem_str):
    """Parse a 2SAT problem from a string."""
    lines = problem_str.strip().split('\n')
    num_literals = int(lines[0])

    clauses = []
    if len(lines) > 1:
        for clause_str in lines[1].split(';'):
            literals = list(map(int, clause_str.split()))
            clauses.append(literals)

    return num_literals, clauses


def run_tests(num_tests, literals_list, clauses_list):
    """Run tests for all combinations of literals and clauses."""
    results = []

    total_tests = len(literals_list) * len(clauses_list)
    test_count = 0

    for num_literals in literals_list:
        for num_clauses in clauses_list:
            test_count += 1
            print(f"Running tests for {num_literals} literals, {num_clauses} clauses ({test_count}/{total_tests})...")

            times = []
            satisfiable_count = 0

            for i in range(num_tests):
                problem = generate_random_2sat(num_literals, num_clauses)
                is_satisfiable, execution_time = solve_2sat(problem)

                times.append(execution_time)
                if is_satisfiable:
                    satisfiable_count += 1

                print(
                    f"  Test {i + 1}/{num_tests}: {'Satisfiable' if is_satisfiable else 'Unsatisfiable'} in {execution_time:.6f} seconds")

            # Calculate statistics
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            satisfiable_percent = (satisfiable_count / num_tests) * 100

            result = {
                'literals': num_literals,
                'clauses': num_clauses,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'satisfiable_percent': satisfiable_percent
            }

            results.append(result)
            print(f"  Average time: {avg_time:.6f} seconds")
            print(f"  Satisfiable: {satisfiable_percent:.2f}%")
            print()

    return results


def save_results(results, output_file=None):
    """Save test results to a file."""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"2sat_test_results_{timestamp}.txt"

    with open(output_file, 'w') as f:
        f.write("2SAT Solver Performance Test Results\n")
        f.write("===================================\n\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("Summary:\n")
        f.write("-" * 80 + "\n")
        f.write(
            f"{'Literals':<10}{'Clauses':<10}{'Avg Time (s)':<15}{'Min Time (s)':<15}{'Max Time (s)':<15}{'Satisfiable %':<15}\n")
        f.write("-" * 80 + "\n")

        for result in results:
            f.write(
                f"{result['literals']:<10}{result['clauses']:<10}{result['avg_time']:<15.6f}{result['min_time']:<15.6f}{result['max_time']:<15.6f}{result['satisfiable_percent']:<15.2f}\n")

    print(f"Results saved to {output_file}")
    return output_file


def main():
    print("2SAT Solver Performance Testing")
    print("===============================")

    try:
        num_tests = int(input("Enter the number of tests for each setting: "))

        literals_input = input("Enter the list of literals to test (comma-separated): ")
        literals_list = [int(x.strip()) for x in literals_input.split(',')]

        clauses_input = input("Enter the list of clauses to test (comma-separated): ")
        clauses_list = [int(x.strip()) for x in clauses_input.split(',')]

        output_file = input("Enter output file name (leave blank for auto-generated): ")
        if not output_file:
            output_file = None

        print("\nRunning tests...")
        results = run_tests(num_tests, literals_list, clauses_list)

        save_results(results, output_file)

    except ValueError:
        print("Error: Please enter valid integer values.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
