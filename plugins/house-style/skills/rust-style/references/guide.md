# Rust style guide

Scope: application and reusable library Rust; new crates use Rust 2024 and the validated Rust 1.99.1 toolchain, with `rust-version = "1.99"`. Existing crates retain their declared edition/MSRV until an explicit migration; this lint profile is validated only on 1.99.1. Async guidance is runtime-independent; FFI rules apply when present.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags). [GOOGLE-RUST] identifies the [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html), Google, CC-BY-3.0; its guidance is restated and selectively combined here, without endorsement.

## Quick rules

- PREFER `#[expect(lint_name, reason = "specific justification")]` for a necessary local Rust lint exception; use inner `#![allow(lint_name, reason = "specific justification")]` in a generated module, or `#[cfg_attr(condition, expect(lint_name, reason = "specific justification"))]` when the lint fires only under that condition. Why: unfulfilled expectations identify stale exceptions. [MS-RUST] [CLIPPY]
- MUST use `UpperCamelCase` for Rust types, traits, and variants, `snake_case` for modules, functions, fields, and bindings, and `SCREAMING_SNAKE_CASE` for constants/statics; treat acronyms as words, as in `HttpClient`. Why: standard Rust casing makes item roles recognizable. [RUST-API] [RUST-STYLE]
- PREFER `as_` for a cheap borrowed view, `to_` for conversion work or copying, and `into_` for consuming ownership; omit `get_` on ordinary field-like getters. Why: Rust method names communicate ownership and cost. [RUST-API]
- PREFER private items and fields, then `pub(super)` or `pub(crate)` where needed; use `pub(in path)` only for visibility without a shorthand equivalent. Why: Rust visibility expresses the intended API boundary. [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST name public re-exports explicitly and avoid library preludes intended for glob imports; technical platform-dispatch globs need a recorded justification. Why: exported names should change deliberately. [MS-RUST]
- MUST keep Cargo features additive and positively named, using `std` for optional standard-library support. Why: Cargo feature unification combines consumers' requests. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST use `Option<T>` for absence and `Result<T, E>` for fallible operations, rather than sentinel values. Why: Rust makes both alternatives explicit to callers. [EFFECTIVE-RUST-BOOK]
- PREFER borrowed `&str`, `&[T]`, and `&Path` inputs when ownership is unnecessary; take owned values when storing or consuming them. Why: callers should control allocation and ownership transfer. [RUST-API] [EFFECTIVE-RUST-BOOK]
- PREFER newtype structs for distinct units or identifiers and data-carrying enums for alternatives; validate invariants in constructors and `TryFrom`/`FromStr`. Why: aliases and separate flags cannot enforce Rust type distinctions. [RUST-API] [MS-RUST]
- MUST implement `From` only for infallible conversions and `TryFrom` for fallible conversions; prefer them to numeric `as` casts. Why: conversion traits expose whether input can be rejected. [RUST-API] [EFFECTIVE-RUST-BOOK]
- MUST keep `Eq`, `Ord`, and `Hash` consistent, and make `Clone` equivalent to copying for `Copy` types. Why: Rust collections and generic algorithms rely on these trait laws. [RUST-API] [EFFECTIVE-RUST-BOOK]
- MUST implement useful `Debug` for public types, with a custom redacting implementation for secret-bearing values. Why: callers need inspectable Rust values without accidental disclosure. [MS-RUST] [RUST-API]
- MUST reserve `Deref`/`DerefMut` for pointer-like behavior rather than inheritance or general field forwarding. Why: implicit dereferencing changes method lookup and coercions. [RUST-API]
- PREFER `new` for infallible construction, `try_new` for fallible construction, and `new_with_*` for alternatives; use `Foo::builder(required_inputs)` and `FooBuilder` for four or more initialization permutations (two independently optional inputs already make four; one makes two), with private builder construction. Why: names reveal failure and keep larger construction APIs discoverable. [GOOGLE-RUST] [MS-RUST]
- MUST propagate ordinary Rust failures with `?`, using `From` or contextual `map_err` as appropriate; preserve nested causes through `Error::source`. Why: callers retain typed failures and their origins. [EFFECTIVE-RUST-BOOK] [MS-RUST]
- PREFER opaque, domain-specific library error structs with private representation and classification accessors over publicly exhaustive error enums; a simple crate may name its type `Error`. Why: internal failure cases can evolve without forcing downstream matches to change. [MS-RUST]
- MUST return `Result` for expected failures and reserve panics for unrecoverable bugs, violated internal invariants, or explicitly documented panicking APIs. Why: Rust panic is not routine error transport. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST avoid production `unwrap`; use a justified `expect` describing the invariant only when failure means a bug, and permit `unwrap`/`expect` in tests where panic means test failure. Why: production panic sites need an explicit contract. [MS-RUST] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST keep `Drop` non-panicking and non-blocking; expose explicit fallible close/shutdown operations when cleanup can fail or wait. Why: destructors cannot return `Result` and may run during unwinding. [RUST-API]
- MUST use `//!` for crate/module documentation and `///` for public items, including applicable `# Errors`, `# Panics`, and `# Safety` sections. Why: rustdoc presents the caller's Rust contract at the item. [RUST-STYLE] [RUST-API]
- MUST run rustdoc tests separately from `cargo test --all-targets`. Why: the all-targets selection does not include documentation tests. [RUST-CARGO]
- MUST release synchronous lock guards and `RefCell` borrows before `.await`, and move blocking I/O or long CPU work off an async executor's worker path. Why: held guards and blocking work can stall unrelated futures. [CLIPPY] [MS-RUST]
- MUST keep ordinary Rust safe; isolate justified unsafe code behind a small sound API, using a narrow reasoned lint exception. Why: safe callers must never be able to trigger undefined behavior. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST put a preceding `SAFETY:` comment on each unsafe block or impl and state caller obligations in an unsafe API's `# Safety` section. Why: unsafe Rust transfers proof obligations to authors and callers. [MS-RUST] [CLIPPY]
- MUST distinguish UTF-8 byte offsets from Unicode scalar values and use `str::get`, `chars`, or `char_indices` according to the operation. Why: arbitrary byte slicing can split a character and panic. [EFFECTIVE-RUST-BOOK] [CLIPPY]

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | rustfmt 1.10.0-stable, bundled with Rust 1.99.1 | [rustfmt.toml](config/rustfmt.toml) | `cargo fmt --all -- --check` |
| Linter | Clippy 0.1.99, bundled with Rust 1.99.1 | [Cargo.lints.toml](config/Cargo.lints.toml), [clippy.toml](config/clippy.toml) | `cargo clippy --workspace --all-targets --locked -- -D warnings` |
| Build / type checks | rustc / Cargo 1.99.1 | Consuming `Cargo.toml` | `cargo check --workspace --all-targets --locked` |
| Tests | libtest / rustdoc from Rust 1.99.1 | Cargo target conventions | `cargo test --workspace --all-targets --locked` and `cargo test --workspace --doc --locked` |
| Dependencies / advisories | Repository-pinned cargo-audit, when installed | `Cargo.lock` | `cargo audit`; report unavailable tools or advisory data rather than claiming a clean check. |
| Feature matrix | Repository-pinned cargo-hack, when installed | Declared feature/target/MSRV matrix | `cargo hack check --feature-powerset --locked`; constrain documented invalid combinations and report unavailable tooling. |

Mechanical formatting: the formatter handles this.

The table's commands run in a consuming repository after configuration adoption. Validated on a sample crate with rustc/Cargo/Clippy 1.99.1 and rustfmt 1.10.0: formatting, Clippy with `-D warnings`, unit tests and doctests passed. The [rustup toolchain file](https://rust-lang.github.io/rustup/overrides.html#the-toolchain-file) also selects the pinned compiler for editors and plain Cargo commands. The Rust toolchain pin is independent of a library's minimum supported Rust version (MSRV).

- MUST set both parser `edition` and rustfmt `style_edition` to `2024` for new crates using this baseline. Why: direct rustfmt and Cargo formatting then agree. [RUST-EDITION]
- MUST merge the Cargo lint fragment into each package, or place it under `workspace.lints` and opt every package in with `[lints] workspace = true`; copy [rust-toolchain.toml](config/rust-toolchain.toml), the formatter file, and the Clippy file to the repository root. Why: workspace membership alone does not inherit lint policy. [RUST-CARGO]
- PREFER Clippy's default groups plus the individually selected checks in this profile over blanket `pedantic`, `cargo`, `nursery`, or `restriction` groups. Why: optional groups include noisy or conflicting policies; this is a house departure from Microsoft. [CLIPPY]
- PREFER `#[expect(lint_name, reason = "specific justification")]` for a necessary local Rust lint exception; use inner `#![allow(lint_name, reason = "specific justification")]` in a generated module, or `#[cfg_attr(condition, expect(lint_name, reason = "specific justification"))]` when the lint fires only under that condition. Why: unfulfilled expectations identify stale exceptions. [MS-RUST] [CLIPPY]
- MUST check Rust libraries on their declared MSRV and supported targets, with default features, no default features where supported, and valid feature combinations. Why: one host build does not exercise Cargo's conditional API. [EFFECTIVE-RUST-BOOK] [MS-RUST]

For workspace adoption, the root holds the fragment renamed to `[workspace.lints.rust]` and `[workspace.lints.clippy]`. Each member manifest, including a root package if present, contains this opt-in rather than its own lint entries: [RUST-CARGO]

```toml
[lints]
workspace = true
```

- PREFER `cargo audit` for dependency advisories and `cargo tree` plus `cargo +nightly udeps` for dependency-use review when the tool and a nightly toolchain are installed; report an absent nightly, unavailable tools, or missing advisory data. Why: dependency risks and unused dependencies are not covered by compilation alone. [MS-RUST] [EFFECTIVE-RUST-BOOK] [CARGO-UDEPS]

### Enforcement map

The IDs below are diagnostics, not new prose rules. `warn` diagnostics fail the table's Clippy command because it uses `-D warnings`; explicit `deny` settings also fail without that flag. Rust's other built-in diagnostics remain enabled at their toolchain defaults. Lints approximate syntax and types; they do not prove the intended behavior. [RUSTC] [CLIPPY]

| Configured rule ID / option | What it catches; remaining review |
| --- | --- |
| rustfmt `edition`, `style_edition`, `newline_style` | Stable Rust 2024 parsing/formatting and LF output; all other layout uses formatter defaults. Rustfmt supplies options, not lint IDs. |
| `nonstandard_style`: `non_camel_case_types`, `non_snake_case`, `non_upper_case_globals` | Rust identifier casing. |
| `missing_docs`, `missing_debug_implementations` | Missing public Rust docs and public `Debug` implementations; content and redaction need review. |
| `elided_lifetimes_in_paths`, `redundant_lifetimes`, `unused_lifetimes` | Hidden path lifetimes and unnecessary lifetime declarations. |
| `unsafe_code`, `unsafe_op_in_unsafe_fn` | Unsafe declarations/operations require a scoped exception; unsafe function bodies still need explicit unsafe blocks. |
| `unused_must_use`, `unfulfilled_lint_expectations` | Unhandled must-use values and obsolete `expect` attributes. |
| `clippy::all`, `clippy::correctness` | Default correctness, suspicious, style, complexity, and performance checks; inspect the expanded set with the pinned toolchain. |
| `clippy::allow_attributes`, `clippy::allow_attributes_without_reason` | Outer `allow` instead of `expect`, or a suppression lacking a reason; justification quality needs review. |
| `clippy::cast_lossless`, `clippy::cast_possible_truncation`, `clippy::cast_possible_wrap`, `clippy::cast_precision_loss`, `clippy::cast_sign_loss`, `clippy::checked_conversions`, `clippy::fallible_impl_from` | Avoidable/lossy numeric casts, hand-written conversion checks, and detected fallible `From` bodies. |
| `clippy::clone_on_ref_ptr` | Method-style shared-pointer clones; use `Arc::clone(&value)` or `Rc::clone(&value)`. |
| `clippy::dbg_macro`, `clippy::todo`, `clippy::unimplemented` | Debug macros and unfinished panic placeholders, including in tests. |
| `clippy::doc_markdown`, `clippy::missing_errors_doc`, `clippy::missing_panics_doc` | Rustdoc code markup, error sections, and statically visible panic sections; indirect panics still need review. |
| `clippy::enum_glob_use`, `clippy::wildcard_imports`, `clippy::macro_use_imports` | Glob imports and legacy macro imports; do not fully police glob re-exports or prelude design. |
| `clippy::mod_module_files`, `clippy::pub_without_shorthand` | `mod.rs` layout and longhand visibility spellings with shorthand equivalents. |
| `clippy::negative_feature_names`, `clippy::redundant_feature_names` | Negative/filler feature names; additive behavior needs build coverage and review. |
| `clippy::map_err_ignore`, `clippy::unused_result_ok` | Patterns that discard errors; cause preservation remains a contract review. |
| `clippy::should_panic_without_expect` | Panic tests without an expected-message restriction. |
| `clippy::undocumented_unsafe_blocks`, `clippy::unnecessary_safety_doc` | Missing safety comments and inappropriate `# Safety` sections on safe APIs; soundness needs review. |
| `clippy::unwrap_used` | `unwrap`/`unwrap_err` outside detected test code, including const evaluation; `expect` invariants are reviewed manually. |
| Clippy `allow-unwrap-in-tests = true`, `allow-unwrap-in-consts = false` | Test-only exception for `unwrap_used`; arbitrary test helpers/examples outside recognized test contexts are not exempt. |
| Clippy `upper-case-acronyms-aggressive = true`, `avoid-breaking-exported-api = false` | Strengthen `clippy::upper_case_acronyms` and include public APIs in applicable checks; existing public names need a compatibility decision before renaming. |

The fragment explicitly leaves these optional IDs at `allow`: `clippy::error_impl_error`, `clippy::expect_used`, `clippy::exhaustive_enums`, `clippy::exhaustive_structs`, `clippy::impl_trait_in_params`, `clippy::implicit_return`, `clippy::inline_trait_bounds`, `clippy::literal_string_with_formatting_args`, `clippy::missing_assert_message`, `clippy::missing_trait_methods`, `clippy::panic`, `clippy::pub_use`, `clippy::pub_with_shorthand`, `clippy::question_mark_used`, `clippy::self_named_module_files`, `clippy::semicolon_inside_block`, `clippy::semicolon_outside_block`, `clippy::separated_literal_suffix`, `clippy::single_char_lifetime_names`, `clippy::unseparated_literal_suffix`, and `clippy::unwrap_in_result`. Their resolutions are in the final section. An allowed lint does not grant permission to violate a prose rule. [CLIPPY]

Review-only decisions include public dependency exposure, error representation/rendering, builder design, prelude/glob-export policy, trait and `Deref` semantics, invariant panic justification, async task lifetimes/blocking, FFI ownership, and unsafe soundness. Default checks such as `clippy::ptr_arg`, `clippy::question_mark`, `clippy::await_holding_lock`, `clippy::missing_safety_doc`, `clippy::result_unit_err`, and `clippy::unused_io_amount` catch some related mistakes, not the whole contract. [RUST-API] [MS-RUST] [CLIPPY]

`clippy::all` expands to the pinned toolchain's default set; inspect it with `clippy-driver -W help` from the adopted repository. [CLIPPY]

- MUST justify `rustfmt::skip` with generated content or essential manual alignment; use the stable formatter profile and omit unsupported nightly options. Why: formatting exceptions must solve a concrete problem. [GOOGLE-RUST] [RUST-STYLE]

## Naming

- MUST use `UpperCamelCase` for Rust types, traits, and variants, `snake_case` for modules, functions, fields, and bindings, and `SCREAMING_SNAKE_CASE` for constants/statics; treat acronyms as words, as in `HttpClient`. Why: standard Rust casing makes item roles recognizable. [RUST-API] [RUST-STYLE]
- PREFER `as_` for a cheap borrowed view, `to_` for conversion work or copying, and `into_` for consuming ownership; omit `get_` on ordinary field-like getters. Why: Rust method names communicate ownership and cost. [RUST-API]
- PREFER elided lifetimes and `'_` where sufficient; name lifetimes for their borrowing roles on types and complex interfaces, allowing `'a`/`'b` for one or two local relationships and generic abstractions. Why: names should clarify which data outlives which use. [GOOGLE-RUST] [RUST-API] [RUSTC]
- PREFER `iter`, `iter_mut`, and `into_iter` for collection traversal, with `Iter`, `IterMut`, and `IntoIter` result types. Why: callers can predict the ownership mode. [RUST-API]

- PREFER role-based generic parameter names, using `T`/`U` for unconstrained types and the `Ext` suffix for extension traits. Why: names should describe the abstraction without implying extra constraints. [GOOGLE-RUST]
- PREFER `foo`/`foo_mut` for read and mutable access, `set_foo` for replacement, `take_foo` for extraction, and `replace_foo` when returning the old value; use callback accessors when a borrow or validation must stay scoped. Why: the method name exposes the access and ownership contract. [GOOGLE-RUST]

## Files and layout

- PREFER `src/lib.rs` for reusable behavior, thin `src/main.rs` or `src/bin/` entry points, and sibling member crates in a Cargo workspace. Why: library targets make behavior reusable and directly testable. [EFFECTIVE-RUST-BOOK] [MS-RUST]
- PREFER `name.rs` with `name/child.rs` over `name/mod.rs` for new modules. Why: named files are easier to distinguish in editors. [CLIPPY]
- PREFER private items and fields, then `pub(super)` or `pub(crate)` where needed; use `pub(in path)` only for visibility without a shorthand equivalent. Why: Rust visibility expresses the intended API boundary. [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST name public re-exports explicitly and avoid library preludes intended for glob imports; technical platform-dispatch globs need a recorded justification. Why: exported names should change deliberately. [MS-RUST]
- PREFER explicit imports, permitting `use super::*` in a small test module whose namespace is controlled. Why: ordinary dependencies remain visible without needless test import churn. [EFFECTIVE-RUST-BOOK] [CLIPPY]
- PREFER standard-library types or owned abstractions in public signatures; when a foreign type is necessary, have callers import its original crate unless an umbrella, technical split, or macro-support path requires a re-export. Why: foreign APIs otherwise become accidental commitments. [MS-RUST] [RUST-API]
- PREFER explicit `pub use` facades for your own items, with one canonical public path per item. Why: module organization can evolve behind a small interface. [MS-RUST] [RUST-API]
- MUST keep Cargo features additive and positively named, using `std` for optional standard-library support. Why: Cargo feature unification combines consumers' requests. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER semver-compatible Cargo dependency ranges, but exactly pin tightly coupled facade/procedural-macro companion versions. Why: ordinary updates stay possible while coupled expansion contracts stay synchronized. [EFFECTIVE-RUST-BOOK] [MS-RUST]

- PREFER leaf modules named for their main abstraction and parent modules focused on declarations and explicit re-exports. Why: readers can locate implementation without traversing organizational code. [GOOGLE-RUST]
- PREFER one module level per grouped `use`, separating deeper paths into their own statements; put narrowly used trait imports in the function that needs them. Why: import scope makes dependencies and method availability easier to inspect. [GOOGLE-RUST]
- PREFER module-qualified calls to free functions from other modules or crates and direct imports of types and traits; qualify colliding type names and allow distinctive function names to stand alone. Why: call sites need enough origin information without repetitive paths. [GOOGLE-RUST]

## Types and data

- MUST use `Option<T>` for absence and `Result<T, E>` for fallible operations, rather than sentinel values. Why: Rust makes both alternatives explicit to callers. [EFFECTIVE-RUST-BOOK]
- PREFER borrowed `&str`, `&[T]`, and `&Path` inputs when ownership is unnecessary; take owned values when storing or consuming them. Why: callers should control allocation and ownership transfer. [RUST-API] [EFFECTIVE-RUST-BOOK]
- PREFER newtype structs for distinct units or identifiers and data-carrying enums for alternatives; validate invariants in constructors and `TryFrom`/`FromStr`. Why: aliases and separate flags cannot enforce Rust type distinctions. [RUST-API] [MS-RUST]
- MUST implement `From` only for infallible conversions and `TryFrom` for fallible conversions; prefer them to numeric `as` casts. Why: conversion traits expose whether input can be rejected. [RUST-API] [EFFECTIVE-RUST-BOOK]
- MUST keep `Eq`, `Ord`, and `Hash` consistent, and make `Clone` equivalent to copying for `Copy` types. Why: Rust collections and generic algorithms rely on these trait laws. [RUST-API] [EFFECTIVE-RUST-BOOK]
- MUST implement useful `Debug` for public types, with a custom redacting implementation for secret-bearing values. Why: callers need inspectable Rust values without accidental disclosure. [MS-RUST] [RUST-API]
- PREFER `Default` alongside a meaningful argument-free `new`, with identical behavior; implement standard conversion and iteration traits when their semantics fit. Why: standard generic code should work with the type. [RUST-API]
- MUST reserve `Deref`/`DerefMut` for pointer-like behavior rather than inheritance or general field forwarding. Why: implicit dereferencing changes method lookup and coercions. [RUST-API]
- PREFER `new` for infallible construction, `try_new` for fallible construction, and `new_with_*` for alternatives; use `Foo::builder(required_inputs)` and `FooBuilder` for four or more initialization permutations (two independently optional inputs already make four; one makes two), with private builder construction. Why: names reveal failure and keep larger construction APIs discoverable. [GOOGLE-RUST] [MS-RUST]
- PREFER infallible builder setters using validated types and a `Result`-returning `build` for cross-field validation. Why: callers handle construction failure at one boundary. [MS-RUST]
- PREFER traits with few required operations and reusable default methods; override a default only when behavior or performance warrants it. Why: implementers should not duplicate derived operations. [EFFECTIVE-RUST-BOOK]

- PREFER unique ownership and borrowing before `Rc` or `Arc`; choose shared ownership or a clone when avoiding it would make the design harder to maintain, with its cost understood. Why: unnecessary sharing complicates mutation and lifetimes. [GOOGLE-RUST]
- PREFER named fields for multi-value records and enums for API choices that an unexplained Boolean would hide; retain tuples for obvious local groupings and one-field newtypes. Why: names preserve the meaning of each position and alternative. [GOOGLE-RUST]
- PREFER iterator inputs and outputs in reusable traversal APIs when consumers benefit; keep slices for indexing and `Vec` when owned storage or simpler application code is useful. Why: flexibility should pay for its API complexity. [GOOGLE-RUST]
- PREFER concrete application parameters; use `impl Into<T>` in reusable APIs only when caller convenience outweighs inference and generated-code costs. Why: a flexible library boundary need not become an application-wide abstraction. [GOOGLE-RUST]
- PREFER applicable common traits for reusable library types and demand-driven trait implementations in applications, using derives when their behavior is correct. Why: downstream reuse and known local callers justify different amounts of generality. [GOOGLE-RUST] [RUST-API]
- MUST add `Eq` only for reflexive equality and `Ord` only for a total order; partial comparison traits are sufficient otherwise. Why: trait promises must match the values the type can represent. [GOOGLE-RUST] [RUST-API]
- PREFER inherent methods for ordinary behavior; introduce traits for actual generic, opaque, dynamic, or extension interfaces, choosing generic dispatch unless runtime variation or code size warrants trait objects. Why: traits should express a boundary rather than merely divide files. [GOOGLE-RUST]
- PREFER `#[non_exhaustive]` on public enums and exposed-field structs whose shape must grow across independently maintained consumers; omit it for fixed shapes, deliberate struct-update APIs, or explicitly coordinated migrations. Why: evolution policy should match the consumer boundary. [GOOGLE-RUST]
- MUST mark a function or its result type `#[must_use]` when discarding the outcome defeats correct use, without duplicating an existing result-type annotation. Why: the compiler should catch accidentally ignored work. [GOOGLE-RUST]
- MUST pair `len` with `is_empty`, and make public `const fn` promises only when const use can remain supported; give option structs a meaningful `Default`. Why: API additions carry behavioral and compatibility expectations. [GOOGLE-RUST] [RUST-API]

## Errors

- MUST propagate ordinary Rust failures with `?`, using `From` or contextual `map_err` as appropriate; preserve nested causes through `Error::source`. Why: callers retain typed failures and their origins. [EFFECTIVE-RUST-BOOK] [MS-RUST]
- PREFER opaque, domain-specific library error structs with private representation and classification accessors over publicly exhaustive error enums; a simple crate may name its type `Error`. Why: internal failure cases can evolve without forcing downstream matches to change. [MS-RUST]
- MUST implement `std::error::Error`, `Debug`, `Display`, `Send`, and `Sync` for public library errors; use `Box<dyn Error + Send + Sync + 'static>` when type erasure is appropriate. Why: errors must integrate with Rust diagnostics and thread boundaries. [RUST-API]
- PREFER concise lowercase error `Display` messages without final punctuation, leaving cause-chain and backtrace rendering to the reporting boundary. Why: nested diagnostics compose without duplicated reports. [RUST-API]
- PREFER one contextual application error representation in binaries and their private implementation crates, while reusable libraries expose stable typed errors. Why: application reporting and library recovery have different needs. [MS-RUST]
- MUST return `Result` for expected failures and reserve panics for unrecoverable bugs, violated internal invariants, or explicitly documented panicking APIs. Why: Rust panic is not routine error transport. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST avoid production `unwrap`; use a justified `expect` describing the invariant only when failure means a bug, and permit `unwrap`/`expect` in tests where panic means test failure. Why: production panic sites need an explicit contract. [MS-RUST] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST keep `Drop` non-panicking and non-blocking; expose explicit fallible close/shutdown operations when cleanup can fail or wait. Why: destructors cannot return `Result` and may run during unwinding. [RUST-API]

- MUST keep correctness independent of `catch_unwind`; a reviewed final defensive boundary is acceptable only with unwinding enabled and a plan to discard failed work. Why: catching cannot make an unknown invariant valid again. [GOOGLE-RUST]
- MUST propagate poisoned-lock failure instead of extracting and reusing its protected contents. Why: the interrupted operation may have broken the data invariant. [GOOGLE-RUST]

## Comments and docs

- MUST use `//!` for crate/module documentation and `///` for public items, including applicable `# Errors`, `# Panics`, and `# Safety` sections. Why: rustdoc presents the caller's Rust contract at the item. [RUST-STYLE] [RUST-API]
- PREFER compiling rustdoc examples that use `?` for fallible calls, hiding only necessary scaffolding with rustdoc's `#` lines. Why: examples teach the same error model as production code. [RUST-API]
- MUST put a preceding `SAFETY:` comment on each unsafe block or impl and state caller obligations in an unsafe API's `# Safety` section. Why: unsafe Rust transfers proof obligations to authors and callers. [MS-RUST] [CLIPPY]

- PREFER examples covering the important crate workflows and direct source documentation; keep implementation notes in ordinary comments and omit explanations that merely restate obvious syntax. Why: documentation should teach the contract and useful usage. [GOOGLE-RUST]

## Testing

- PREFER public-interface tests in `tests/` and private unit tests in `#[cfg(test)] mod tests`. Why: integration tests exercise the same visibility boundary as downstream crates. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST run rustdoc tests separately from `cargo test --all-targets`. Why: the all-targets selection does not include documentation tests. [RUST-CARGO]
- PREFER assertion messages that add the failed invariant, input case, or caller context when the built-in values cannot explain it; omit messages that repeat the condition. Why: a failure should carry the information needed to investigate it. [GOOGLE-RUST]
- MUST narrow intentional panic tests with `#[should_panic(expected = "relevant message")]`. Why: an unrelated panic must not satisfy the test. [CLIPPY]
- PREFER compile-time checks for promised `Send`/`Sync` bounds, compile-fail tests for API misuse, and Miri for supported unsafe abstractions. Why: runtime assertions alone cannot validate Rust type contracts or detect all undefined behavior. [RUST-API] [MS-RUST]

## Performance

- PREFER short iterator transformations for direct data operations; use `for` for side effects instead of `for_each`, and split complicated chains into named steps or a loop. Why: readers should see the control flow without decoding nested closures. [GOOGLE-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER `Arc::clone(&value)` and `Rc::clone(&value)` for reference-counted sharing, and borrowed views instead of ownership clones that exist only to satisfy a signature. Why: shared ownership and data copying have different costs. [RUST-API] [CLIPPY]
- MUST release synchronous lock guards and `RefCell` borrows before `.await`, and move blocking I/O or long CPU work off an async executor's worker path. Why: held guards and blocking work can stall unrelated futures. [CLIPPY] [MS-RUST]
- PREFER capacity-aware construction, iterator `collect`, and reusable buffers on allocation-sensitive paths. Why: Rust containers otherwise repeatedly allocate or grow. [MS-RUST] [EFFECTIVE-RUST-BOOK]

## Security

- MUST keep ordinary Rust safe; isolate justified unsafe code behind a small sound API, using a narrow reasoned lint exception. Why: safe callers must never be able to trigger undefined behavior. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST use an explicit compatible FFI ABI and representation, document ownership/destruction, and enforce pointer validity before constructing Rust references. Why: foreign memory does not carry Rust's validity guarantees. [RUST-FFI] [EFFECTIVE-RUST-BOOK]
- MUST define an FFI unwind policy and prevent unwinding through boundaries that do not permit it; a deliberate `C-unwind` boundary needs compatible callers. Why: unwind behavior depends on ABI and panic strategy, not a blanket rule. [RUST-FFI]
- PREFER standard randomized hashing for externally influenced keys; restrict faster noncryptographic alternatives to trusted keys with an explicit threat assessment. Why: attacker-chosen collisions can make hash-table work pathological. [MS-RUST]

- MUST explain why a safe implementation cannot meet the requirement before adding unsafe code, supplying measurements when speed is the reason. Why: a safety proof alone does not justify accepting extra risk. [GOOGLE-RUST]

## Language-specific pitfalls

- MUST use `checked_*` arithmetic for fallible size/length or untrusted-input calculations; use `saturating_*`, `wrapping_*`, or `std::num::Wrapping` only when saturation or modular arithmetic is the contract. Why: [integer overflow](https://doc.rust-lang.org/book/ch03-02-data-types.html#integer-overflow) behaves differently between default debug and release builds. [RUST-BOOK]

- PREFER tail expressions and expression-valued `if`/`match` for straightforward results, using early `return` for control flow. Why: unnecessary final returns obscure normal Rust expression style. [RUST-STYLE] [CLIPPY]
- MUST distinguish UTF-8 byte offsets from Unicode scalar values and use `str::get`, `chars`, or `char_indices` according to the operation. Why: arbitrary byte slicing can split a character and panic. [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST await returned futures or deliberately drop them, and track spawned work according to the runtime's task-handle contract. Why: constructing a future alone does not make it progress. [RUST-FUTURE] [CLIPPY]
- MUST handle partial `Read::read`/`Write::write` counts or use `read_exact`/`write_all` when the contract requires the whole buffer. Why: successful I/O can transfer fewer bytes than requested. [CLIPPY]
- PREFER structured Rust logging with named fields and deferred formatting; keep templates intact and reserve direct console output for intentional CLI behavior. Why: structured events remain queryable without eager string allocation. [MS-RUST]
- MUST keep `dbg!`, `todo!`, and `unimplemented!` out of completed Rust code. Why: these macros leak debug output or leave runtime panic placeholders. [CLIPPY]
- MUST treat Effective Rust's pre-1.86 trait-upcasting limitation, library-lockfile recommendation, and blanket FFI-panic claim as historical; use stable upcasting where valid, retain a Cargo lockfile by default, and follow the current ABI unwind contract. Why: those dated restrictions no longer describe this baseline. [EFFECTIVE-RUST-BOOK] [RUST-1.86] [RUST-CARGO] [RUST-FFI]

- PREFER variable type annotations where conversions or iterator results otherwise obscure the type, and pattern matching instead of testing `Option`/`Result` then unwrapping it. Why: readers and the compiler should see the same type and variant evidence. [GOOGLE-RUST]
- PREFER naming known variants explicitly in a match on a non-exhaustive enum before its future-case wildcard; use `if let` or `let-else` when only one case matters. Why: deliberate handling stays distinct from unknown future variants. [GOOGLE-RUST]
- MUST avoid `doc(hidden)` interfaces owned by other crates and user-code execution before `main`; use unstable language or library features only with explicit project approval and a documented compatibility need. Why: hidden contracts and startup side effects are fragile, while unstable features need an agreed compatibility policy. [GOOGLE-RUST]
- PREFER `format!` or `write!` for multi-part string construction and substitutions; keep overloaded operators consistent with their familiar mathematical or logical operation. Why: ordinary syntax should keep its expected meaning. [GOOGLE-RUST]

## Where the sources disagree

- PREFER original-crate imports for exposed foreign types (Microsoft M-FOREIGN-REEXPORTS) over Effective Rust Item 24's matching-version re-export default, except for umbrella, technical-split, and macro-support needs. Why: explicit dependencies keep public ownership clear. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER opaque error structs with classification accessors (Microsoft) over the public error enums permitted by Effective Rust. Why: representation can evolve without expanding an exhaustive public match. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER concise error `Display` text (API C-GOOD-ERR) over Microsoft's combined summary, backtrace, and cause-chain rendering. Why: reporting boundaries can render diagnostics once. [RUST-API] [MS-RUST]
- PREFER the conventional simple-crate `Error` name (Microsoft) over optional `clippy::error_impl_error`. Why: the crate path supplies the missing context. [MS-RUST] [CLIPPY]
- MUST avoid library preludes intended for glob imports (Microsoft), despite Effective Rust's curated-prelude allowance. Why: explicit imports make dependencies discoverable. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- MUST use explicit public re-export lists, adopting Microsoft's narrow technical-dispatch exception over Effective Rust's broader internal glob-export allowance. Why: internal module growth must not silently grow the public API. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER deliberate `pub use` facades allowed by Microsoft, the API Guidelines, and Effective Rust over optional `clippy::pub_use`. Why: a blanket prohibition blocks useful API organization. [MS-RUST] [RUST-API] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- PREFER `FooBuilder` (Microsoft) over API C-BUILDER's optional domain-specific builder name. Why: the relationship to `Foo` stays predictable. [MS-RUST] [RUST-API]
- PREFER `Foo::builder` with private builder construction (Microsoft) over the public `DetailsBuilder::new` demonstrated by Effective Rust. Why: construction has one discoverable entry point. [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER semver-compatible dependency ranges (Effective Rust), with exact version pins for Microsoft's tightly coupled macro companions. Why: this scoped exception preserves the expansion contract without freezing unrelated dependencies. [EFFECTIVE-RUST-BOOK] [MS-RUST]
- PREFER reasoned `expect` attributes (Microsoft and Clippy) over Effective Rust's older local `allow` examples, retaining inner reasoned `#![allow(...)]` in generated modules and conditional `cfg_attr(..., expect(...))` for configuration-specific exceptions. Why: stale ordinary exceptions become visible. [MS-RUST] [CLIPPY] [EFFECTIVE-RUST-BOOK]
- PREFER useful trait default methods (Effective Rust) over globally enabling `clippy::missing_trait_methods`; delegating wrappers may opt in locally. Why: ordinary implementers should reuse correct defaults. [EFFECTIVE-RUST-BOOK] [CLIPPY]
- PREFER Rust tail expressions and enabled `clippy::needless_return` over optional `clippy::implicit_return`. Why: the official expression idiom wins over the contradictory restriction; this also settles internal lint pair 1. [RUST-STYLE] [CLIPPY]
- PREFER Google's descriptive lifetime names on types and complex interfaces over API C-CASE's short-name default; retain elision and short local/generic exceptions, leaving `clippy::single_char_lifetime_names` off and `clippy::needless_lifetimes` on. Why: naming should clarify relationships without banning concise local notation; this also settles internal lint tension 7. [GOOGLE-RUST] [RUST-API] [CLIPPY]
- PREFER ordinary inline bounds for short signatures and `where` clauses when clearer, as the Style Guide permits, over blanket `clippy::inline_trait_bounds`. Why: the signature's complexity determines the useful form. [RUST-STYLE] [CLIPPY]
- MUST retain `?` for ordinary propagation (API and Effective Rust) and keep `clippy::question_mark` enabled instead of `clippy::question_mark_used`. Why: Rust has a dedicated propagation operator; this also settles internal lint pair 2. [RUST-API] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST allow justified invariant/bug panics (Microsoft and Effective Rust) instead of adopting optional `clippy::panic` globally. Why: an unrecoverable bug is different from an expected `Result` failure. [MS-RUST] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- MUST reject production `unwrap` with `clippy::unwrap_used`, allow justified invariant `expect`, and permit test unwrapping as Effective Rust does; leave `expect_used` and `unwrap_in_result` disabled. Why: the panic's purpose matters more than its enclosing return type. [MS-RUST] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- PREFER Google's contextual assertion messages over Microsoft M-PANIC-MESSAGE's requirement for a message on every intentional production panic; follow Microsoft's test exemption and leave `clippy::missing_assert_message` off. Why: the house adds context when the condition and built-in values do not explain the failure, instead of repeating them. [GOOGLE-RUST] [MS-RUST] [CLIPPY]
- PREFER deferred structured log templates (Microsoft), leaving `clippy::literal_string_with_formatting_args` disabled. Why: braces can be intentional structured properties. [MS-RUST] [CLIPPY]
- PREFER `clippy::mod_module_files` and named module files over opposing `clippy::self_named_module_files` (internal pair 3). Why: filenames identify their modules in editor tabs. [CLIPPY]
- PREFER rustfmt's output without either `clippy::semicolon_inside_block` or `clippy::semicolon_outside_block` (internal pair 4), departing from Microsoft's latter selection. Why: one formatter owns mechanical layout. [RUST-STYLE] [CLIPPY] [MS-RUST]
- PREFER leaving both `clippy::separated_literal_suffix` and `clippy::unseparated_literal_suffix` disabled (internal pair 5). Why: enforcing opposing optional spelling restrictions adds no type-safety benefit. [CLIPPY]
- PREFER `pub(crate)`/`pub(super)` and `clippy::pub_without_shorthand` over opposing `clippy::pub_with_shorthand` (internal pair 6). Why: standard shorthand expresses the same visibility directly. [CLIPPY]

- PREFER default Clippy groups plus selected lints over Microsoft M-STATIC-VERIFICATION's blanket `pedantic` and `cargo` groups; also leave its `ambiguous_negative_literals`, `redundant_imports`, and `trivial_numeric_casts` compiler opt-ins unselected. Why: this smaller profile targets the stated house rules; these extra syntax/style restrictions need demonstrated value before adoption. [MS-RUST] [CLIPPY] [RUSTC]

- PREFER Google's `try_new` and `new_with_*` constructor names over the API Guidelines' and Microsoft's `with_*` alternatives; use Microsoft's builder threshold for four or more initialization permutations. Why: one constructor naming pattern makes creation predictable while builders manage configuration growth. [GOOGLE-RUST] [RUST-API] [MS-RUST]
- PREFER Microsoft's explicit public exports over Google's non-leaf glob-export allowance (public glob facades). Why: a new child item must not silently enlarge the public API. [GOOGLE-RUST] [MS-RUST]
- PREFER Google and Microsoft's no-new-prelude default over Effective Rust's curated-prelude option; review any dependency-prelude exception (preludes). Why: explicit names expose dependencies. [GOOGLE-RUST] [MS-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER Google's single-module groups over the nested groups accepted by the official formatter; review this shape manually (import grouping). Why: stable rustfmt does not enforce this semantic grouping. [GOOGLE-RUST] [RUST-STYLE]
- PREFER Cargo's normal `src/` layout for general crates, restricting Google's flat-file build layout to Chromium (Chromium layout). Why: the Google restriction belongs to its build system. [GOOGLE-RUST] [RUST-CARGO]
- PREFER Microsoft's runtime-aware async guidance for general Rust, retaining Google's async prohibition only when contributing to Chromium (Chromium async). Why: the ban is not a portable language restriction. [GOOGLE-RUST] [MS-RUST]
- PREFER standard Rust threads or the chosen runtime for ordinary projects, restricting Google's sequence requirement to Chromium (Chromium scheduling). Why: scheduling follows the host application architecture. [GOOGLE-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER the mutex appropriate to the runtime outside Fuchsia, retaining Google's `fuchsia_sync::Mutex` choice only inside Fuchsia (Fuchsia mutexes). Why: a platform dependency cannot be a universal default. [GOOGLE-RUST] [EFFECTIVE-RUST-BOOK] [CLIPPY]
- PREFER Google's correctness-independent defensive catch over a general reading of Microsoft's request-containment option; discard failed work and respect aborting hosts (panic catching). Why: catching does not establish restored invariants. [GOOGLE-RUST] [MS-RUST]
- PREFER Google's short pipelines and explicit side-effect loops as a readability refinement of Effective Rust's iterator emphasis (iterator style). Why: both favor the clearer expression, so long chains earn no preference. [GOOGLE-RUST] [EFFECTIVE-RUST-BOOK]
- PREFER Google's demand-driven application traits while keeping the API Guidelines' common-trait checklist for reusable libraries (application traits). Why: these prescriptions address different audiences. [GOOGLE-RUST] [RUST-API]
- PREFER the API Guidelines' eager common traits for reusable libraries when their laws hold, over Google's partial-first default; use only partial comparison traits when total laws fail. Why: lawful common traits improve interoperability without promising invalid ordering or equality. [RUST-API] [GOOGLE-RUST]
- PREFER Google's contextual panic, `expect`, non-exhaustive and generic-input decisions over blanket Clippy restrictions; leave `panic`, `expect_used`, `exhaustive_enums`, `exhaustive_structs`, and `impl_trait_in_params` off (restriction lints). Why: documented exceptions need review rather than unconditional bans. [GOOGLE-RUST] [CLIPPY]
- PREFER Google's stable-compatible formatter settings, omitting its nightly-only options from this stable toolchain (formatter options). Why: unknown or unstable settings must not produce a misleading configuration. [GOOGLE-RUST] [RUST-STYLE]
