# C++ style guide

Scope: C++20 applications and libraries, including foreign-library adapters, with exceptions and RTTI enabled in project-controlled targets. Upstream code retains its own style, configs, and build flags.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | clang-format 23.1.3 | [`.clang-format`](config/.clang-format) | `clang-format --dry-run --Werror <owned .cc and .h files>` |
| Linter | clang-tidy 23.1.3; explicit checks below | [`.clang-tidy`](config/.clang-tidy) | `clang-tidy -p <build-dir> <owned .cc files>` |
| Build / type checks | clang++ 23.1.3, C++20 | Consuming target's build files and warning policy below | Repository's declared build command (for CMake: `cmake --build <build-dir>`) |
| Tests | Consuming repository's pinned test runner | Target's test configuration | Repository's declared test command (for CTest: `ctest --test-dir <build-dir> --output-on-failure`) |

Mechanical formatting: the formatter handles this. Commands above run after copying the configs into the owned consuming subtree; substitute actual owned files and build directories.

- MUST apply this guide and its configs only to project-controlled C++; upstream code retains its own style and build configuration. Why: upstream code has a separate compatibility contract. [GOOGLE-CPP]
- MUST target Google's C++20 baseline without C++23-only facilities; enable exceptions and RTTI in project-controlled targets as a deliberate departure from Google's restrictions. Why: the selected error and checked-cast policies require those features. [GOOGLE-CPP] [CPP-CORE]
- MUST place the configs at the root of the project-controlled subtree or pass their explicit paths, and select only owned translation units and headers as tool inputs. Why: tool configuration must cover the actual input tree, and header filters never exclude a main input file. [CLANG-FORMAT] [CLANG-TIDY]
- MUST run production clang-tidy against the target's `compile_commands.json`, using `clang-tidy --config-file=<owned-config> -p <build-dir> <owned-file.cc>`. Why: analysis needs the actual include paths, defines, and language flags. [CLANG-TIDY]
- MUST keep the exact enabled check list and verify configuration changes with `clang-tidy --config-file=<owned-config> --verify-config`. Why: other checks conflict with this guide or require a newer clang-tidy. [CLANG-TIDY]

The configs use the Google formatter preset with named overrides, and 78 explicit clang-tidy checks plus ten automatically enabled analyzer prerequisites. `WarningsAsErrors: '*'` makes emitted diagnostics fail the check; it does not enable more checks. Parent tidy configs are not inherited. The header exclusion covers path components `third_party`, `vendor`, and `generated`; custom layouts still require an owned-file input list and a matching header exclusion. These are diagnostic filters, not a parsing sandbox. [CLANG-TIDY]

- MUST build owned Clang/GCC targets with `-Wall -Wextra -Wconversion -Wsign-conversion -Werror`; use `/W4 /WX` plus reviewed conversion-warning coverage on MSVC. Why: implicit conversions and suspicious operations should fail the build before review. [OPENSSF-HARDENING] [MSVC-WARNINGS]

### Formatter coverage

Clang-format uses option names rather than linter rule IDs. `BasedOnStyle: Google` supplies mechanical layout and include sorting; `Language: Cpp` and `Standard: c++20` select parsing. Overrides are `InsertBraces`, `AllowShortIfStatementsOnASingleLine`, `AllowShortLoopsOnASingleLine`, `DerivePointerAlignment`, and `PointerAlignment`. `Standard` does not configure the compiler. Brace insertion has macro/preprocessor limitations and needs diff review. [CLANG-FORMAT]

### Lint coverage by check ID

Descriptions below identify detectable cases, not proofs of whole-program safety. Each enabled ID appears here; grouped rows describe closely related diagnostics. [CLANG-TIDY]

