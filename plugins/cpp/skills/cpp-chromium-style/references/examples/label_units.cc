// Chromium rules: size_t counts [chromium-cpp:32], UTF-16 [chromium-cpp:37]
// [chromium-cpp:38], braced branches [chromium-cpp:16].
// Count UTF-16 code units, deliberately not user-perceived characters.

#include <stddef.h>

#include <cassert>
#include <string>

namespace label_example {
namespace {

size_t CountSeparators(const std::u16string& label) {
  size_t count = 0;
  for (char16_t unit : label) {
    if (unit == u'\u2022') {
      ++count;
    }
  }
  return count;
}

}  // namespace
}  // namespace label_example

int main() {
  const std::u16string label = u"North \u2022 South";
  assert(label_example::CountSeparators(label) == 1);
  assert(label_example::CountSeparators(u"") == 0);
  assert(label_example::CountSeparators(u"\u2022\u2022") == 2);
  const std::u16string symbol = u"\U0001F30D";
  assert(symbol.size() == 2);
}
