---
name: go-style
description: "Write, edit, or review .go and go.mod using house Go style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: go
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Go style (house)

Our blend of the best Go guides, in our own words. Every rule in the full guide names its source.

Scope: hand-written Go application, service, CLI, and library code using modules and Go 1.27 language semantics; reference toolchain Go 1.27.3, checked 2026-10-30. Older modules need an explicit compatibility adaptation, especially for loop variables. [GO-RELEASES] [GO-SPEC]

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- PREFER handling every Go error; when an error cannot affect the result, such as closing a read-only file, discard it explicitly with `_ =` and a short reason comment. Why: a visible, justified discard avoids invented error handling and blanket lint suppressions. [GOLANGCI]
- MUST use MixedCaps for exported identifiers and mixedCaps for unexported identifiers, including constants; preserve initialisms such as `ID` and `HTTP`, and omit private-global underscore prefixes. Why: casing communicates visibility consistently. [GO-REVIEW] [GOOGLE-GO]
- PREFER short lowercase package names without underscores or repeated qualifiers, such as `cache.New` rather than `cache.NewCache`. Why: callers already supply the package context. [EFFECTIVE-GO] [GO-REVIEW]
- MUST avoid dot imports, including in external tests. Why: qualified names reveal where an API originates. [GOOGLE-GO]
- PREFER explicit startup functions over `init`; keep unavoidable `init` deterministic, without environment reads, I/O, or goroutines. Why: import-time work hides dependencies and lifetime. [UBER-GO]
- PREFER small interfaces defined by actual consumers and concrete return types; return an interface only for justified encapsulation or runtime implementation choice. Why: callers get useful behavior without speculative abstractions. [GO-REVIEW] [GOOGLE-GO]
- MUST use pointer receivers for mutation or noncopyable synchronization state, and avoid copying structs containing used locks. Why: copies can separate state from its synchronization. [GO-REVIEW] [GOOGLE-GO]
- MUST copy slices and maps when crossing an ownership boundary that promises isolation; copy nested mutable values when a shallow copy is insufficient. Why: assignment preserves access to shared backing state. [UBER-GO] [GO-SPEC]
- MUST represent instants with `time.Time` and elapsed intervals with `time.Duration`; use `AddDate` for calendar changes. Why: calendar units and elapsed time are different contracts. [UBER-GO]
- PREFER nil slices and `len(s) == 0` for ordinary empty collections; use non-nil empty slices when a wire contract requires `[]` instead of `null`. Why: allocation and serialization have different requirements. [GO-REVIEW] [UBER-GO]
- MUST return a final `error` result for fallible operations and literal `nil` on success; use a separate boolean for ordinary absence. Why: valid zero values must remain distinguishable from failure. [GO-REVIEW] [GOOGLE-GO]
- MUST use `errors.Is` and `errors.As` to inspect potentially wrapped errors instead of comparing messages or asserting a concrete error type directly. Why: wrapping preserves semantics through an error chain. [UBER-GO] [GOOGLE-GO]
- MUST use `%w` when exposing an underlying error for caller inspection, and document that exposed identity as part of the API. Why: wrapping creates a compatibility promise. [UBER-GO] [GOOGLE-GO]
- MUST use returned errors for ordinary failures and restrict `os.Exit` or fatal logging to `main`; a test harness may use `TestMain` for process exit. Why: library callers retain control of recovery and cleanup. [UBER-GO] [GO-TEST]
- MUST register `defer` cleanup after successful acquisition, account for close errors that affect the operation, and close each iteration's resources before an unbounded loop continues. Why: defers execute at function return, not block exit. [EFFECTIVE-GO] [GO-REVIEW]
- MUST pass the caller's `context.Context` first through request-related calls, with the testing parameter immediately after any context in test helpers; avoid context fields except when a fixed external API requires one. Why: cancellation and request lifetime must follow the call chain. [GO-REVIEW] [GOOGLE-GO]
- MUST call each derived context's cancel function when its work ends, normally with `defer cancel()` after creation. Why: cancellation releases associated resources promptly. [GO-CONTEXT]
- MUST give every goroutine an owner, a stopping condition, and a way for its owner to wait for completion. Why: abandoned or blocked work leaks resources and can outlive its state. [UBER-GO] [GO-REVIEW]
- MUST document exported Go declarations with identifier-led sentence comments and provide a package comment adjacent to one package clause. Why: Go documentation tools associate comments with declarations. [GO-REVIEW] [GOOGLE-GO]
- PREFER the standard `testing` package with explicit checks and named table cases sharing one assertion path; comparison libraries may supply diffs. Why: failures remain direct and easy to diagnose. [GOOGLE-GO] [UBER-GO]
- MUST call `t.Helper()` in reporting test helpers and call `t.Fatal` or `t.FailNow` only from the test's own goroutine. Why: diagnostics need the caller location and termination affects only the calling goroutine. [GOOGLE-GO]
- MUST give marshaled struct fields explicit format tags, including deliberate exclusions. Why: Go field renames must not silently rename wire fields. [UBER-GO]
- MUST generate keys and security tokens with `crypto/rand`, never `math/rand` or `math/rand/v2`. Why: simulation generators do not provide cryptographic unpredictability. [GO-REVIEW]
- MUST return an untyped `nil` for an absent interface or successful `error`, rather than a typed nil pointer converted to that interface. Why: an interface holding a concrete type is non-nil. [GO-FAQ]
- MUST rely on per-iteration variables for Go 1.22+ loops declared with `:=`, avoiding redundant `v := v`; explicitly protect captured preexisting variables assigned with `=`. Why: only newly declared loop variables receive independent iteration storage. [GO-SPEC] [GOLANGCI]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [context-first loader](references/examples/limit.go), [table tests and wrapped errors](references/examples/limit_test.go), [runnable usage](references/examples/example_test.go).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
