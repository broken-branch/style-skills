// House rules: RAII ownership and all five special members [CPP-CORE];
// explicit close failures and borrower contracts [GOOGLE-CPP].
#ifndef EXAMPLES_INPUT_FILE_H_
#define EXAMPLES_INPUT_FILE_H_

#include <cerrno>
#include <cstdio>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <system_error>
#include <utility>

namespace examples {

// Owns a read-only C stream, released with fclose. No parent handle or
// callbacks are retained. Calls on the same object require external
// synchronization. After a move, IsOpen is false and Close is harmless;
// ReadByte throws logic_error on moved-from or closed objects.
class InputFile {
 public:
  // Borrows path only during this call; throws system_error if opening fails.
  [[nodiscard]] static InputFile Open(const std::string& path) {
    Handle file(std::fopen(path.c_str(), "rb"));
    if (!file) {
      throw std::system_error(errno, std::generic_category(), "open input");
    }
    return InputFile(std::move(file));
  }

  InputFile(const InputFile&) = delete;
  InputFile& operator=(const InputFile&) = delete;
  InputFile(InputFile&&) noexcept = default;
  InputFile& operator=(InputFile&&) noexcept = default;
  ~InputFile() = default;

  [[nodiscard]] bool IsOpen() const noexcept { return file_ != nullptr; }

  // Returns absence at EOF; throws system_error for I/O errors or logic_error
  // if closed. An I/O failure may have advanced the stream position.
  [[nodiscard]] std::optional<unsigned char> ReadByte() {
    if (!file_) {
      throw std::logic_error("read from closed input");
    }
    const int value = std::fgetc(file_.get());
    if (value != EOF) {
      return static_cast<unsigned char>(value);
    }
    if (std::ferror(file_.get()) != 0) {
      throw std::system_error(errno, std::generic_category(), "read input");
    }
    return std::nullopt;
  }

  // Releases ownership even if fclose fails; throws system_error on failure.
  // Calling Close again is harmless. Use it when close diagnostics matter.
  void Close() {
    if (file_ && std::fclose(file_.release()) != 0) {
      throw std::system_error(errno, std::generic_category(), "close input");
    }
  }

 private:
  struct FileCloser {
    // unique_ptr calls this only for non-null handles. Read-only streams have
    // no buffered output to commit; destructor/move cleanup cannot report
    // close errors. Call Close explicitly if those errors need handling.
    void operator()(std::FILE* file) const noexcept { (void)std::fclose(file); }
  };
  using Handle = std::unique_ptr<std::FILE, FileCloser>;

  explicit InputFile(Handle file) noexcept : file_(std::move(file)) {}

  Handle file_;
};

}  // namespace examples

#endif  // EXAMPLES_INPUT_FILE_H_
