---
name: cpp-style
description: "Write, edit, or review .cc, .cpp, .h, and .hpp using house C++ style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: cpp
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# C++ style (house)

Our blend of the best C++ guides, in our own words. Every rule in the full guide names its source.

Scope: C++20 applications and libraries, including foreign-library adapters, with exceptions and RTTI enabled in project-controlled targets. Upstream code retains its own style, configs, and build flags.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST apply this guide and its configs only to project-controlled C++; upstream code retains its own style and build configuration. Why: upstream code has a separate compatibility contract. [GOOGLE-CPP]
- MUST target Google's C++20 baseline without C++23-only facilities; enable exceptions and RTTI in project-controlled targets as a deliberate departure from Google's restrictions. Why: the selected error and checked-cast policies require those features. [GOOGLE-CPP] [CPP-CORE]
- MUST use PascalCase for owned types, concepts, ordinary functions, and methods, including accessors; preserve external-interface and standard-library protocol names such as `begin`, `end`, `size`, and `iterator`. Why: declarations have predictable spelling. [GOOGLE-CPP]
- MUST use snake_case for namespaces, parameters, and ordinary variables; suffix private class fields and nonconstant static class fields with `_`, but not public struct fields or struct statics. Why: member state is recognizable at use sites. [GOOGLE-CPP]
- MUST use kPascalCase for enumerators, constexpr variables, static-storage constants, and value template parameters. Why: constants are distinct from mutable state. [GOOGLE-CPP]
- PREFER snake_case `.cc` implementations, `.h` headers, and adjacent `_test.cc` unit tests in project-controlled code. Why: related C++ files are easy to locate. [GOOGLE-CPP]
- MUST make headers self-contained, use project-path include guards, and directly include the provider of each used external declaration. Why: compilation must not depend on incidental include order. [GOOGLE-CPP] [CPP-CORE]
- MUST manage resources with RAII owners; use `std::unique_ptr` and `std::make_unique` for exclusive heap ownership. Why: C++ destruction provides reliable cleanup on return and exception. [CPP-CORE] [GOOGLE-CPP]
- MUST treat raw pointers and references as borrowers; use references for required objects and pointers for nullable objects. Why: borrowing must not conceal ownership transfer. [CPP-CORE] [CHROMIUM-CPP]
- MUST keep storage alive for every `std::span`, `std::string_view`, iterator, and captured reference; never return a view into a local or temporary owner. Why: views do not extend C++ object lifetimes. [CPP-CORE] [CLANG-TIDY]
- PREFER `std::vector`, `std::array`, and `std::string` for owned sequences, and `std::span` or `std::string_view` for borrowed inputs. Why: these types carry ownership or extent explicitly. [CPP-CORE]
- PREFER `std::optional<T>` for ordinary absence and `std::variant` or a named struct for alternatives and multiple results. Why: callers can distinguish values without sentinel conventions or unchecked unions. [CPP-CORE] [GOOGLE-CPP]
- MUST initialize every scalar and member before use; prefer the rule of zero, and declare or delete all five special members when customizing any one. Why: partial initialization and implicit special-member suppression cause lifetime bugs. [CPP-CORE]
- MUST mark ordinary single-argument constructors and conversion operators `explicit` (excluding copy/move and initializer-list constructors), and overriding methods `override` or `final`. Why: implicit conversion and accidental non-overrides are easy to miss. [GOOGLE-CPP] [CPP-CORE]
- MUST use typed exceptions for failures to fulfill C++ operation contracts, throw by value, and catch by const reference at recovery boundaries. Why: failed construction and nested calls need one consistent error path. [CPP-CORE]
- MUST contain exceptions inside C callback adapters and translate them to the boundary's documented error result; never unwind through foreign frames that do not support the exception contract. Why: foreign callers may not support C++ unwinding. [CPP-CORE]
- MUST use named C++ casts for necessary conversions; prohibit `reinterpret_cast`, `const_cast`, and unchecked base-to-derived `static_cast` in ordinary code. Why: explicit syntax alone cannot establish object type or lifetime safety. [CPP-CORE]
- PREFER range iteration; when signed index arithmetic is necessary, use `std::ptrdiff_t` and `std::ssize`, checking representability and bounds before access or unsigned conversion. Why: unsigned subtraction can wrap before a bounds check. [CPP-CORE] [GOOGLE-CPP]
- PREFER UTF-8 in `std::string` for application text, converting to UTF-16 or platform wide strings only at APIs that require them. Why: encoding changes belong at explicit boundaries. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER `auto` only when the initializer makes the useful type apparent; spell public function return types explicitly. Why: readers need the interface's type without chasing implementation. [GOOGLE-CPP]
- MUST use explicit captures in escaping lambdas and give asynchronous work ownership of the data it needs. Why: a closure may survive the scope that created it. [CPP-CORE] [GOOGLE-CPP]
- MUST use named scoped lock owners and joined thread lifetimes; prefer `std::scoped_lock` and `std::jthread`, and wait on condition-variable predicates. Why: concurrency must preserve lifetime and synchronization invariants. [CPP-CORE]
- MUST omit default arguments on virtual methods. Why: call behavior must not depend on the caller's static base type. [GOOGLE-CPP]
- MUST return named local values without `std::move` and avoid reading moved-from values until reinitialized unless the operation's contract permits it. Why: forced moves block copy elision and moved-from state is limited. [CPP-CORE] [CLANG-TIDY]
- PREFER standard C++ library facilities over introducing Abseil equivalents in new standalone code; keep an established repository abstraction when it is required. Why: Google-specific library policy need not become a house dependency. [CPP-CORE] [GOOGLE-CPP]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [RAII input file](references/examples/input_file.h), [ownership and failure tests](references/examples/input_file_test.cc), [validated value type](references/examples/percentage.h), [value boundary tests](references/examples/percentage_test.cc).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
