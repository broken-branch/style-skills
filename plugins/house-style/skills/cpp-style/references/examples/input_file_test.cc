// House rules: ownership, move and error-boundary tests [CPP-CORE];
// direct includes and typed recovery at the executable boundary [GOOGLE-CPP].
// Run with a file containing one byte 'A', followed by a nonexistent path.
#include "input_file.h"

#include <cstdlib>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <system_error>
#include <utility>

namespace {

void Require(bool condition, const char* message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    Require(argc == 3, "expected readable and nonexistent file paths");
    auto original = examples::InputFile::Open(argv[1]);
    auto moved = std::move(original);
    // IsOpen explicitly supports moved-from objects (unique_ptr becomes null).
    // NOLINTNEXTLINE(bugprone-use-after-move)
    Require(!original.IsOpen(), "move left the source owning a stream");
    original.Close();
    Require(moved.ReadByte() == 'A', "first byte differs");
    Require(!moved.ReadByte().has_value(), "expected EOF");

    auto replacement = examples::InputFile::Open(argv[1]);
    moved = std::move(replacement);
    // Verify the same documented empty state after move assignment.
    // NOLINTNEXTLINE(bugprone-use-after-move)
    Require(!replacement.IsOpen(), "move assignment retained ownership");
    Require(moved.ReadByte() == 'A', "move assignment lost stream position");
    moved.Close();
    moved.Close();
    Require(!moved.IsOpen(), "close retained ownership");

    bool rejected_closed = false;
    try {
      (void)moved.ReadByte();
    } catch (const std::logic_error&) {
      rejected_closed = true;
    }
    Require(rejected_closed, "reading a closed stream should fail");

    bool rejected_missing = false;
    try {
      const auto missing = examples::InputFile::Open(argv[2]);
    } catch (const std::system_error&) {
      rejected_missing = true;
    }
    Require(rejected_missing, "opening a nonexistent file should fail");
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