| Enabled check IDs | What the config catches |
| --- | --- |
| `clang-analyzer-core.CallAndMessage` | Invalid callable targets or undefined call arguments. |
| `clang-analyzer-core.DivideZero` | Feasible division by zero. |
| `clang-analyzer-core.NonNullParamChecker`, `clang-analyzer-core.NullDereference` | Null arguments to nonnull contracts and null dereferences. |
| `clang-analyzer-core.StackAddressEscape` | Escaping pointers to dead stack storage. |
| `clang-analyzer-core.UndefinedBinaryOperatorResult` | Operations involving undefined values. |
| `clang-analyzer-core.uninitialized.ArraySubscript`, `clang-analyzer-core.uninitialized.Assign`, `clang-analyzer-core.uninitialized.Branch`, `clang-analyzer-core.uninitialized.UndefReturn` | Uninitialized indices, assignments, conditions, and returned values. |
| `clang-analyzer-cplusplus.InnerPointer` | Uses of invalidated pointers into supported containers. |
| `clang-analyzer-cplusplus.NewDelete`, `clang-analyzer-cplusplus.NewDeleteLeaks` | Modeled use-after-delete, double deletion, and allocation leaks. |
| `clang-analyzer-cplusplus.PureVirtualCall` | Pure virtual calls during construction/destruction. |
| `clang-analyzer-unix.Malloc`, `clang-analyzer-unix.MismatchedDeallocator` | Modeled C allocation leaks, invalid frees, and allocator/deallocator mismatches. |
| `bugprone-assert-side-effect` | Side effects that disappear when assertions are disabled. |
| `bugprone-dangling-handle`, `bugprone-stringview-nullptr`, `bugprone-suspicious-stringview-data-usage` | Recognized dangling views, null string views, and use of view data as a C string. |
| `bugprone-exception-escape`, `bugprone-std-exception-baseclass` | Detectable exception escape from nonthrowing functions and exceptions outside the `std::exception` hierarchy. |
| `bugprone-implicit-widening-of-multiplication-result`, `bugprone-narrowing-conversions` | Widening after a multiplication has already overflowed and implicit narrowing. |
| `bugprone-move-forwarding-reference` | `std::move` applied to forwarding references. |
| `bugprone-not-null-terminated-result` | Recognized C-string operations that omit terminator space or termination. |
| `bugprone-sizeof-container`, `bugprone-sizeof-expression` | Mistaking object/pointer storage size for element counts or data size. |
| `bugprone-spuriously-wake-up-functions` | Recognized waits without a predicate or rechecking loop. |
| `bugprone-unchecked-optional-access` | Flow-sensitive unchecked access to supported optional types. |
| `bugprone-undefined-memory-manipulation` | Byte operations on objects whose C++ semantics make them invalid. |
| `bugprone-unused-raii` | Unnamed resource owners destroyed at the end of the statement. |
| `bugprone-unused-return-value` | Discarded values for the check's default recognized functions and status return types; arbitrary custom status APIs still need review or `[[nodiscard]]`. |
| `bugprone-use-after-move` | Recognized use after a value has been moved from. |
| `cppcoreguidelines-avoid-capturing-lambda-coroutines`, `cppcoreguidelines-avoid-reference-coroutine-parameters`, `cppcoreguidelines-no-suspend-with-lock` | Capturing coroutine lambdas, borrowed coroutine parameters, and suspension while a recognized lock is held. |
| `cppcoreguidelines-init-variables`, `cppcoreguidelines-pro-type-member-init`, `modernize-use-default-member-init` | Missing scalar/member initialization and repeated fixed member defaults. |
| `cppcoreguidelines-misleading-capture-default-by-value` | Implicit capture of `this` under a value-capture default. |
| `cppcoreguidelines-no-malloc` | Direct `malloc`, `calloc`, `realloc`, and `free` use. |
| `cppcoreguidelines-pro-type-const-cast`, `cppcoreguidelines-pro-type-reinterpret-cast`, `cppcoreguidelines-pro-type-static-cast-downcast` | All `const_cast` expressions (`StrictMode: true`), reinterpret casts, and static downcasts. |
| `cppcoreguidelines-slicing`, `cppcoreguidelines-virtual-class-destructor` | Sliced derived objects and unsuitable polymorphic base destructors. |
| `cppcoreguidelines-special-member-functions` | Missing members from the five-operation set after a customization; all four `Allow…` relaxations are false. |
| `cppcoreguidelines-use-enum-class` | Named unscoped enums; anonymous enums still need review. |
| `google-build-using-namespace`, `google-global-names-in-headers` | Namespace-wide imports and supported global using declarations in headers. |
| `google-default-arguments` | Default arguments on virtual functions. |
| `misc-anonymous-namespace-in-header`, `misc-definitions-in-headers` | Header-local anonymous namespaces and non-inline definitions that risk ODR violations. |
| `misc-include-cleaner` | Missing direct provider includes and unused includes in the main file; included headers need separate review/compilation. |
| `misc-throw-by-value-catch-by-reference` | Recognized pointer throws, non-temporary thrown objects, and catches by value; const qualification remains review work. |
| `misc-use-anonymous-namespace` | Eligible file-scope static entities that can use an anonymous namespace. |
| `modernize-avoid-c-arrays` | Raw arrays, except string arrays allowed by `AllowStringArrays: true`. |
| `modernize-avoid-c-style-cast` | Replaceable C-style casts. |
| `modernize-avoid-setjmp-longjmp`, `modernize-avoid-variadic-functions` | Nonlocal jumps and definitions of C variadic functions. |
| `modernize-make-shared`, `modernize-make-unique` | Eligible explicit allocation expressions inside smart-pointer construction. |
| `modernize-use-equals-default`, `modernize-use-equals-delete` | Hand-written default behavior and old private-declaration noncopyability patterns. |
| `modernize-use-nullptr`, `modernize-use-override`, `modernize-use-using` | Null pointer constants, missing override markers, and legacy typedefs. |
| `performance-for-range-copy`, `performance-unnecessary-copy-initialization` | Avoidable expensive loop/local copies. |
| `performance-move-const-arg`, `performance-move-constructor-init`, `performance-no-automatic-move` | Ineffective/elision-blocking moves, copying inside move construction, and local const that prevents a return move. |
| `performance-noexcept-move-constructor` | Move operations lacking a nonthrowing declaration; correctness of that promise still needs review. |
| `portability-avoid-pragma-once` | Use of `#pragma once`; guard uniqueness and correct project path remain manual. |
| `readability-braces-around-statements` | Control bodies missed by formatter insertion; `ShortStatementLines: 0` removes the short-body exception. |
| `readability-identifier-naming` | Configured category casing and prefixes/suffixes; uppercase `_H_` guard names are exempt from the general macro pattern. |
| `misc-explicit-constructor` | Implicit single-argument constructors/conversion operators, subject to the check's standard exceptions. |

