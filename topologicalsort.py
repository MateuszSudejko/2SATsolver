def create_condensed_graph(adj_matrix, sccs):
    """
    Create a condensed graph where each SCC is treated as a single vertex.

    Args:
        adj_matrix: The original adjacency matrix
        sccs: List of strongly connected components

    Returns:
        condensed_adj_matrix: Adjacency matrix of the condensed graph
        scc_mapping: Mapping from original vertices to SCC indices
    """
    n = len(adj_matrix)
    num_sccs = len(sccs)

    # Create a mapping from original vertices to SCC indices
    scc_mapping = [-1] * n
    for i, scc in enumerate(sccs):
        for vertex in scc:
            scc_mapping[vertex] = i

    # Create the condensed adjacency matrix
    condensed_adj_matrix = [[0 for _ in range(num_sccs)] for _ in range(num_sccs)]

    # For each edge in the original graph, add an edge in the condensed graph if it connects different SCCs
    for u in range(n):
        for v in range(n):
            if adj_matrix[u][v] == 1:
                scc_u = scc_mapping[u]
                scc_v = scc_mapping[v]
                if scc_u != scc_v:  # Only add edges between different SCCs
                    condensed_adj_matrix[scc_u][scc_v] = 1

    return condensed_adj_matrix, scc_mapping


def kahn_topological_sort(adj_matrix):
    """
    Perform topological sorting using Kahn's algorithm.

    Args:
        adj_matrix: Adjacency matrix of the graph

    Returns:
        sorted_vertices: Topologically sorted list of vertices
    """
    n = len(adj_matrix)

    # Calculate in-degree for each vertex
    in_degree = [0] * n
    for i in range(n):
        for j in range(n):
            if adj_matrix[j][i] == 1:
                in_degree[i] += 1

    # Initialize queue with vertices that have no incoming edges
    queue = []
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    # Process vertices in topological order
    sorted_vertices = []
    while queue:
        u = queue.pop(0)
        sorted_vertices.append(u)

        # Decrease in-degree of adjacent vertices
        for v in range(n):
            if adj_matrix[u][v] == 1:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    # Check if there's a cycle
    if len(sorted_vertices) != n:
        raise ValueError("The graph contains a cycle, topological sort is not possible.")

    return sorted_vertices


def topological_sort_sccs(adj_matrix, sccs):
    """
    Perform topological sorting on the condensed graph where each SCC is a vertex.

    Args:
        adj_matrix: The original adjacency matrix
        sccs: List of strongly connected components

    Returns:
        sorted_scc_indices: Topologically sorted list of SCC indices
    """
    # Create the condensed graph
    condensed_adj_matrix, _ = create_condensed_graph(adj_matrix, sccs)

    # Perform topological sort on the condensed graph
    try:
        sorted_scc_indices = kahn_topological_sort(condensed_adj_matrix)
        return sorted_scc_indices
    except ValueError as e:
        # This shouldn't happen since the condensed graph is a DAG by definition
        print(f"Error: {e}")
        return []


# Example usage and testing
if __name__ == "__main__":
    # Example adjacency matrix
    adj_matrix = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ]

    # Example SCCs
    sccs = [[0, 1, 2], [3]]

    # Perform topological sort
    sorted_scc_indices = topological_sort_sccs(adj_matrix, sccs)
    print("Topologically sorted SCCs:", sorted_scc_indices)
