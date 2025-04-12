from strongconnect import tarjan_scc
from find_example_solution import find_example_solution, print_solution
from topologicalsort import topological_sort_sccs

def parse_input():
    """Ask user for input method and parse the 2SAT problem."""
    print("How would you like to provide input?")
    print("1. Manual input")
    print("2. From file")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print("Enter the number of variables:")
        num_vars = int(input())
        print("Enter the clauses separated by semicolons (e.g., '1 -2;-1 2;-1 -2;1 -3'):")
        clauses_str = input()
    elif choice == '2':
        file_path = input("Enter the path to the input file: ")
        with open(file_path, 'r') as file:
            num_vars = int(file.readline().strip())
            clauses_str = file.readline().strip()
    else:
        print("Invalid choice. Defaulting to manual input.")
        print("Enter the number of variables:")
        num_vars = int(input())
        print("Enter the clauses separated by semicolons (e.g., '1 -2;-1 2;-1 -2;1 -3'):")
        clauses_str = input()

    # Parse clauses
    clauses = []
    for clause_str in clauses_str.split(';'):
        literals = list(map(int, clause_str.split()))
        clauses.append(literals)

    return num_vars, clauses


def create_implication_graph(num_vars, clauses):
    """Create the implication graph for the 2SAT problem."""
    # The graph has 2*num_vars nodes: for each variable i,
    # node 2*i represents i and node 2*i+1 represents -i
    n = 2 * num_vars
    graph = [[0 for _ in range(n)] for _ in range(n)]

    # Convert literal to node index
    def literal_to_node(literal):
        if literal > 0:
            return 2 * (literal - 1)
        else:
            return 2 * (abs(literal) - 1) + 1

    # For each clause (a or b), add implications (-a => b) and (-b => a)
    for clause in clauses:
        a, b = clause
        not_a = -a
        not_b = -b

        # Add edge -a => b
        graph[literal_to_node(not_a)][literal_to_node(b)] = 1

        # Add edge -b => a
        graph[literal_to_node(not_b)][literal_to_node(a)] = 1

    return graph


def check_satisfiability(num_vars, sccs):
    """Check if the 2SAT formula is satisfiable by ensuring no variable and its negation are in the same SCC."""
    for scc in sccs:
        # Convert node indices to variable indices
        var_set = set()
        for node in scc:
            var = node // 2
            is_negated = node % 2 == 1
            var_set.add((var, is_negated))

        # Check if any variable and its negation are in the same SCC
        for var, is_negated in var_set:
            if (var, not is_negated) in var_set:
                return False

    return True


def main():
    # Parse input
    num_vars, clauses = parse_input()

    # Create implication graph
    graph = create_implication_graph(num_vars, clauses)

    # Find strongly connected components
    sccs = tarjan_scc(graph)

    # Check satisfiability
    is_satisfiable = check_satisfiability(num_vars, sccs)

    # Output result
    if is_satisfiable:
        print("The formula is satisfiable.")

        sorted_scc_indices = topological_sort_sccs(graph, sccs)

        # Find an example solution
        solution = find_example_solution(sccs, sorted_scc_indices, num_vars)

        # Print the solution
        print_solution(solution)
    else:
        print("The formula is unsatisfiable.")


if __name__ == "__main__":
    main()
