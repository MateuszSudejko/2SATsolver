def tarjan_scc(adj_matrix):
    n = len(adj_matrix)
    index = 0
    stack = []
    indices = [-1] * n
    lowlink = [-1] * n
    on_stack = [False] * n
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in range(n):
            if adj_matrix[v][w]:  # There is an edge from v to w
                if indices[w] == -1:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack[w]:
                    lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in range(n):
        if indices[v] == -1:
            strongconnect(v)

    return sccs

# Example usage and testing
if __name__ == "__main__":
    adj_matrix = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1]
    ]
    print("Strongly Connected Components:", tarjan_scc(adj_matrix))
