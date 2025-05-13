# Java

## Data structures

### Tuple

Java doesn't have tuples, so we have two ways of mimicing them:

1. We can pretend that a fixed size array is a tuple, but this isn't very type-safe, as the caller doesn't know how many elements the returned "tuple" contains.
We're also restricted to one type.

Python:
```python
def get_tuple() -> Tuple[int, int]:
    return (10, 20)
```

Java:
```java
int[] getTuple() {
    return new int[]{ 10, 20 };
}
```

2. We can create a record class with named fields.

Python:
```python
def get_tuple() -> Tuple[int, str]:
    return (10, "hello")
```

Java:
```java
// note that fields of a records are final, so reassigning record field values is impossible.
record Pair(Integer a, String b) {}
Pair getTuple() {
    return new Pair(10, "hello");
}
```

### Optional

Python:
```python
def get_option() -> int | None:
    if 10 == 11:
        return 42
    else:
        return None

if (some := get_option()) is not None:
    ...
else:
    ...

value = some if (some := get_option()) is not None else getDefault()

# get arg if non-None, else default value.
value = some if (some := getSthOrNone()) is not None else default

match (opt_a, opt_b):
    case (None, None):
        pass
    case (some, None):
        pass
    case (None, some):
        pass
    case (some_a, some_b):
        pass
```

Java:
```java
Optional<Integer> getOptional() {
    if (10 == 11) {
        return Optional.of(42);
    } else {
        return Optional.empty();
    }
}

Optional<Integer> opt;
if ((opt = getOptional()).isPresent()) {
    int some = opt.get();
    ...
} else {
    ...
}

var value = getOptional().orElseGet(() -> getDefault());

// get arg if non-null, else default value.
var value = Optional.ofNullable(getSthOrNone()).orElse(default);
```

### Array

Python: doesn't have fixed size arrays.

Java:
```java
// primitive types: init elements with default, e.g. 0 for ints.
int[] a = new int[5];
// reference types: init elements with null.
String[] s = new String[10];

// arrays are fixed size.
var numElements = a.length;

var x = a[0];

a[1] = 10;
// throws ArrayIndexOutOfBoundsException
a[5] = 10;
```

### List/vector

Python:
```python
v = [1, 2, 3]
e = v[1]
v.append(2)
# remove element at index 1.
del v[1]

# pop last element.
last = v.pop()
```

Java:
```java
List<Integer> v = new ArrayList<>(Arrays.asList(1, 2, 3));
int e = v.get(1);
v.add(2);
// remove element at index 1.
v.remove(1);
// convert from List<T> to T[].
int[] arr = v.stream().mapToInt(Integer::intValue).toArray();

// Pop last element, isn't included in List API.
ArrayList<Integer> v2 = new ArrayList<>(Arrays.asList(1, 2, 3));
var last = v2.remove(v2.size() - 1);
```

### Strings

Python:
```python
a = "hello"
b = "world"

# convert int to str.
x = 1
x_str = str(x)

# concatenation (creates new allocation).
c = a + b
c = f"{a}{b}"

// substring.
// optional start: inclusive, optional end: exclusive, both can be out of bounds, which will truncate to start/end.
sub = a[start:end]
sub = a[:end]
sub = a[start:]

# find index of start of next occurence of substring in s[start:end].
if (at_idx := s.find(substring, start, end)) != -1:
    ...
else:
    ...

# joining by adding separator between each elements.
d = ",".join(["one", "two", "three"])

# split string and map elements.
nums = [int(num) for num in "1,2,3".split(",")]

# iterate over chars in a word.
for c in s:
    pass
```

