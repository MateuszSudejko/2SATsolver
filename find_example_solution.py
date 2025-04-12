def find_example_solution(sccs, sorted_scc_indices, num_vars):
    """
    Find an example solution for a satisfiable 2SAT formula.

    Args:
        sccs: List of strongly connected components (list of lists of literals)
        sorted_scc_indices: Topologically sorted list of SCC indices
        num_vars: Number of variables in the formula

    Returns:
        solution: Dictionary mapping each variable to its truth value
    """
    # Initialize solution dictionary
    # We'll use 1-based indexing for variables in the solution
    solution = {}

    # Process SCCs in topological order
    for scc_idx in sorted_scc_indices:
        scc = sccs[scc_idx]

        for node in scc:
            var = node // 2 + 1  # Convert to 1-based indexing
            is_negated = node % 2 == 1

            # If this variable hasn't been assigned yet
            if var not in solution:
                # Assign False to the literal in this SCC
                # This means assigning True to its negation
                if is_negated:
                    solution[var] = True  # Assign True to the variable
                else:
                    solution[var] = False  # Assign False to the variable

    # Make sure all variables are assigned
    for var in range(1, num_vars + 1):
        if var not in solution:
            # If a variable wasn't assigned, we can assign any value
            # Let's default to False
            solution[var] = False

    return solution


def print_solution(solution):
    """
    Print the solution in a readable format.

    Args:
        solution: Dictionary mapping each variable to its truth value
    """
    print("Example solution:")
    for var, value in sorted(solution.items()):
        print(f"Variable {var}: {value}")

    # Also print in the form of a list of literals
    true_literals = []
    false_literals = []
    for var, value in solution.items():
        if value:
            true_literals.append(var)
            false_literals.append(-var)
        else:
            true_literals.append(-var)
            false_literals.append(var)

    print("\nTrue literals:", sorted(true_literals))
    print("False literals:", sorted(false_literals))


# Example usage
if __name__ == "__main__":
    # Example SCCs (using node indices)
    # For a graph with 3 variables (6 nodes)
    sccs = [[0, 3], [1], [2, 5], [4]]

    # Example topologically sorted SCC indices
    sorted_scc_indices = [3, 2, 1, 0]

    # Number of variables
    num_vars = 3

    # Find an example solution
    solution = find_example_solution(sccs, sorted_scc_indices, num_vars)

    # Print the solution
    print_solution(solution)
