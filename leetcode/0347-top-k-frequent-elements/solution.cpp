#include <vector>
#include <unordered_map>
#include <map>
#include <bits/algorithmfwd.h>

class Solution
{
public:
    std::vector<int> topKFrequent(std::vector<int> &nums, int k)
    {
        // TC must be O(n log n)

        // Map number -> frequency
        std::map<int, int> num_to_freq;
        for (const auto &num : nums)
        {
            num_to_freq[num] += 1;
        }

        std::vector<std::tuple<int, int>> freq_num;
        for (auto &[num, freq] : num_to_freq)
        {
            freq_num.emplace_back(freq, num);
        }
        // Sort by freq descendingly.
        std::sort(freq_num.begin(), freq_num.end(), std::greater<>());

        std::vector<int> res;
        for (int i = 0; i < k; ++i)
        {
            auto &[freq, num] = freq_num[i];
            res.emplace_back(num);
        }

        return res;
    }
};