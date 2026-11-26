// House rules: invariant-preserving value types and rule of zero [CPP-CORE];
// explicit constructors and category-based naming [GOOGLE-CPP].
#ifndef EXAMPLES_PERCENTAGE_H_
#define EXAMPLES_PERCENTAGE_H_

#include <stdexcept>

namespace examples {

// An integer percentage in [0, 100]. Independent copies share no state;
// concurrent const access is safe, but assignment needs synchronization.
class Percentage {
 public:
  // Throws out_of_range for values outside [0, 100]; no invalid object escapes.
  explicit Percentage(int value) : value_(value) {
    if (value < 0 || value > kMaximum) {
      throw std::out_of_range("percentage must be between 0 and 100");
    }
  }

  [[nodiscard]] int Value() const noexcept { return value_; }

  friend bool operator==(const Percentage&, const Percentage&) = default;

 private:
  static constexpr int kMaximum = 100;
  int value_;
};

}  // namespace examples

#endif  // EXAMPLES_PERCENTAGE_H_
