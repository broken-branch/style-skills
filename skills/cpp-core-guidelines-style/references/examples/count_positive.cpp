// Core Guidelines: borrowed sequences [cpp-core:F.24], constrained templates
// [cpp-core:T.10] [cpp-core:T.11] [cpp-core:T.13].
// Original example; the span's owner outlives this synchronous call.

#include <array>
#include <cassert>
#include <concepts>
#include <cstddef>
#include <span>

namespace {

template <std::signed_integral T>
constexpr std::size_t count_positive(std::span<const T> values) noexcept
{
    std::size_t count{0};
    for (const auto value : values) {
        if (value > 0) {
            ++count;
        }
    }
    return count;
}

} // namespace

int main()
{
    constexpr std::array values{-4, 0, 8, 1};
    static_assert(count_positive<int>(values) == 2);
    static_assert(count_positive<int>({}) == 0);
    assert(count_positive<int>(std::span{values}.subspan(2)) == 2);
}