The following prerequisites also appear in the installed 23.1.3 `--list-checks` output. Their modeling descriptions were checked with `clang -cc1 -analyzer-checker-help-developer`; models support analysis rather than add style restrictions. [CLANG-TIDY]

| Automatically enabled IDs | Diagnostic or modeling purpose |
| --- | --- |
| `clang-analyzer-core.BitwiseShift` | Invalid shift counts. |
| `clang-analyzer-core.NullPointerArithm` | Invalid arithmetic involving null pointers. |
| `clang-analyzer-core.VLASize` | Invalid variable-length array sizes; this is not permission to use C++ compiler extensions. |
| `clang-analyzer-core.uninitialized.CapturedBlockVariable`, `clang-analyzer-core.uninitialized.NewArraySize` | Undefined captured block values or array allocation counts. |
| `clang-analyzer-core.DynamicTypePropagation`, `clang-analyzer-core.NonnilStringConstants` | Dynamic type propagation and nonnull constant-string modeling. |
| `clang-analyzer-core.builtin.AssumeModeling`, `clang-analyzer-core.builtin.BuiltinFunctions`, `clang-analyzer-core.builtin.NoReturnFunctions` | Models for assume constructs, builtins, and nonreturning calls. |

Naming options cover types/concepts/type parameters, functions/methods, variables/parameters/namespaces, fields, constants/enumerators/value parameters, and macros. `GetConfigPerFile: false` keeps naming tied to this config. Uppercase header-guard shapes have a macro regex exemption; standard-library function/method/type-alias names have regex exemptions, including hidden-friend `swap`, insertion hooks `push_back`/`emplace_back`, and tuple-like `get`. Static members of classes and structs share one clang-tidy category, so their suffix distinction is review-only; guard/path agreement, other externally imposed names, and template-dependent declarations also need review. [CLANG-TIDY]

### Review-only coverage

Lifetime validity across translation units, actual exclusive/shared ownership, foreign exception containment, checked arithmetic/bounds, UTF encodings, `thread_local` destruction, concept semantics, filename conventions, notices, public API contracts, and most concurrency design are review obligations. The checks detect examples of these problems, not every violation. No check is claimed to prove memory safety. [CPP-CORE] [CLANG-TIDY]

The shipped checks deliberately omit `misc-const-correctness` to avoid blanket local-const rewrites, and omit whole-family globs. In particular, Fuchsia bans, trailing-return rewrites, macro-to-enum conversion, enum-size shrinking, and format/print migrations are not enabled. The final section records those choices. [CLANG-TIDY]

## Naming

- MUST use PascalCase for owned types, concepts, ordinary functions, and methods, including accessors; preserve external-interface and standard-library protocol names such as `begin`, `end`, `size`, and `iterator`. Why: declarations have predictable spelling. [GOOGLE-CPP]
- MUST use snake_case for namespaces, parameters, and ordinary variables; suffix private class fields and nonconstant static class fields with `_`, but not public struct fields or struct statics. Why: member state is recognizable at use sites. [GOOGLE-CPP]
- MUST use kPascalCase for enumerators, constexpr variables, static-storage constants, and value template parameters. Why: constants are distinct from mutable state. [GOOGLE-CPP]
- MUST name unavoidable macros in UPPER_SNAKE_CASE with a project prefix and use project-path guards such as `PROJECT_PATH_FILE_H_`. Why: macros share a global namespace. [GOOGLE-CPP]
- PREFER treating acronyms as words in PascalCase, such as `HttpServer` and `ReadUrl`. Why: word boundaries stay readable. [GOOGLE-CPP]

