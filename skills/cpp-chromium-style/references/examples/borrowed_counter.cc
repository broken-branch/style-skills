// Chromium rules: borrowed pointer parameters [chromium-cpp:40],
// snake_case inline accessors [chromium-cpp:22], braces [chromium-cpp:16].
// A nullable borrowed argument makes a missing counter an ordinary outcome.

#include <stddef.h>

#include <cassert>
#include <limits>

namespace counter_example {
namespace {

class Counter {
 public:
  explicit Counter(size_t value);
  Counter(const Counter&) = default;
  Counter& operator=(const Counter&) = default;

  size_t value() const { return value_; }
  bool TryIncrement();

 private:
  size_t value_;
};

Counter::Counter(size_t value) : value_(value) {}

bool Counter::TryIncrement() {
  if (value_ == std::numeric_limits<size_t>::max()) {
    return false;
  }
  ++value_;
  return true;
}

// The caller owns the counter and keeps it alive throughout this call.
bool RecordVisit(Counter* counter) {
  if (counter == nullptr) {
    return false;
  }
  return counter->TryIncrement();
}

}  // namespace
}  // namespace counter_example

int main() {
  counter_example::Counter counter(0);
  assert(counter_example::RecordVisit(&counter));
  assert(counter.value() == 1);
  assert(!counter_example::RecordVisit(nullptr));
  counter_example::Counter full(std::numeric_limits<size_t>::max());
  assert(!counter_example::RecordVisit(&full));
  assert(full.value() == std::numeric_limits<size_t>::max());
}
