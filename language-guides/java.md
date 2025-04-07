# Java

## Data structures

### Hashset

Python:
```py
s = set()
s.add(elem)
s.remove(elem)
contains: bool = elem in s
```

Java:
```java
HashSet<T> s = new HashSet<>();
s.add(elem);
s.remove(elem);
boolean contains = s.contains(elem);
```

### Hashmap, defaultdict

Python:
```py
d = dict()
d[k] = v
del d[k]

d = defaultdict(lambda: [])
d[k].append(v)
```

Java:
```java
HashMap<K, V> d = new HashMap<>();
d.put(k, v);
d.remove(k);

HashMap<K, List<V>> d = new HashMap<>();
d.computeIfAbsent(k, key -> new ArrayList<>()).add(v);
```

### Queue/deque

Python:
```py
q = deque()
q.append(x)
q.appendleft(x)
last = q.pop()
first = q.popleft()
```

Java:
```java
Deque<T> q = new LinkedList<>();
q.addLast(x);
q.addFirst(x);
T last = q.removeLast();
T first = q.removeFirst();
```

### Heap

Python:
```py
min_heap = []
heappush(min_heap, x)
x = -1 * min_heap[0]
x = heappop(min_heap)

max_heap = []
heappush(max_heap, -x)
x = -1 * heappop(max_heap)
```

Java:
```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.add(x);
int x = minHeap.peek();
int x = minHeap.poll();

PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
maxHeap.add(x);
int x = maxHeap.peek();
int x = maxHeap.poll();
```

### BST

Python:
```py
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

Java:
```java
TreeSet<Integer> s = new TreeSet<>();
s.add(x);
s.remove(x);
T e = s.ceiling(x); // smallest element >= x
T e = s.lower(x); // largest element < x
T e = s.higher(x); // smallest element > x
T e = s.floor(x); // largest element <= x
```

## Common tasks

### Sorting (by key and with custom comparator)

Python:
```py
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

Java:
```java
public record Pair(int fst, int snd) {}

public static void main(String[] args) {
    List<Pair> v = new ArrayList<>();

    v.sort(Comparator.comparingInt(Pair::snd).reversed());

    Comparator<Pair> cmp = new Comparator<>() {
        @Override
        public int compare(Pair a, Pair b) {
            return b.snd() - a.snd();
        }
    };
    v.sort(cmp);
}
```

## Algorithms

### Binary search

Python:
```py
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

Java:
```java
int l = 0, r = v.length - 1;
while (l <= r) {
    int m = l + (r - l) / 2;
    if (x < v[m]) {
        r = m - 1;
    } else if (v[m] < x) {
        l = m + 1;
    } else {
        return m;
    }
}
return -1;
```

### DFS

Python:
```py
visited = set()

def dfs(node):
    if node in visited:
        return
    visited.add(node)

    for neighbour in neighbours[node]:
        dfs(neighbour)

dfs(start)
```

Java:
```java
public static void main(String[] args) {
    Map<Integer, List<Integer>> neighbours = new HashMap<>();
    Set<Integer> visited = new HashSet<>();
    dfs(start, neighbours, visited);
}

public static void dfs(int node, Map<Integer, List<Integer>> neighbours, Set<Integer> visited) {
    if (visited.contains(node)) {
        return;
    }
    visited.add(node);
    for (int neighbour : neighbours.getOrDefault(node, new ArrayList<>())) {
        dfs(neighbour);
    }
}
```

### BFS

Python:
```py
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

Java:
```java
public record NodeDistance(int node, int dist) {}

public static void main(String[] args) {
    Map<Integer, List<Integer>> neighbours = new HashMap<>();
    bfs(neighbours, start);
}

public static void bfs(Map<Integer, List<Integer>> neighbours, int start) {
    Set<Integer> visited = new HashSet<>();
    Map<Integer, Integer> nodeToDist = new HashMap<>();
    // [(node, distance)]
    Queue<NodeDistance> q = new LinkedList<>();

    q.add(new NodeDistance(start, 0));
    visited.add(start);

    while (!q.isEmpty()) {
        NodeDistance x = q.poll();
        nodeToDist.put(x.node(), x.dist());
        for (int neighbour : neighbours.getOrDefault(x.node(), new ArrayList<>())) {
            if (visited.contains(neighbour))
                continue;
            visited.add(neighbour);
            q.add(new NodeDistance(neighbour, x.dist() + 1));
        }
    }
}
```


### Dijkstra

Python:
```py
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

Java:
```java
public static void main(String[] args) {
    Map<Integer, Map<Integer, Integer>> neighbours = new HashMap<>();
    int start = 0;
    dijkstra(neighbours, start);
}

public record DistNode(int dist, int node) {}

public static void dijkstra(Map<Integer, Map<Integer, Integer>> neighbours, int start) {
    Set<Integer> visited = new HashSet<>();
    Map<Integer, Integer> dist = new HashMap<>();
    for (int node : neighbours.keySet()) {
        dist.put(node, Integer.MAX_VALUE);
    }
    PriorityQueue<DistNode> pq = new PriorityQueue<>(Comparator.comparingInt(DistNode::dist));

    dist.put(start, 0);
    pq.add(new DistNode(dist.get(start), start));

    while (!pq.isEmpty()) {
        DistNode x = pq.poll();
        int d = x.dist();
        int node = x.node();

        if (visited.contains(node))
            continue;
        visited.add(node);
        
        dist.put(node, d);

        for (Map.Entry<Integer, Integer> entry : neighbours.getOrDefault(node, new HashMap<>()).entrySet()) {
            int neighbour = entry.getKey();
            int weight = entry.getValue();
            if (visited.contains(neighbour))
                continue;

            pq.add(new DistNode(d + weight, neighbour));
        }
    }
}
```

### DP

Python:
```py
dp = [None for _ in range(0, n)]

for i in range(0, n):
    if i <= 1:
        dp[i] = 1
    else:
        dp[i] = dp[i-1] + dp[i-2]

return dp[n-1]
```

Java:
```java
int[] dp = new int[n];
List<Integer> dp = new ArrayList<>(Collections.nCopies(n, -1));
for (int i = 0; i < n; i++) {
    if (i <= 1) {
        dp[i] = 1;
    } else {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
}
return dp[n - 1];
```

