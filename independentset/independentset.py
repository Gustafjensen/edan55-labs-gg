import math

def readAdjacencyMatrix(filename):
    V = []
    E = {}
    with open(filename) as f:
        data = f.read().split()
    nodes = int(data[0])
    for i in range(nodes):
        V.append(i)
        E[i] = []
    idx = 1
    row = 0
    for adj in data[1:]:
        if int(adj) == 1:
            E[row].append(idx - 1)
        if idx == nodes:
            idx = 1
            row += 1
        else:
            idx += 1   
    return (V,E)
    
R0_count = 0
R1_count = 0
R2_count = 0

def independentSetR0(graph, memo=None):
    global R0_count
    R0_count += 1
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    if V in memo:
        return memo[V]
        
    for v in V:
        active_neighbors = set(E[v]) & V
        if len(active_neighbors) == 0:
            res = 1 + independentSetR0((V - {v}, E), memo)
            memo[V] = res
            return res

    u = max(V, key=lambda v: len(set(E[v]) & V))
    
    res_exclude = independentSetR0((V - {u}, E), memo)
    
    neighbors = set(E[u]) & V
    res_include = 1 + independentSetR0((V - {u} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]

def independentSetR1(graph, memo=None):
    global R1_count
    R1_count += 1
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    for v in V:
        active_neighbors = set(E[v]) & V
        if len(active_neighbors) == 1:
            return 1 + independentSetR1((V - {v} - active_neighbors, E), memo)
        elif len(active_neighbors) == 0:
            return 1 + independentSetR1((V - {v}, E), memo)

    if V in memo:
        return memo[V]
        
    u = max(V, key=lambda v: len(set(E[v]) & V))
    
    res_exclude = independentSetR1((V - {u}, E), memo)
    
    neighbors = set(E[u]) & V
    res_include = 1 + independentSetR1((V - {u} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]

def independentSetR2(graph, memo=None):
    global R2_count
    R2_count += 1
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    for v in V:
        active_neighbors = list(set(E[v]) & V)
        degree = len(active_neighbors)
        
        if degree == 1:
            return 1 + independentSetR2((V - {v} - set(active_neighbors), E), memo)
        elif degree == 0:
            return 1 + independentSetR2((V - {v}, E), memo)
        elif degree == 2:
            u, w = active_neighbors[0], active_neighbors[1]
            if(u in E[w] or w in E[u]):
                return 1 + independentSetR2((V - {v, u, w}, E), memo)
            else:
                z = -v
                z_neighbors = list((set(E[u]) | set(E[w])) - {v, u, w})
                new_E = E.copy()
                new_E[z] = z_neighbors
                for neighbor in z_neighbors:
                    new_E[neighbor] = list((set(E[neighbor]) - {u, w}) | {z})
                return 1 + independentSetR2((V - {v, u, w} | {z}, new_E), memo)

    if V in memo:
        return memo[V]
        
    u = max(V, key=lambda v: len(set(E[v]) & V))
    
    res_exclude = independentSetR2((V - {u}, E), memo)
    
    neighbors = set(E[u]) & V
    res_include = 1 + independentSetR2((V - {u} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]

for filename in ["data/g30.in", "data/g40.in", "data/g50.in", "data/g60.in"]:
    R0_count = 0
    res = independentSetR0(readAdjacencyMatrix(filename))
    print(f"{filename}: MIS={res}, Nodes visited={round(math.log(R0_count), 1)}")

print("---")

for filename in ["data/g30.in", "data/g40.in", "data/g50.in", "data/g60.in", "data/g70.in", "data/g80.in", "data/g90.in", "data/g100.in"]:
    R1_count = 0
    res = independentSetR1(readAdjacencyMatrix(filename))
    print(f"{filename}: MIS={res}, Nodes visited={round(math.log(R1_count), 1)}")

print("---")

for filename in ["data/g30.in", "data/g40.in", "data/g50.in", "data/g60.in", "data/g70.in", "data/g80.in", "data/g90.in", "data/g100.in", "data/g110.in", "data/g120.in"]:
    R2_count = 0
    res = independentSetR2(readAdjacencyMatrix(filename))
    print(f"{filename}: MIS={res}, Nodes visited={round(math.log(R2_count), 1)}")


            

        
        
    