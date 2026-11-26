---
name: rust-style
description: "Write, edit, or review .rs and Cargo.toml using house Rust style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: rust
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Rust style (house)

Our blend of the best Rust guides, in our own words. Every rule in the full guide names its source.

Scope: application and reusable library Rust; new crates use Rust 2024 and the validated Rust 1.99.1 toolchain, with `rust-version = "1.99"`. Existing crates retain their declared edition/MSRV until an explicit migration; this lint profile is validated only on 1.99.1. Async guidance is runtime-independent; FFI rules apply when present.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

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

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [contextual errors](references/examples/parse_count.rs), [validated newtype](references/examples/batch_size.rs), [borrowed Unicode prefix](references/examples/unicode_prefix.rs).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
