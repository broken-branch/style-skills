// Google rules: return a result [google-cpp:117], avoid exceptions
// [google-cpp:147], direct includes [google-cpp:21].
// Parse a whole nonnegative decimal count without throwing.

#include <cassert>
#include <charconv>
#include <optional>
#include <string_view>
#include <system_error>

namespace count_example {
namespace {

std::optional<int> ParseCount(std::string_view text) {
  if (text.empty()) {
    return std::nullopt;
  }
  int count = 0;
  const auto [end, error] =
      std::from_chars(text.data(), text.data() + text.size(), count);
  if (error != std::errc{} || end != text.data() + text.size() || count < 0) {
    return std::nullopt;
  }
  return count;
}

}  // namespace
}  // namespace count_example

int main() {
  assert(count_example::ParseCount("27") == 27);
  assert(count_example::ParseCount("0") == 0);
  assert(!count_example::ParseCount(""));
  assert(!count_example::ParseCount("-3"));
  assert(!count_example::ParseCount("3x"));
  assert(!count_example::ParseCount(" 3"));
  assert(!count_example::ParseCount("999999999999999999999999"));
}