Java:
```java
String a = "hello";
String b = "world";

// convert int to string.
int x = 1;
String xString = Integer.toString(x);
xString = String.format("%d", x);

// format specifiers:
// %s : string
// %d : decimal integer
// %f : float, double
// %c : char

// concatenation (creates new allocation);
String c = a + b;
c = String.format("%s%s", a, b);

// substring that allocates, and start and end must be valid.
String substring = a.substring(start, end);

// find idx of next occurence.
int idx;
if ((idx = a.indexOf('l', start)) != -1) {
    ...
} else {
    ...
}

// substring with zero-copy.
CharBuffer buf = CharBuffer.wrap(a);
buf.position(start).limit(end);
CharSequence view = buf.slice();

// joining by adding separator between each elements.
String d = List.of("one", "two", "three").stream().collect(Collectors.joining(","));
d = String.join(",", List.of("one", "to", "three"));

// split string and map elements.
// String.split returns String[], so has no .stream() method.
List<Integer> nums = Arrays.stream("1,2,3".split(",")).map(Integer::parseInt).collect(Collectors.toList());

// iterate over chars in a word.
// 1. bad: makes a whole copy, returning a char[].
for (char c : word.toCharArray()) {
    ...
}
// 2. fast, but not stream-able:
for (int i = 0; i < s.length(); ++i) {
    char c = s.charAt(i);
    ...
}
// 3. fast, stream-able:
Iterable<Character> chars = () -> word.chars().mapToObj(charInt -> (char)charInt).iterator();
for (Character c : chars) {
    ...
}
```

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
d = { "key": "value" }

# get: will raise exception if key doesn't exist.
v = d[k]
# get or default
v = d.get(k, default)

d[k] = v
del d[k]

d = defaultdict(lambda: [])
d[k].append(v)

d = defaultdict(lambda: 0)
d[k] += 1

if (value := d.get(k, None)) is not None:
    ...
else:
    ...

# iterate over hashmap to hashmap.
d = defaultdict(lambda: {})
for (b, c) in d[a].items():
    ...
```

Java:
```java
Map<K, V> d = new HashMap<>();
Map<K, V> d = new HashMap<>(Map.of("key", "value"));


// get: will return null if key doesn't exist.
var v = d.get(k);
// get or default
var v = d.getOrDefault(k, default);

d.put(k, v);
d.remove(k);

HashMap<K, List<V>> d = new HashMap<>();
// computeIfAbsent = lazy init, putIfAbsent = eager init.
d.computeIfAbsent(k, key -> new ArrayList<>()).add(v);
d.putIfAbsent(k, new ArrayList<>()).add(v);

HashMap<K, Integer> d = new HashMap<>();
d.put(k, d.getOrDefault(k, 0) + 1);

T value;
if ((value = d.get(k)) != null) {
    ...
} else {
    ...
}

// iterate over hashmap to hashmap.
Map<Integer, Map<Integer, Integer>> d = new HashMap<>();
for (var entry : d.getOrDefault(a, Map.of()).entrySet()) {
    var b = entry.getKey();
    var c = entry.getValue();
    ...
}
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
// min heap
min_heap = []
heappush(min_heap, x)
x = -1 * min_heap[0]
x = heappop(min_heap)

// max heap
max_heap = []
heappush(max_heap, -x)
x = -1 * heappop(max_heap)
```

Java:
```java
// min heap
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.add(x);
int x = minHeap.peek();
int x = minHeap.poll();

// max heap
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

### Sorting

Python:
```py
v = [(1, 2), (2, 1), (3, 0)]

# sort by key: asc by first, desc by len(snd), desc by third.
def key(item):
    # fst = int, snd = str, thd = float
    fst, snd, thd = item
    return fst, -len(snd), -thd

v.sort(key=key)

# sort using custom comparator.
def cmp(a, b):
    # -1: a < b
    # 0: a == b
    # 1: a > b
    a_fst, a_snd, a_thd = a
    b_fst, b_snd, b_thd = b
    return len(b_snd) - len(a_snd)

v.sort(key=functools.cmp_to_key(cmp))
```

Java:
```java
public record Tuple(int fst, String snd, double thd) {}

public static void main(String[] args) {
    List<Tuple> v = new ArrayList<>();

    // sort by key: asc by first, desc by len(snd), desc by third.
    var comparator = Comparator.comparingInt(Tuple::fst)
        .thenComparing(Comparator.comparingInt(tuple -> tuple.snd().length()).reversed())
        .thenComparing(Comparator.comparingDouble(Tuple::thd).reversed());
    v.sort(comparator);

    // sort using custom comparator.
    Comparator<Tuple> cmp = new Comparator<>() {
        @Override
        public int compare(Tuple a, Tuple b) {
            return b.snd().length() - a.snd().length();
        }
    };
    v.sort(cmp);
}
```

### Inline closures/lambdas

Python:
```python
supplier = lambda: 10

consumer = lambda x: print(x)

function = lambda s: len(s)

predicate = lambda x: x % 2 == 0

bifunction = lambda x, s: x == len(s)
```

