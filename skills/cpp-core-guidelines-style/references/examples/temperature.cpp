// Core Guidelines: constructor invariants [cpp-core:C.42], rule of zero
// [cpp-core:C.20], underscore naming [cpp-core:NL.10].
// Original example; rule links are in ../sources.md.

#include <cassert>
#include <exception>
#include <stdexcept>

namespace {

class temperature {
  public:
    explicit temperature(int kelvin) : kelvin_{kelvin}
    {
        if (kelvin < 0) {
            throw std::invalid_argument{"temperature below absolute zero"};
        }
    }

    int kelvin() const noexcept { return kelvin_; }

  private:
    int kelvin_;
};

} // namespace

int main()
try {
    const temperature freezing{273};
    const auto copy = freezing;
    assert(copy.kelvin() == 273);
    assert(temperature{0}.kelvin() == 0);
    bool rejected = false;
    try {
        const temperature impossible{-1};
    }
    catch (const std::invalid_argument &) {
        rejected = true;
    }
    assert(rejected);
}
catch (const std::exception &) {
    return 1;
}
