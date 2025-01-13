These notes are C++ specific.

# Initialization

Aggregate initialization allows us to directly initialize the members of aggregates.

```cpp
struct Employee
{
    int id; // note: no initializer here
    int age;
    double wage;
};

Employee joe; // note: no initializer here either => access is UB

Employee joe {}; // value-initialize all members

Employee frank = { 1, 32, 60000.0 }; // copy-list initialization using braced list
Employee joe { 2, 28, 45000.0 };     // list initialization using braced list (preferred)

// Default member initializers:
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

Employee joe; // default-initialize all members
```

# Data structures

## `std::array`

Best practice: Use `std::array` for constexpr arrays, and `std::vector` for non-constexpr arrays.

Example `std::array` usage:
```cpp
// Empty initialisation: what are the values initialized with? 0?
std::array<int, 5> a;   // Members default initialized (int elements are left uninitialized)
std::array<int, 5> b{}; // Members value initialized (int elements are zero initialized) (preferred)
std::array<int, 7> a {}; // Using a literal constant

constexpr int len { 8 };
std::array<int, len> b {}; // Using a constexpr variable

// Initialize with values.
std::array<int, 6> fibonnaci = { 0, 1, 1, 2, 3, 5 }; // copy-list initialization using braced list
std::array<int, 5> prime { 2, 3, 5, 7, 11 };         // list initialization using braced list (preferred)

std::array<int, 4> a { 1, 2, 3, 4, 5 }; // compile error: too many initializers
std::array<int, 4> b { 1, 2 };          // b[2] and b[3] are value-initialized

constexpr std::array a1 { 9, 7, 5, 3, 1 }; // The type is deduced to std::array<int, 5>
constexpr std::array a2 { 9.7, 7.31 };     // The type is deduced to std::array<double, 2>
```

## `std::string`

TODO: Pass `string_view` to function to avoid copying.
TODO: `string::substr`

## Pairs

- `pair<type1, type2> p`
- `{a, b}` or `make_pair(a, b)`
- `pair.first` and `pair.second`

## Tuples

- `tuple<type1, type2, ..., typeN> t`
- `make_tuple(a, b, c, ..., d)`
- read or mutate ith element with `get<i>(t)`
- `tie(a, b, c, ..., d) = t`

# Complete Search

- Euclidean distance: `distance[(x1,y1),(x2,y2)]^2=(x2−x1)^2+(y2−y1)^2`
