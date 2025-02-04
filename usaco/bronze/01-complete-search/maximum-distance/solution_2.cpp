#include <iostream>
#include <algorithm>
#include <string>
#include <optional>
#include <vector>
#include <utility>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <queue>
#include <climits>
#include <cmath>
#include <bitset>
#include <cassert>

#define ll long long

ll euclidean_distance(ll x1, ll y1, ll x2, ll y2)
{
    ll dx = x1 - x2;
    ll dy = y1 - y2;
    return dx * dx + dy * dy;
}

void solve()
{
    ll N;
    std::cin >> N;

    std::vector<ll> x(N, -1);
    std::vector<ll> y(N, -1);
    for (auto &e : x)
    {
        std::cin >> e;
    }
    for (auto &e : y)
    {
        std::cin >> e;
    }

    // O(N^2)
    ll max_dist_squared = -1;
    // Compare each unique pair.
    for (int i = 0; i < N; ++i)
    {
        // Start j from i+1 since we only care about unique pairs, so order of i,j doesn't matter.
        for (int j = i + 1; j < N; ++j)
        {
            max_dist_squared = std::max(max_dist_squared, euclidean_distance(x[i], y[i], x[j], y[j]));
        }
    }

    std::cout << max_dist_squared << std::endl;
}

int main()
{
    // Speed up stdin.
    std::cin.tie(nullptr);
    std::cin.sync_with_stdio(false);

    solve();
}
