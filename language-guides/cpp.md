# Cpp

## Data structures

### Pair

Python:
```python
pair = (10, "hello")

# direct access.
fst = pair[0]
snd = pair[1]

# destructure.
fst, snd = pair
```

Cpp:
```cpp
std::pair<int, std::string> pair_{10, "hello"};

// direct access, by value (bitwise copy for int, copy constructor for std::string).
int fst = pair_.first;
std::string snd = pair_.second;

// direct access, by reference (no copies).
// NOTE: & is not used on the right-hand side, as that would give us a ptr, so whether we access by value or reference depends on left-side type declaration.
int &fst = pair_.first;
std::string &snd = pair_.second;

// destructure, by value (bitwise copy for int, copy constructor for std::string).
auto [fst, snd] = pair_;

// destructure, by reference (no copies).
auto &[fst_ref, snd_ref] = pair_;
```

### Tuple

Python:
```python
t = (10, "hello", 4.5)

# direct access.
fst = t[0]
snd = t[1]
thd = t[2]

# destructure.
fst, snd, thd = t

# ignore some elements during destructuring.
_, snd, _ = t
```

Cpp:
```cpp
std::tuple<int, std::string, float> t{10, "hello", 4.5};

// direct access, by value (bitwise copy for int, copy constructor for std::string, bitwise copy for float).
// NOTE: std::get<N> makes use of non-type (comptime constant) template parameter N.
int fst = std::get<0>(t);
std::string snd = std::get<1>(t);
float thd = std::get<2>(t);

// direct access, by reference (no copies).
int &fst = std::get<0>(t);
std::string &snd = std::get<1>(t);
float &thd = std::get<2>(t);

// destructure, by value (bitwise copy for int, copy constructor is invoked for std::string).
auto [fst, snd, thd] = t;

// destructure, by reference (no copies).
auto &[fst_ref, snd_ref, thd_ref] = t;

// destructure into existing/declared variables, always copies.
int fst;
std::string snd;
float thd;
std::tie(fst, snd, thd) = t;

// ignore some of the elements during destructuring.
auto [_, snd, _] = t;
std::tie(std::ignore, snd, std::ignore) = t;

// NOTE: impossible to use std::tie to get references, because references must always be valid, hence the following is invalid cpp:
std::string &snd;
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

value = some if (some := get_option()) is not None else get_default()

# get arg if non-None, else default value.
value = some if (some := get_option()) is not None else default_value

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

Cpp:
```cpp
std::optional<int> get_option() {
    if (10 == 11) {
        return 42;
    } else {
        return std::nullopt;
    }
}

if (auto opt = get_option(); opt.has_value()) {
    int some = opt.value();
    ...
} else {
    ...
}

// std::optional<T> defines an implicit `operator bool()` that returns the same value as `has_value()`, so these two are equivalent:
if (opt.has_value()) {
    ...
}
if (opt) {
    ...
}

// eagerly evaluated default.
int value = get_option().value_or(get_default());

// lazily evaluated default: only in C++23.
int value = get_option().or_else([]{ return std::optional{get_default()}; }).value();

std::optional<int> opt_a = get_a();
std::optional<int> opt_b = get_b();
if (!opt_a && !opt_b) {
    ...
} else if (opt_a && !opt_b) {
    ...
} else if (!opt_a && opt_b) {
    ...
} else if (opt_a && opt_b) {
    ...
}
```

### Array

Python: doesn't have fixed size arrays.

Cpp:
```cpp
// 1. C-style built-in array (works for any type, not just primitives).
int a1[5];           // elements are uninitialized (indeterminate).
int a2[5] = {};      // value-initialized: all elements == 0.

// length (compile-time constant)
constexpr std::size_t len1 = sizeof(a2) / sizeof(a2[0]);

int x = a2[0];
a2[1] = 10;
a2[5] = 10;          // out of bounds access is UB!!!

// 2. std::array for fixed-size array.
std::array<int, 5> arr{};         // value-initialized: all zeros

std::size_t len2 = arr.size();    // length at runtime

int y = arr[0];
arr[1] = 10;
arr[5] = 10;         // out of bounds access is UB!!!

try {
    arr.at(5) = 10;  // throws std::out_of_range if index >= size()
}
catch (const std::out_of_range& e) {
    std::cerr << "Out of range: " << e.what() << "\n";
}
```

### List/vector

Python:
```python
v = [1, 2, 3]
e = v[1]
v.append(2)
# remove element at index 1, and shift rest over.
del v[1]

# pop last element.
last = v.pop()
```

Cpp:
```cpp
std::vector<int> v{1, 2, 3};

int e = v[1];     // unchecked, UB if out of bounds.
int e = v.at(1);  // bounds-checked, throws std::out_of_range if invalid.

v.push_back(2);
v.emplace_back(2);  // instead of constructing a new value, and then having it be copied to the vector's memory, just pass args, which constructs the object in-place.