## Files and layout

- PREFER snake_case `.cc` implementations, `.h` headers, and adjacent `_test.cc` unit tests in project-controlled code. Why: related C++ files are easy to locate. [GOOGLE-CPP]
- MUST make headers self-contained, use project-path include guards, and directly include the provider of each used external declaration. Why: compilation must not depend on incidental include order. [GOOGLE-CPP] [CPP-CORE]
- PREFER direct includes over forward declarations; never hand-declare another library's types, and use owned forward declarations only for an evidenced build-time benefit. Why: declarations can drift from the definition. [GOOGLE-CPP]
- MUST keep non-inline object/function definitions out of headers, keep necessary template definitions reachable, and include an implementation's paired header first. Why: this exposes missing prerequisites and avoids one-definition-rule failures. [GOOGLE-CPP] [CPP-CORE]
- MUST place owned APIs in a project namespace, file-local `.cc` entities in anonymous namespaces, and never put anonymous namespaces or global using declarations in public headers. Why: linkage and lookup are part of a C++ API. [CPP-CORE] [GOOGLE-CPP]
- MUST avoid `using namespace` directives and additions to `std`; use qualified names or narrow implementation-local using declarations. Why: imported names change overload lookup unexpectedly. [GOOGLE-CPP]
- MUST use a foreign library's documented stable interfaces and wrap acquired handles in owners using the matching release operation. Why: internal APIs are unstable and handles have library-specific destruction contracts. [CPP-CORE]

## Types and data

- MUST manage resources with RAII owners; use `std::unique_ptr` and `std::make_unique` for exclusive heap ownership. Why: C++ destruction provides reliable cleanup on return and exception. [CPP-CORE] [GOOGLE-CPP]
- MUST treat raw pointers and references as borrowers; use references for required objects and pointers for nullable objects. Why: borrowing must not conceal ownership transfer. [CPP-CORE] [CHROMIUM-CPP]
- MUST keep storage alive for every `std::span`, `std::string_view`, iterator, and captured reference; never return a view into a local or temporary owner. Why: views do not extend C++ object lifetimes. [CPP-CORE] [CLANG-TIDY]
- PREFER `std::vector`, `std::array`, and `std::string` for owned sequences, and `std::span` or `std::string_view` for borrowed inputs. Why: these types carry ownership or extent explicitly. [CPP-CORE]
- PREFER `std::optional<T>` for ordinary absence and `std::variant` or a named struct for alternatives and multiple results. Why: callers can distinguish values without sentinel conventions or unchecked unions. [CPP-CORE] [GOOGLE-CPP]
- MUST establish an optional's engaged state before dereference and a variant's active alternative before access. Why: representation validity does not imply that the requested value is present. [CPP-CORE] [CLANG-TIDY]
- PREFER value members and automatic storage; use `std::shared_ptr` only for genuinely shared lifetime and break owner cycles with `std::weak_ptr`. Why: unnecessary allocation and reference counting obscure ownership. [CPP-CORE] [GOOGLE-CPP]
- MUST initialize every scalar and member before use; prefer the rule of zero, and declare or delete all five special members when customizing any one. Why: partial initialization and implicit special-member suppression cause lifetime bugs. [CPP-CORE]
- MUST mark ordinary single-argument constructors and conversion operators `explicit` (excluding copy/move and initializer-list constructors), and overriding methods `override` or `final`. Why: implicit conversion and accidental non-overrides are easy to miss. [GOOGLE-CPP] [CPP-CORE]
- MUST give polymorphic bases a public virtual or protected nonvirtual destructor and pass them by reference or pointer. Why: deletion and copying through a base must not destroy only a subobject or slice derived state. [CPP-CORE]
- PREFER structs for independent public data and classes with private fields for maintained invariants. Why: access control should protect meaningful state relationships. [GOOGLE-CPP] [CPP-CORE]
- PREFER named `enum class` types with implicit underlying type unless a wire format, ABI, or measured storage need fixes the representation. Why: scoped values prevent accidental integer conversions without freezing layout needlessly. [CPP-CORE]
- PREFER range iteration; when signed index arithmetic is necessary, use `std::ptrdiff_t` and `std::ssize`, checking representability and bounds before access or unsigned conversion. Why: unsigned subtraction can wrap before a bounds check. [CPP-CORE] [GOOGLE-CPP]
- MUST retain `std::size_t` at allocation/container-size interfaces, use fixed-width integers for defined external widths, and keep bit operations unsigned. Why: distinct integer roles should not be conflated with the signed-index default. [CPP-CORE] [GOOGLE-CPP]
- PREFER UTF-8 in `std::string` for application text, converting to UTF-16 or platform wide strings only at APIs that require them. Why: encoding changes belong at explicit boundaries. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER `auto` only when the initializer makes the useful type apparent; spell public function return types explicitly. Why: readers need the interface's type without chasing implementation. [GOOGLE-CPP]
- PREFER direct member initialization and fixed in-class defaults; use braces for aggregates and checked scalar construction, but parentheses for count/value constructors such as `std::vector<int>(count, value)`. Why: braces can select an initializer-list overload with different meaning. [CPP-CORE] [GOOGLE-CPP]
- PREFER `const` locals and `constexpr` compile-time values where they do not prevent an intended move; keep returned movable locals non-const when needed. Why: C++ const qualification can turn a return move into a copy. [CPP-CORE] [CLANG-TIDY]
- PREFER ordinary consumed parameters by value and then move into storage; reserve `T&&` for move operations, forwarding, or justified consuming overloads. Why: one by-value interface is easier to call and maintain. [GOOGLE-CPP]
- PREFER standard C++ library facilities over introducing Abseil equivalents in new standalone code; keep an established repository abstraction when it is required. Why: Google-specific library policy need not become a house dependency. [CPP-CORE] [GOOGLE-CPP]

