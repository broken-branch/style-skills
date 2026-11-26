// Google rules: explicit construction [google-cpp:75], declared copy pairs
// [google-cpp:81] [google-cpp:83], class member names [google-cpp:273].
// Copies have independent budgets; negative starting budgets become zero.

#include <cassert>

namespace retry_example {
namespace {

class RetryBudget {
 public:
  explicit RetryBudget(int attempts);
  RetryBudget(const RetryBudget&) = default;
  RetryBudget& operator=(const RetryBudget&) = default;

  int remaining() const { return remaining_; }
  bool TryConsume();

 private:
  int remaining_;
};

RetryBudget::RetryBudget(int attempts)
    : remaining_(attempts > 0 ? attempts : 0) {}

bool RetryBudget::TryConsume() {
  if (remaining_ == 0) {
    return false;
  }
  --remaining_;
  return true;
}

}  // namespace
}  // namespace retry_example

int main() {
  retry_example::RetryBudget budget(1);
  retry_example::RetryBudget copy = budget;
  assert(budget.TryConsume());
  assert(!budget.TryConsume());
  assert(copy.remaining() == 1);
  copy = budget;
  assert(copy.remaining() == 0);
  assert(!retry_example::RetryBudget(-1).TryConsume());
}