Java:
```java
Supplier<Integer> supplier = () -> 10;
Integer supplier_called = supplier.get();

Consumer<Integer> consumer = x -> System.out.println(x);
// we can, optionally, specify the type of the args (rule: specify types of all args, or none of them).
Consumer<Integer> consumer = (Integer x) -> System.out.println(x);
consumer.accept(20);

Function<String, Integer> function = s -> s.length();
function.apply("foo");

Predicate<Integer> predicate = x -> x % 2 == 0;
predicate.test(42);

BiFunction<Integer, String, Boolean> bifunction = (x, s) -> x == s.length();
bifunction.apply(2, "hi");

// BiConsumer and BiPredicate follow naturally.
```
Note that Java lambdas can only capture local variables that are final (cannot be reassigned after capture), and it's the value for primitives and the reference for objects that is captured.


### Iterators/generators/streams.


Python:
```python
# flatmapping nested loops.
def all_cells():
    for r in range(0, rows):
        for c in range(0, cols):
            yield (r, c)

# filtering.
def all_matching_pred():
    for cell in all_cells():
        if pred(cell):
            yield cell

# iterate over anything (iterator, generator).
for e in iterable:
    pass

# collect from iterator to dictionary.
d = {k: k2v(k) for k in keys()}

# get max value in iterator.
max((dp[r][c] for r in range(0, m) for c in range(0, n)), default=0)
```

Java:
```java
// flatmapping nested loops (.boxed() is necessary to convert from primitive to reference type).
Supplier<Stream<Node>> allCells = () -> IntStream.range(0, rows).boxed()
    .flatMap(r -> IntStream.range(0, cols).mapToObj(c -> new Node(r, c)));

// filtering.
Supplier<Stream<Node>> allMatchingPred = () -> allCells.get().filter(pred);

// iterate over stream with lambda body (bad, since it doesn't allow control flow stmts in body).
stream.forEach(elem -> {
    ...
});

// iterate over stream with regular for loop (better).
Iterable<T> iterable = () -> stream.iterator();
for (var elem : iterable) {
    ...
}

// collect from stream to map.
Map<K, V> = keyStream.collect(Collectors.toMap(
    k -> k,
    k -> k2v(k)));

// get max value in stream.
IntStream.range(0, m).flatMap(r -> IntStream.range(0, n).map(c -> dp[r][c])).max().orElse(0);
```

### Exceptions

- Unchecked exceptions:

Python:
```python
def foo():
    raise Exception("error message")

# not forced to handle exceptions.
foo()
```

Java:
```java
void foo() {
    // unchecked exception: any class that extends RuntimeException.
    throw new RuntimeException("error message");
}

// not forced to handle exceptions.
foo();
```

- Checked exceptions:

Python: does not have checked exceptions.

Java:
```java
void foo() throws CheckedException, CheckedException2 {
    // checked exception: any class that extends Exception but not RuntimeException.
    throw new CheckedException("error message");
}

// forced to handle exceptions.
try {
    foo();
} catch (CheckedException e) {
    ...
} catch (CheckedException2 e) {
    ...
}
```

### Match statements

Python:
```python
x = 10
match x:
    case 1:
        print("a")
    case 10 | 20:
        print("b")
    case _:
        print("c")


# match as "expression" (not proper): return from each branch of the match stmt.
match x:
    case 1:
        ret = 10
    case 10:
        ret = 20
    case _:
        ret = 30
```

Java:
```java
int x = 10;
switch (x) {
    case 1 -> System.out.println("a");
    case 10, 20 -> {
        System.out.println("b");
    }
    default -> System.out.println("c");
};

// switch as expression.
var ret = switch(x) {
    case 1 -> 10;
    case 10 -> {
        System.out.println("printing stuff");
        yield 20;
    }
    default -> 30;
};
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
    Queue<NodeDistance> q = new ArrayDeque<>();

    q.add(new NodeDistance(start, 0));
    visited.add(start);

    while (!q.isEmpty()) {
        NodeDistance x = q.poll();
        nodeToDist.put(x.node(), x.dist());
        for (int neighbour : neighbours.getOrDefault(x.node(), List.of())) {
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

        for (Map.Entry<Integer, Integer> entry : neighbours.getOrDefault(node, Map.of()).entrySet()) {
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

