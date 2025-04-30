# Python

## Data structures

### Hashset

```python
s = set()
s.add(elem)
s.remove(elem)
contains: bool = elem in s
```

### Hashmap, defaultdict

```python
d = dict()
d[k] = v
del d[k]
d.get(k, default=None)
d.pop(k, default=None)

d = defaultdict(lambda: [])
d[k].append(v)
```

### Queue/deque

```python
q = deque()
q.append(x)
q.appendleft(x)
last = q.pop()
first = q.popleft()
```

### Heap

```python
min_heap = []
heappush(min_heap, x)
x = -1 * min_heap[0]
x = heappop(min_heap)

max_heap = []
heappush(max_heap, -x)
x = -1 * heappop(max_heap)
```

### BST

```python
s = SortedSet()
s.add(x)
s.remove(x)
i = s.bisect_left(x) # idx of smallest value >= x (idx left of x where next val would be inserted)
i = s.bisect_left(x)-1 # idx of largest value < x
i = s.bisect_right(x) # idx of smallest value > x (idx right of x where next val would be inserted)
i = s.bisect_right(x)-1 # idx of largest value <= x

d = SortedDict()
d[k] = v
del d[k]
```

## Common tasks

### Sorting (by key and with custom comparator)

```python
v = [(1, 2), (2, 1), (3, 0)]

def by_snd_desc(item):
    fst, snd = item
    return -snd

v.sort(key=by_snd_desc)

def cmp(a, b):
    # -1: a < b
    # 0: a == b
    # 1: a > b
    a_fst, a_snd = a
    b_fst, b_snd = b
    return b_snd - a_snd

v.sort(key=functools.cmp_to_key(cmp))
```

### Strings

Substring or character search:
```python
if (at_idx := s.find(substring, start, end)) != -1:
    ...
else:
    ...
```

## Algorithms

### Binary search

```python
v = [1, 2, 3]
x = 1
# both inclusive
l, r = 0, len(v)-1
while l <= r:
    m = (l + r) // 2
    if x < v[m]:
        # search left
        r = m-1
    elif v[m] < x:
        # search right
        l = m+1
    else:
        return m
return -1
```

### DFS

```python
visited = set()

def dfs(node):
    if node in visited:
        return
    visited.add(node)

    for neighbour in neighbours[node]:
        dfs(neighbour)

dfs(start)
```

### BFS

```python
visited = set()
# [(node, dist)]
q = deque()
node_to_dist = {}

q.append((start, 0))
visited.add(start)

while len(q) > 0:
    node, dist = q.popleft()

    node_to_dist[node] = dist

    for neighbour in neighbours[node]:
        if neighbour in visited:
            continue
        visited.add(neighbour)
        q.append((neighbour, dist+1))
```

### Dijkstra

```python
visited = set()
dist = {node:float("inf") for node in nodes}
pq = []

dist[start] = 0
heappush(pq, (dist[start], start))

while len(pq) > 0:
    d, node = heappop(pq)

    if node in visited:
        continue
    visited.add(node)

    dist[node] = d

    # neighbours: Dict[src, Dict[dst, weight]]
    for neighbour, w in neighbours[node].items():
        if neighbour in visited:
            continue
        heappush(pq, (dist[node]+w, neighbour))
```

### DP

```python
dp = [None for _ in range(0, n)]

for i in range(0, n):
    if i <= 1:
        dp[i] = 1
    else:
        dp[i] = dp[i-1] + dp[i-2]

return dp[n-1]
```

### Topological sort

```python
neighbours = defaultdict(lambda: set())
# the number of incoming edges.
in_degree = {node:0 for node in all_nodes()}

for u, v in edges:
    neighbours[u].add(v)
    in_degree[v] += 1

order = []
q = deque()

# enqueue the initial nodes with indegree 0
for node in all_nodes():
    if in_degree[node] == 0:
        q.append(node)

while len(q) > 0:
    node = q.popleft()
    order.append(node)

    # "delete" this node (pretend it no longer exists), so all nodes it has an edge to now have in-degree one less.
    for neighbour in neighbours[node]:
        if in_degree[neighbour] == 0:
            # we've already visited this node.
            raise Exception("unreachable, since a node with indegree 0 should have no more incoming edges and should, therefore, never be visited again")

        in_degree[neighbour] -= 1

        if in_degree[neighbour] == 0:
            # neighbour now has no more incoming edges, so can be visited next.
            q.append(neighbour)

num_nodes = len(in_degree.keys())
if len(order) == num_nodes:
    return order
else:
    # we weren't able to visit all nodes, so there must exist a cycle.
    return None
```

### DFS Bridges

```python
# classic bridge finding problem: a bridge is an edge that, if removed, disconnects the graph.
# our strategy for finding bridges is: a tree edge is a bridge if there is no DFS back-edge going "past it back up (towards root)".

neighbours = defaultdict(lambda: [])
for a, b in edges:
    # bidirectional edges
    neighbours[a].append(b)
    neighbours[b].append(a)

bridges = []

i = 0
# we visit nodes in preorder.
preorder = {}
# the highest (closest to root) a node can reach in the dfs tree.
reach = {}

def dfs(node, parent):
    nonlocal i, bridges

    preorder[node] = i
    i += 1
    reach[node] = preorder[node]
    for neighbour in neighbours[node]:
        if neighbour == parent:
            # we're in an undirected graph, so we're not allowed to treat (u,v) and (v,u) as a cycle.
            # therefore, ensure we don't do u -> v -> u.
            continue

        if neighbour not in preorder:
            # neighbour hasn't been visited yet: definitely not a back-edge.
            dfs(neighbour, parent=node)

            # if neighbour can't reach anything earlier than itself, it's (node,neighbour) bridge.
            if reach[neighbour] == preorder[neighbour]:
                # neighbour can only reach itself (this is the default we set at the beginning of dfs).
                bridges.append((node, neighbour))

        # neighbour has been visited now, so its reach value has been set.
        # node reaches as high (close to root) as any of its neighbours.
        reach[node] = min(reach[node], reach[neighbour])

# start from any of the nodes.
start = next(iter(all_nodes()))
dfs(start, parent=None)

return bridges
```

### Bellman Ford

```python
dist = {node:float('inf') for node in all_nodes()}

dist[source] = 0.0

# Relax all edges up to (V - 1) times, because, in the worst case, the shortest path between any two vertices can have at most (V - 1) edges.
for _ in range(num_nodes - 1):
    updated = False

    # Try to improve each edge.
    for u, v, w in edges:
        if (dist_v_via_u := dist[u] + w) < dist[v]:
            # found shorter path to v via u.
            dist[v] = dist_v_via_u
            updated = True

    # Early exit: if no update in this pass, distances are final.
    if not updated:
        break

# Check for negative-weight cycles
# If we can still relax any edge, then there's a cycle with total negative weight.
for u, v, w in edges:
    if dist[u] + w < dist[v]:
        raise ValueError("graph contains a negative-weight cycle")

return dist
```
