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
    return pow(x1 - x2, 2) + pow(y1 - y2, 2);
}

void solve()
{
    ll N;
    std::cin >> N;

    std::vector<ll> x(N, -1);
    std::vector<ll> y(N, -1);
    for (int i = 0; i < N; ++i)
    {
        std::cin >> x[i];
    }
    for (int i = 0; i < N; ++i)
    {
        std::cin >> y[i];
    }

    // O(N^2)
    ll res = -1;
    // Compare each unique pair.
    for (int i = 0; i < N; ++i)
    {
        // Start j from i since order of i,j doesn't matter.
        for (int j = i; j < N; ++j)
        {
            res = std::max(res, euclidean_distance(x[i], y[i], x[j], y[j]));
        }
    }

    std::cout << res << std::endl;
}

int main()
{
    // Speed up stdin.
    std::cin.tie(nullptr);
    std::cin.sync_with_stdio(false);

    solve();
}
