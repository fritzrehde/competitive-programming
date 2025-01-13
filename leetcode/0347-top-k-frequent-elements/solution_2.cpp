#include <vector>
#include <unordered_map>

class Solution
{
    void quickselect(std::vector<std::pair<int, int>> &freq_nums, int k)
    {
        // Return once the first k largest elements are in the first k slots of freq_nums.

        // Quickselect until we've found idx of k-th most frequent element.
        int l = 0, r = freq_nums.size() - 1;
        while (l < r)
        {
            // TODO: probably not best choice of pivot element
            int pivot_idx = (l + r) / 2;
            int pivot_val = freq_nums[pivot_idx].first;
            // Move pivot to end of range.
            swap(freq_nums[pivot_idx], freq_nums[r]);
            // Partition around pivot.
            int store_idx = l;
            for (int i = l; i < r; i += 1)
            {
                // "Sort" descendingly.
                if (freq_nums[i].first > pivot_val)
                {
                    // num at i belongs left of pivot.
                    swap(freq_nums[i], freq_nums[store_idx]);
                    store_idx += 1;
                }
            }
            // Put pivot right after the last left element we stored.
            swap(freq_nums[r], freq_nums[store_idx]);
            pivot_idx = store_idx;
            if (pivot_idx < (k - 1))
            {
                // Need to search right for the k-th element.
                l = pivot_idx + 1;
            }
            else if (pivot_idx > (k - 1))
            {
                // Need to search left for the k-th element.
                r = pivot_idx - 1;
            }
            else if (pivot_idx == (k - 1))
            {
                // We found the k-th most frequent number, and everything left of pivot_idx is larger so even more frequent.
                return;
            }
        }
    }

public:
    std::vector<int> topKFrequent(std::vector<int> &nums, int k)
    {
        // TC must be O(n log n) to pass

        // The key to solving this problem in O(n): the order in which we return k most frequent elements doesn't matter: in other words, it's sufficient to find the k-th most frequent element and all elements more frequent than it with quickselect.

        // Map number -> frequency
        std::unordered_map<int, int> num_to_freq;
        for (const auto &num : nums)
        {
            num_to_freq[num] += 1;
        }

        std::vector<std::pair<int, int>> freq_nums;
        for (const auto &[num, freq] : num_to_freq)
        {
            freq_nums.emplace_back(freq, num);
        }
        quickselect(freq_nums, k);

        std::vector<int> res;
        for (int i = 0; i < k; ++i)
        {
            auto &[freq, num] = freq_nums[i];
            res.emplace_back(num);
        }

        return res;
    }
};