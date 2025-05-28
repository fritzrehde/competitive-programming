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
```python
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
```python
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
```python
q = deque()
q.append(x)
q.appendleft(x)
last = q.pop()
first = q.popleft()
```

Cpp:
```cpp
std::deque<int> q;
q.push_back(x);
q.push_front(x);
int last = q.back(); q.pop_back();
int first = q.front(); q.pop_front();
```

### Heap

Python:
```python
# min heap
min_heap = []
heappush(min_heap, x)
x = -1 * min_heap[0]
x = heappop(min_heap)

# max heap
max_heap = []
heappush(max_heap, -x)
x = -1 * heappop(max_heap)
```

Cpp:
```cpp
// min heap
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
min_heap.push(x);
int smallest = min_heap.top(); min_heap.pop();

// max heap
using Item = std::tuple<int, std::string>;
std::priority_queue<Item, std::vector<Item>> max_heap;
max_heap.push({10, "hello"});
auto [_, largest] = max_heap.top(); max_heap.pop();
```

### BST

Python:
```python
s = SortedSet()
s.add(x)
s.remove(x)
i = s.bisect_left(x)     # idx of smallest value >= x (idx left of x where next val would be inserted)
i = s.bisect_left(x)-1   # idx of largest value < x
i = s.bisect_right(x)    # idx of smallest value > x (idx right of x where next val would be inserted)
i = s.bisect_right(x)-1  # idx of largest value <= x

# peek first or last.
first_opt = next(iter(s), None)
last_opt = next(reversed(s), None)

d = SortedDict()
d[k] = v
del d[k]
```

Cpp:
```cpp
std::set<int> s;
s.insert(x);
s.erase(x);
// NOTE: compare result of s.[lower|upper]_bound(x) with s.begin() to ensure std::prev() returns valid iterator/is not UB.
auto it = s.lower_bound(x);             // iter to smallest value >= x
auto it = std::prev(s.lower_bound(x));  // iter to largest value < x
auto it = s.upper_bound(x);             // iter to smallest value > x
auto it = std::prev(s.upper_bound(x));  // iter to largest value <= x

// peek first or last.
std::optional<int> first_opt = !s.empty() ? std::optional<int>{ *s.begin() } : std::nullopt;
std::optional<int> last_opt = !s.empty() ? std::optional<int>{ *s.rbegin() } : std::nullopt;

std::map<int, std::string> d;
d[k] = v;
d.erase(k);
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
```python
v = [(1, "hi", 2.5), (2, "looong", 1.2), (3, "blah", 0.1)]

# 1. sort by key: asc by first, desc by len(snd), desc by third.
def key(item):
    # fst = int, snd = str, thd = float
    fst, snd, thd = item
    return fst, -len(snd), -thd

v.sort(key=key)

# 2. sort using custom comparator: compare by len(snd) only.
def cmp(a, b):
    # -1: a < b
    # 0: a == b
    # 1: a > b
    a_fst, a_snd, a_thd = a
    b_fst, b_snd, b_thd = b
    return len(b_snd) - len(a_snd)

v.sort(key=functools.cmp_to_key(cmp))
```

Cpp:
```cpp
using Item = std::tuple<int, std::string, double>;
std::vector<Item> v {
    {1, "hi", 2.5},
    {2, "looong", 1.2},
    {3, "blah", 0.1}
};

// 1. sort by key: asc by fst, desc by len(snd), desc by thd.
std::sort(v.begin(), v.end(),
    [](auto const &a, auto const &b) {
        auto &[a_fst, a_snd, a_thd] = a;
        auto &[b_fst, b_snd, b_thd] = b;
        auto a_key = std::make_tuple(a_fst, -a_snd.size(), -a_thd);
        auto b_key = std::make_tuple(b_fst, -b_snd.size(), -b_thd);
        return a_key < b_key;
    }
);
// C++20 introduces std::ranges::sort, which takes a projection lambda:
std::ranges::sort(v,
    std::less<>(),
    [](auto const &item) {
        auto &[fst, snd, thd] = item;
        return std::tuple{fst, -snd.size(), -thd};
    }
);

// 2. sort using custom comparator: compare by len(snd) only.
std::sort(v.begin(), v.end(),
    [](auto const &a, auto const &b) {
        // true:  a < b
        // false: a == b
        // false: a > b
        return std::get<1>(a).size() > std::get<1>(b).size();
    }
);
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

Cpp:
```cpp
// () -> int
auto supplier = []() { return 10; };
int supplied = supplier();  // 10

// (int) -> void
auto consumer = [](int x) { std::cout << x << std::endl; };
consumer(42);

// (const std::string&) -> std::size_t
auto function = [](const std::string &s) { return s.size(); };
std::size_t len = function("hello");

// (int) -> bool
auto predicate = [](int x) { return x % 2 == 0; };
bool is_even = predicate(17);

// (int, const std::string&) -> bool
auto bifunction = [](int x, const std::string &s) {
    return x == static_cast<int>(s.size());
};
bool match = bifunction(5, "world");
```
Notes on C++ lambdas and captures:
The capture clause `[]` controls how the lambda captures variables from the environment.

- `[]` captures nothing.
- `[=]` captures all used locals by value.
- `[&]` captures all used locals by reference.
- `[x, &y]` captures `x` by value, `y` by reference.
- `[x, &]` captures `x` by value, any other used locals by reference.
- `[&x, =]` captures `x` by reference, any other used locals by value.
- `[x, =, &]` is a compile-error because `=` and `&` can't be used in the same capture clause

Copies of variable values are made at the point where the lambda is created, not when it's used.

### Iterators/generators/streams.

Python:
```python
# iterate over anything (iterator, generator).
for e in iterable:
    pass

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

# collect from iterator to dictionary.
d = {k: k2v(k) for k in keys()}

# get max value in iterator.
max((dp[r][c] for r in range(0, m) for c in range(0, n)), default=0)
```

Cpp:
```cpp
// iterate over anything (can do so by value or by reference).
for (auto &e : iterable) {
    ...
}

// C++20 Ranges:
auto all_cells() {
    auto rows_view = std::views::iota(0, rows);
    auto cols_view = std::views::iota(0, cols);
    return rows_view
         | std::views::transform([&](int r){
                return cols_view 
                     | std::views::transform([&](int c){
                           return std::pair{r,c};
                       });
           })
         | std::views::join;
}

auto all_matching_pred(auto pred) {
    return all_cells()
         | std::views::filter(pred);
}

// C++XX Coroutines/generators:
// NOTE: Generators are not in the cpp standard yet, but should be soon.
using Cell = std::tuple<int, int>;
std::generator<Cell> all_cells() {
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            co_yield {r, c};
        }
    }
}
```

### Exceptions

All exceptions in both Python and Cpp are unchecked, meaning the caller does not know about all of the exceptions they might need to handle.

Python:
```python
def foo():
    raise Exception("error message")

try:
    foo()
except ExceptionTypeA as e:
    ...
except (ExceptionTypeA, ExceptionTypeB) as e:
    ...
except Exception as e:
    # catch-all for any other exception.
    ...
else:
    # runs only if no exception was raised.
    ...
finally:
    # always runs, whether or not an exception occurred.
    ...

# no catch -> exception propagates up the call stack.
```

Cpp:
```cpp
void foo() {
    throw std::runtime_error("error message");
}

try {
    foo();
} catch (const std::invalid_argument &e) {
    ...
} catch (const std::exception &e) {
    ...
}
// no catch -> exception propagates up the call stack.
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
```python
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

