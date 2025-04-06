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

- sorting (by key and with custom comparator)

## Algorithms

- binary search
- dfs
- bfs
- dijkstra
- dp
- backtracking