// remove element at index 1, and shift rest over.
v.erase(v.begin() + 1);

int last = v.back();
v.pop_back();
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

# substring.
# optional start: inclusive, optional end: exclusive, both can be out of bounds, which will truncate to start/end.
sub = a[start:end]
sub = a[:end]
sub = a[start:]

# find index of start of next occurence of pattern in s[start:end].
if (at_idx := s.find(pattern, start, end)) != -1:
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

Cpp:
```cpp
std::string a = "hello";
std::string b = "world";

// convert int to string.
int x = 1;
std::string x_str1 = std::to_string(x);
std::string x_str2 = std::format("{}", x);         // C++20

// concatenation (allocates new string).
std::string c1 = a + b;
std::string c2 = std::format("{}{}", a, b);        // C++20

// substring (owning).
size_t start = 1, end = 4;
size_t len = end - start;
std::string sub1 = a.substr(start, len);           // throws if start > a.size()

// substring (zero-copy via string_view).
std::string_view sv(a);
std::string_view sub2 = sv.substr(start, len);     // no allocation, but no bounds-safety check

// find index of start of next occurence of substring in s[start:].
if (size_t pos = s.find(pattern, start); pos != std::string::npos) {
    ...
} else {
    ...
}

// join a vector<string> with a delimiter.
std::vector<std::string> words = {"one","two","three"};
std::ostringstream oss;
for (size_t i = 0; i < words.size(); ++i) {
    if (i > 0) oss << ',';
    oss << words[i];
}
std::string joined = oss.str();

// split string and map to ints.
std::string numbers = "1,2,3";
std::stringstream ss(numbers);
std::string token;
std::vector<int> nums;
while (std::getline(ss, token, ',')) {
    nums.push_back(std::stoi(token));
}

// iteration over characters.
for (char ch : s) {
    ...
}

// iteration over characters, if indices are needed.
for (size_t i = 0; i < s.size(); ++i) {
    char ch = s[i];
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

Cpp:
```cpp
std::unordered_set<int> s;
auto [it, insert_happened] = s.insert(elem);
int ret = s.erase(elem);           // returns 1 if removed, 0 if not found.
bool contains = (s.find(elem) != s.end());
bool contains = s.contains(elem);  // C++20
```

### Hashmap, defaultdict

Python:
```py
d = dict()
d = { "k1": "v2", "k2": "v2" }

# get: will raise exception if key doesn't exist.
v = d[k]
# get or default
v = d.get(k, default_val)

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

# if d[a] doesn't exist, (a, {}) entry will be created.
for (b, c) in d[a].items():
    ...

# if d[a] doesn't exist, no new entry will be created.
for (b, c) in d.get(a, {}).items():
    ...
```

Cpp:
```cpp
// basic map
std::unordered_map<std::string, std::string> d{
    { "k1", "v1" },
    { "k2", "v2" },
};

// get (throws no exception; operator[] default-constructs if missing).
std::string v = d["k1"];        // "value"
std::string v = d["missing"];   // "" (default-constructed std::string)

// get-or-default without inserting.
std::string v;
if (auto it = d.find(k); it != d.end()) {
    v = it->second;
} else {
    v = default_val;
}

// insert / overwrite.
d[k] = v;

// remove entry.
d.erase(k);    // no-op if "key" not present.

// defaultdict-like for vectors (lazy init via operator[]).
std::unordered_map<int, std::vector<int>> dv;
dv[k].push_back(v);   // dv[k] default-constructs an empty vector, then appends v.

// defaultdict-like for counts.
std::unordered_map<int, int> dc;
dc[5] += 1;           // dc[k] default-constructs to 0, then increments.

if (auto opt = d.find(k); opt != d.end()) {
    auto v = opt->second;
    ...
} else {
    ...
}

// iterate over hashmap to hashmap.
std::unordered_map<int, std::unordered_map<int, int>> d;

// if d[a] doesn't exist, (a, {}) entry will be created.
for (auto& [b, c] : d[a]) {
    ...
}

// if d[a] doesn't exist, no new entry will be created.
if (auto it = d.find(a); it != d.end()) {
    for (auto &[b, c] : it->second) {
        ...
    }
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

# peek first or last.
first_opt = next(iter(s), None)
last_opt = next(reversed(s), None)

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

// peek first or last.
Optional<Integer> firstOpt = Optional.ofNullable(s.peekFirst());
Optional<Integer> lastOpt = Optional.ofNullable(s.peekLast());
// poll[First|Last]() also exists.

TreeMap<Integer, String> d = new TreeMap<>();
d.put(k, v);
d.remove(k);
Map.Entry<Integer, String> entry = d.ceilingEntry(k);
Integer key = d.ceilingKey(k);
```


## Common tasks

### Const correctness

<!-- TODO -->

Rust:
```rust
```

Cpp:
```cpp
```

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

// get max value in stream with comparator.
T max = Stream.of(a, b).min(comparator).get();
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

### Match statements, pattern matching

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