## Errors

- MUST use typed exceptions for failures to fulfill C++ operation contracts, throw by value, and catch by const reference at recovery boundaries. Why: failed construction and nested calls need one consistent error path. [CPP-CORE]
- MUST derive custom exceptions from `std::exception`, normally a suitable standard subclass, and reserve exceptions for errors rather than ordinary absence or iteration. Why: callers need a catchable error hierarchy and predictable normal control flow. [CPP-CORE] [CLANG-TIDY]
- MUST finish construction with a valid object or throw; a factory may return an error without exposing a partially initialized object, but public `Init()` phases are not the default. Why: every usable instance must satisfy its invariant. [CPP-CORE] [GOOGLE-CPP]
- MUST contain exceptions inside C callback adapters and translate them to the boundary's documented error result; never unwind through foreign frames that do not support the exception contract. Why: foreign callers may not support C++ unwinding. [CPP-CORE]
- MUST keep destructors nonthrowing and declare `noexcept` only when the operation truly cannot let an exception escape; provide an explicit fallible close/commit operation when cleanup can fail. Why: throwing during unwinding terminates the process. [CPP-CORE]
- MUST give project code built in an exception-disabled target an explicit status/result API and factory-based construction, preserving RAII; use virtual dispatch or an explicit, validated type tag in RTTI-disabled targets instead of `dynamic_cast`, and never use `setjmp`/`longjmp` for C++ recovery. Why: disabled unwinding still requires valid objects and reliable destruction. [CPP-CORE]
- PREFER `[[nodiscard]]` on fallible status/result APIs and factories whose result must be consumed. Why: the compiler can detect accidental omission at call sites. [CLANG-TIDY]

## Comments and docs

- MUST document borrowed-result lifetimes, pointer nullability, iterator invalidation, exception guarantees, and synchronization requirements on C++ API declarations. Why: types alone do not encode those usage contracts. [GOOGLE-CPP] [CPP-CORE]
- MUST describe a foreign-handle wrapper's matching release operation, required parent-handle lifetime, and any callback ownership or thread restrictions. Why: a C interface does not carry C++ lifetime semantics. [CPP-CORE]
- MUST preserve existing legal notices and use the consuming repository's own notice template for new files, never copying another project's attribution into new code. Why: project-specific notices do not transfer with style advice. [GOOGLE-CPP] [CHROMIUM-CPP]

## Testing

- MUST exercise C++ lifetime and error boundaries affected by a change: constructor failure, cleanup on exceptions, move behavior, and empty/out-of-range access where relevant. Why: happy-path tests do not expose invalid ownership or partial construction. [CPP-CORE]
- PREFER running ownership and parser tests with AddressSanitizer and UndefinedBehaviorSanitizer, and concurrent tests separately with ThreadSanitizer where supported. Why: dynamic tools detect C++ defects that ordinary assertions miss. [CPP-CORE]
- MUST keep side effects out of `assert` and test release behavior when `NDEBUG` changes assertion execution. Why: assertions may disappear from a compiled program. [CLANG-TIDY]
- PREFER compiling each public header in an otherwise empty translation unit. Why: a standalone compile reveals accidental transitive prerequisites. [GOOGLE-CPP]
- MUST verify foreign-library adapters with integration tests for lifetime and error translation; changes to generated output need representative golden-file comparisons. Why: a C++ unit test alone cannot establish integration behavior or generated output. [CPP-CORE]

