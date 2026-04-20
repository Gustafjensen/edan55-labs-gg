import random
import time
from collections import defaultdict


def read_graph(filename):
    with open(filename) as f:
        lines = f.read().split()
    idx = 0
    n, m = int(lines[idx]), int(lines[idx+1])
    idx += 2
    edges = []
    adj = defaultdict(list)
    for _ in range(m):
        u, v, w = int(lines[idx]), int(lines[idx+1]), int(lines[idx+2])
        idx += 3
        edges.append((u, v, w))
        adj[u].append((v, w))
        adj[v].append((u, w))
    return n, edges, adj


def cut_value(A, edges):
    return sum(w for u, v, w in edges if (u in A) != (v in A))


def algorithm_r(n, edges, adj):
    A = {v for v in range(1, n+1) if random.randint(0, 1)}
    return cut_value(A, edges)


def algorithm_s(n, edges, adj):
    A = set()
    improved = True
    while improved:
        improved = False
        for v in range(1, n+1):
            gain = sum(w for u, w in adj[v] if (u in A) == (v in A)) \
                 - sum(w for u, w in adj[v] if (u in A) != (v in A))
            if gain > 0:
                if v in A:
                    A.remove(v)
                else:
                    A.add(v)
                improved = True
                break
    return cut_value(A, edges)


def algorithm_rs(n, edges, adj):
    A = {v for v in range(1, n+1) if random.randint(0, 1)}
    improved = True
    while improved:
        improved = False
        for v in range(1, n+1):
            gain = sum(w for u, w in adj[v] if (u in A) == (v in A)) \
                 - sum(w for u, w in adj[v] if (u in A) != (v in A))
            if gain > 0:
                if v in A:
                    A.remove(v)
                else:
                    A.add(v)
                improved = True
                break
    return cut_value(A, edges)


if __name__ == "__main__":
    for filename in ["data/pw09_100.9.txt", "data/matching_1000.txt"]:
        n, edges, adj = read_graph(filename)
        print(f"\n=== {filename} ===")
        for name, algo in [("R", algorithm_r), ("S", algorithm_s), ("RS", algorithm_rs)]:
            start = time.perf_counter()
            results = [algo(n, edges, adj) for _ in range(100)]
            elapsed = time.perf_counter() - start
            if(name == "RS" and filename == "data/matching_1000.txt"):
                for r in results:
                    print(r)
            print(f"  {name}: Avg={sum(results)/100:.1f}  Max={max(results)}  Time={elapsed/100:.6f}s")
