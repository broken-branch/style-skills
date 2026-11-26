// House rules: constructor boundaries and release-build tests [CPP-CORE];
// direct includes and exception recovery [GOOGLE-CPP].
#include "percentage.h"

#include <array>
#include <cstdlib>
#include <exception>
#include <iostream>
#include <limits>
#include <stdexcept>

namespace {

void Require(bool condition, const char* message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

}  // namespace

int main() {
  try {
    for (const int value : std::array{0, 25, 100}) {
      const examples::Percentage percentage(value);
      const auto copy = percentage;
      Require(percentage.Value() == value, "constructor changed the value");
      Require(copy == percentage, "copy changed the value");
    }

    for (const int value : std::array{-1, 101, std::numeric_limits<int>::min(),
                                      std::numeric_limits<int>::max()}) {
      bool rejected = false;
      try {
        const examples::Percentage invalid(value);
      } catch (const std::out_of_range&) {
        rejected = true;
      }
      Require(rejected, "out-of-range percentage was accepted");
    }
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