## Performance

- MUST return named local values without `std::move` and avoid reading moved-from values until reinitialized unless the operation's contract permits it. Why: forced moves block copy elision and moved-from state is limited. [CPP-CORE] [CLANG-TIDY]
- PREFER passing inexpensive inputs by value and expensive read-only inputs by const reference or view, and avoid copying expensive range elements. Why: C++ value syntax may hide allocation and copy costs. [CPP-CORE] [CLANG-TIDY]
- PREFER nonthrowing move operations when their members permit it, and declare that contract with `noexcept`. Why: standard containers may copy instead when moving can throw. [CPP-CORE] [CLANG-TIDY]

## Security

- PREFER standard-library hardening in all owned builds: `_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST` for [libc++](https://libcxx.llvm.org/Hardening.html), or `_GLIBCXX_ASSERTIONS` for [libstdc++](https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_macros.html). Why: library precondition checks catch some invalid accesses in release builds, while explicit bounds validation remains necessary. [LIBCXX-HARDENING] [LIBSTDCXX-MACROS]

- MUST use named C++ casts for necessary conversions; prohibit `reinterpret_cast`, `const_cast`, and unchecked base-to-derived `static_cast` in ordinary code. Why: explicit syntax alone cannot establish object type or lifetime safety. [CPP-CORE]
- PREFER virtual dispatch to hierarchy inspection; when a downcast is unavoidable in an RTTI-enabled target, use `dynamic_cast` with its null or exception failure handled; use virtual dispatch or a validated explicit type tag when RTTI is disabled. Why: the conversion must validate the dynamic type. [CPP-CORE]
- MUST isolate unavoidable foreign-layout or legacy const-incorrect API adaptation in a small reviewed wrapper, with a check-specific exception and evidence for lifetime, alignment, aliasing, and mutability. Why: a low-level escape must not become normal application practice. [CPP-CORE]
- MUST check lengths and multiplication before allocation or byte access, use range-checked access or an established index bound, and never assume C++20 `std::span::operator[]` checks bounds. Why: sequence extent does not itself prevent out-of-bounds access or overflow. [CPP-CORE]
- MUST pass a null-terminated owner to APIs that require a C string; do not pass arbitrary `std::string_view::data()` as one. Why: a view can end before its backing storage's terminator. [CPP-CORE] [CLANG-TIDY]
- MUST use object construction/assignment for nontrivial types; use `std::bit_cast` only for valid same-size trivially copyable value representations, never as a pointer-safety workaround. Why: byte operations do not establish C++ object lifetimes or pointer validity. [CPP-CORE] [GOOGLE-CPP]

## Language-specific pitfalls

- MUST use `nullptr`, `using` aliases, and typed parameter packs instead of null integer constants, legacy typedefs, and C variadic function definitions. Why: these C++ forms expose types to tools. [GOOGLE-CPP] [CPP-CORE]
- MUST use explicit captures in escaping lambdas and give asynchronous work ownership of the data it needs. Why: a closure may survive the scope that created it. [CPP-CORE] [GOOGLE-CPP]
- MUST use named scoped lock owners and joined thread lifetimes; prefer `std::scoped_lock` and `std::jthread`, and wait on condition-variable predicates. Why: concurrency must preserve lifetime and synchronization invariants. [CPP-CORE]
- MUST avoid reference coroutine parameters, capturing coroutine lambdas, and holding locks across suspension. Why: coroutine frames can survive their callers and resume on another execution context. [CPP-CORE]
- MUST synchronize conflicting shared accesses, avoid calling unknown callbacks under locks, and never use `volatile` as synchronization. Why: C++ data races have undefined behavior. [CPP-CORE]
- MUST use trivially destructible `thread_local` types and mark namespace/class thread locals `constinit` or, when appropriate, `constexpr`. Why: thread-exit destructor order and dynamic initialization are hazardous. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER explicit scoped owners with controlled shutdown over intentionally leaked static owners; keep global initialization constant and independent of other translation units. Why: initialization and destruction order should not determine correctness. [CPP-CORE]
- MUST omit default arguments on virtual methods. Why: call behavior must not depend on the caller's static base type. [GOOGLE-CPP]
- PREFER overloads to default arguments when either works, keeping any nonvirtual defaults independent of evaluation time. Why: call sites should have stable, unsurprising behavior. [GOOGLE-CPP]
- PREFER leading return types unless a trailing type is required or substantially clearer. Why: ordinary signatures should share one readable form. [GOOGLE-CPP]
- PREFER concepts only where they materially clarify an existing generic interface, reuse standard concepts, and keep new concepts internal. Why: constraints should improve diagnostics without expanding the public contract unnecessarily. [GOOGLE-CPP]
- MUST define new concepts around compiler-checkable operations and document/test semantic laws separately. Why: a satisfied requires-expression does not prove semantic behavior. [GOOGLE-CPP] [CPP-CORE]
- PREFER `template <typename T> requires Concept<T>` for constrained declarations over abbreviated constrained parameter syntax. Why: one constraint form is easier to recognize across simple and compound requirements. [GOOGLE-CPP]
- PREFER explicit `std::string` construction when ownership matters instead of the `s` literal suffix. Why: owning allocation is visible without a literal namespace import. [GOOGLE-CPP]
- PREFER `std::format` for new type-safe formatted strings when the target standard library supports it; preserve established formatting APIs and use C++20-compatible output. Why: C++23 `std::print` is outside this baseline and migration checks can change contracts. [CPP-CORE] [CLANG-TIDY]
- PREFER composition to implementation inheritance, allow natural operator overloads, and reserve virtual inheritance for a justified interface design. Why: optional Fuchsia restrictions are not universal C++ requirements. [GOOGLE-CPP] [CHROMIUM-CPP]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST use exceptions for contract failure in exception-enabled targets when Core favors exceptions and Google/Chromium forbid them locally; exception-disabled integration targets use explicit results and RAII factories. Why: one error strategy per build boundary preserves construction invariants; Google itself acknowledges that exception benefits can outweigh costs in new projects. [CPP-CORE] [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST complete construction or fail without exposing an invalid object when Core rejects two-phase initialization and Google permits an Init/factory fallback. Why: factories cover exception-free cases without invalid public states. [CPP-CORE] [GOOGLE-CPP]
- PREFER direct includes when Google prefers includes and Chromium prefers eligible forward declarations; allow justified declarations only for project-controlled types. Why: ownership of declarations matters more than speculative compile-time savings. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER signed `std::ptrdiff_t`/`std::ssize` for necessary index arithmetic when Core favors signed `gsl::index` and Chromium requires `size_t`; retain `size_t` at size APIs and check conversions. Why: this follows signed arithmetic without adding GSL or changing standard interfaces. [CPP-CORE] [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST use C++20 for project-controlled targets when Google's stated baseline differs from Chromium's C++23; vendored or third-party code keeps its own compiler flags and style. Why: source formatter `Standard` values cannot settle compiler compatibility. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER UTF-8 application strings when Google discourages UTF-16 and Chromium uses it widely; use UTF-16/wide strings at external API boundaries that require them. Why: external encodings do not need to spread into the internal model. [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST use the shipped formatter's `InsertBraces: true` policy when Google permits short unbraced exceptions and Chromium chooses stricter control bodies. Why: the formatter and `readability-braces-around-statements` can enforce one policy. [GOOGLE-CPP] [CHROMIUM-CPP] [CLANG-TIDY]
- PREFER `_test.cc` in project-controlled code when Google prefers it and Chromium distinguishes `_unittest.cc` from `_browsertest.cc`. Why: standalone tests do not inherit Chromium's target taxonomy. [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST use the consuming repository's notice template and preserve upstream notices when Google's usual omission of copyright lines differs from Chromium's mandatory authors/year header. Why: style is not evidence for changing attribution. [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST require trivial destruction for thread locals when Google also permits proven-safe user destruction and Chromium requires trivial destruction. Why: the narrower condition avoids destructor-order proofs. [GOOGLE-CPP] [CHROMIUM-CPP]
- MUST use standard `constinit` for mutable namespace/class thread locals when Google uses it and Chromium still names `ABSL_CONST_INIT`; `constexpr` covers eligible constants. Why: C++20 supplies the needed guarantee directly. [GOOGLE-CPP] [CHROMIUM-CPP]
- PREFER selective, usually internal concepts when Core calls for constraints on all template arguments and Google uses concepts sparingly. Why: constraints must earn their additional interface complexity. [CPP-CORE] [GOOGLE-CPP]
- MUST make newly defined concepts compiler-checkable and state semantic laws in docs/tests when Core emphasizes semantic axioms and Google rejects concepts justified mainly by unenforced promises. Why: concept satisfaction cannot certify semantics. [CPP-CORE] [GOOGLE-CPP]
- PREFER explicit `requires` constraints when Core favors abbreviated concept notation and Google favors a requires-clause. Why: the same syntax handles simple and compound constraints. [CPP-CORE] [GOOGLE-CPP]
- PREFER overloads when Core favors default arguments and Google favors overloads in doubtful cases; leave Fuchsia's absolute default-argument bans disabled. Why: useful nonvirtual constant defaults remain permitted. [CPP-CORE] [GOOGLE-CPP] [CLANG-TIDY]
- MUST omit all defaults on virtual functions when Core permits consistent defaults and Google forbids them. Why: default arguments bind statically even though virtual dispatch is dynamic. [CPP-CORE] [GOOGLE-CPP]
- PREFER by-value ordinary consuming parameters when Core favors `X&&` and Google favors values, retaining forwarding and justified move overloads. Why: one consuming interface handles lvalues and rvalues predictably. [CPP-CORE] [GOOGLE-CPP]
- MUST enable RTTI in owned targets, departing from Google's preference to avoid it outside tests; prefer virtual dispatch, then checked `dynamic_cast`, over the static/Abseil downcasts Google permits. Integration targets keep their required flags and use virtual dispatch or validated type tags when RTTI is disabled. Why: Core's checked-downcast policy needs RTTI where those casts are used. [CPP-CORE] [GOOGLE-CPP]
- MUST prohibit reinterpretation and const-removing casts in ordinary code when Core's safety profiles forbid them and Google allows careful use; reviewed foreign adapters isolate necessary exceptions. Why: general code should not depend on unverified aliasing or mutability assumptions. [CPP-CORE] [GOOGLE-CPP]
- PREFER controlled-lifetime RAII owners when Core requires resource release and Google permits deliberately never-deleted static owners. Why: shutdown can be explicit without normalizing leaks. [CPP-CORE] [GOOGLE-CPP]
- PREFER standard facilities for new standalone code when Core favors them and Google's local hierarchy favors Abseil, retaining required existing abstractions. Why: an organization-specific preference does not justify a new dependency. [CPP-CORE] [GOOGLE-CPP]
- PREFER explicit `std::string` construction when Core recommends the `s` literal and Google bans literal suffixes. Why: explicit ownership is readable without another name-lookup convention. [CPP-CORE] [GOOGLE-CPP]
- MUST use the configured Google-derived category casing when Core suggests general underscore naming and Google specifies PascalCase types/functions and kPascalCase constants; accessors also use PascalCase. Why: one configured naming policy is enforceable. [CPP-CORE] [GOOGLE-CPP]
- PREFER `.cc` implementations when Core suggests `.cpp` and Google requires `.cc`. Why: this default fits projects adopting the Google naming conventions. [CPP-CORE] [GOOGLE-CPP]
- PREFER initialization syntax that preserves constructor intent when Core generally prefers braces and Google accepts all forms with initializer-list caveats. Why: a count/value vector constructor must not silently become a two-element list. [CPP-CORE] [GOOGLE-CPP]
- PREFER const locals unless const blocks an intended return move when Core defaults to const, Google is neutral, and `performance-no-automatic-move` flags the copy cost. Why: immutability need not prevent efficient value return. [CPP-CORE] [GOOGLE-CPP] [CLANG-TIDY]
- MUST declare/delete all five special members after customizing one when Core requires the full set and Google permits fewer explicit declarations. Why: strict special-member checking makes suppression effects visible. [CPP-CORE] [GOOGLE-CPP]
- PREFER leading return types when Google limits trailing returns and optional `modernize-use-trailing-return-type` rewrites them; leave that check disabled. Why: automated rewriting should not contradict the selected signature style. [GOOGLE-CPP] [CLANG-TIDY]
- MUST use anonymous namespaces for file-local implementation entities when Core/Chromium prefer them and optional `llvm-prefer-static-over-anonymous-namespace` prefers static; enable `misc-use-anonymous-namespace` instead. Why: one linkage policy works for functions, variables, and types. [CPP-CORE] [CHROMIUM-CPP] [CLANG-TIDY]
- PREFER named scoped enums when Core favors them and optional `modernize-macro-to-enum` creates anonymous unscoped enums; leave the transform disabled. Why: a migration's intermediate form is not the target design. [CPP-CORE] [CLANG-TIDY]
- PREFER an implicit enum underlying type absent a concrete representation need when Core favors that default and optional `performance-enum-size` shrinks enums; leave that check disabled. Why: automatic storage tuning can freeze or change an ABI. [CPP-CORE] [CLANG-TIDY]
- PREFER supported `std::format` for new standalone formatting and existing APIs for existing code when Google favors Abseil and optional tidy checks migrate to std::format/std::print; leave both migration checks disabled. Why: automated migrations cannot choose dependencies, output contracts, or a C++23 baseline for us. [GOOGLE-CPP] [CPP-CORE] [CLANG-TIDY]
- PREFER natural operators and justified interface/virtual inheritance when Google/Chromium allow them and optional Fuchsia checks prohibit them; leave those checks disabled. Why: composition remains the default without importing unrelated platform bans. [GOOGLE-CPP] [CHROMIUM-CPP] [CLANG-TIDY]
