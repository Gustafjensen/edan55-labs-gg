from collections import defaultdict

def read_graph(filename):
    with open(filename + ".gr") as f_gr:
        n, m = 0, 0
        adj = defaultdict(set)
        v_G = []
        for line in f_gr:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "c":
                continue
            elif parts[0] == "p":
                n, m = int(parts[2]), int(parts[3])
            else:
                u, v = int(parts[0]), int(parts[1])
                v_G.append((u,v))
                adj[u].add(v)
                adj[v].add(u)
    
    with open(filename + ".td") as f_td:
        num_bags, max_bags, vertices = 0, 0, 0
        bags = {}
        tree_edges = []
        for line in f_td:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "c":
                continue
            elif parts[0] == "s":
                num_bags, max_bags, vertices = int(parts[2]), int(parts[3]), int(parts[4])
            elif parts[0] == "b":
                bag_id = int(parts[1])
                bags[bag_id] = [int(v) for v in parts[2:]]
            else:
                u, v = int(parts[0]), int(parts[1])
                tree_edges.append((u, v))
                
    return {
        "graph_n": n,
        "graph_m": m,
        "v_G": v_G,
        "adj": adj,
        "num_bags": num_bags,
        "max_bags": max_bags,
        "vertices": vertices,
        "bags": bags,
        "tree_edges": tree_edges
    }



