
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
    
def independentSetR0(graph, memo=None):
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    if V in memo:
        return memo[V]
        
    v_max = max(V, key=lambda v: len(E[v]))
    
    res_exclude = independentSetR0((V - {v_max}, E), memo)
    
    neighbors = set(E[v_max]) & V
    res_include = 1 + independentSetR0((V - {v_max} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]

def independentSetR1(graph, memo=None):
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    for v in V:
        if(len(set(E[v]) & V) == 1):
            return 1 + independentSetR1((V - {v} - set(E[v]), E), memo)

    if V in memo:
        return memo[V]
        
    v_max = max(V, key=lambda v: len(E[v]))
    
    res_exclude = independentSetR1((V - {v_max}, E), memo)
    
    neighbors = set(E[v_max]) & V
    res_include = 1 + independentSetR1((V - {v_max} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]

def independentSetR2(graph, memo=None):
    if memo is None:
        memo = {}
        
    V, E = graph
    V = frozenset(V)
    if not V:
        return 0

    for v in V:
        if(len(set(E[v]) & V) == 2):
            u, w = E[v][0], E[v][1]
            if(u in E[w] and w in E[u]):
                return 1 + independentSetR2((V - {v} - set(E[v]), E), memo)
            else:
                return 1 + independentSetR2((V - {v} - set(E[v]) | {-v}, E | {-v: E[u] + E[w]}), memo)
        if(len(set(E[v]) & V) == 1):
            return 1 + independentSetR2((V - {v} - set(E[v]), E), memo)

    if V in memo:
        return memo[V]
        
    v_max = max(V, key=lambda v: len(E[v]))
    
    res_exclude = independentSetR2((V - {v_max}, E), memo)
    
    neighbors = set(E[v_max]) & V
    res_include = 1 + independentSetR2((V - {v_max} - neighbors, E), memo)
    
    memo[V] = max(res_exclude, res_include)
    return memo[V]
    
print(independentSetR2(readAdjacencyMatrix("data/g50.in")))

            

        
        
    