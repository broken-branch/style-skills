# Go style guide

Scope: hand-written Go application, service, CLI, and library code using modules and Go 1.27 language semantics; reference toolchain Go 1.27.3, checked 2026-10-30. Older modules need an explicit compatibility adaptation, especially for loop variables. [GO-RELEASES] [GO-SPEC]
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

The distributable [`.golangci.yml`](config/.golangci.yml) is copied to a consuming module's root. Commands below run there. A binary built with Go 1.27 or newer is needed to analyze this baseline. The runner pins its bundled analyzer versions, including revive 1.17.1, Staticcheck 0.8.2, gosec 2.29.0, and `golang.org/x/tools` 0.52.0. [GOLANGCI]

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | `gofmt` with Go 1.27.3; `goimports` from x/tools 0.52.0, bundled in golangci-lint 2.15.0 | `.golangci.yml`, formatter selection only; neither needs standalone configuration | `golangci-lint fmt --diff --config .golangci.yml .` |
| Linter | golangci-lint 2.15.0, explicit diagnostic selection | `.golangci.yml` | `golangci-lint config verify --config .golangci.yml` then `golangci-lint run --config .golangci.yml ./...` |
| Build / type checks | Go 1.27.3 | `go.mod` (`go 1.27.0`; reference toolchain `go1.27.3`) | `go build ./...` |
| Tests | Go 1.27.3 `testing` and race detector | `*_test.go` and `go.mod` | `go test ./...` and, on a supported target, `go test -race ./...` |
| Vulnerabilities | Repository-pinned `golang.org/x/vuln/cmd/govulncheck` | Module dependencies | `govulncheck ./...` in CI and before dependency additions/upgrades; report unavailable tooling or advisory data. |
| Modernizers | `go fix`, bundled with Go 1.27.3 | `go.mod` | `go fix -diff ./...`; review and apply applicable fixes to new code. |

Mechanical formatting: the formatter handles this.

- MUST format Go source with `gofmt` and maintain imports with `goimports`. Why: standard Go tools make mechanical style predictable. [GO-REVIEW]
- MUST use the v2 configuration's explicit linter and formatter selections instead of enabling every available checker. Why: available checks include policies that conflict with this guide. [GOLANGCI]
- PREFER refactoring complex expressions rather than imposing a numeric source-width limit. Why: semantic structure matters more than a column count. [GOOGLE-GO] [GO-REVIEW]
- MUST name the checker and explain the concrete reason in any necessary `//nolint:checker // reason` directive. Why: Go lint exceptions need a searchable scope and rationale. [GOLANGCI]

- MUST run `go fix -diff ./...` on new Go code and apply applicable modernizer fixes before rerunning lint and tests. Why: [Go 1.26 modernizers](https://go.dev/doc/go1.26#tools) catch obsolete idioms that style checks miss. [GO-FIX]
- MUST run `govulncheck ./...` in CI and before adding or upgrading dependencies, reporting unavailable scans explicitly. Why: the [official vulnerability checker](https://go.dev/doc/security/vuln/) identifies vulnerable dependencies and reachable affected calls. [GO-VULN]

### Configured diagnostic IDs

Each ID below is explicitly selected. Tables describe detection, not proof of correctness; some analyzers depend on reachable code or recognize only particular APIs. `typecheck` is the runner's unavoidable loading prerequisite. Tests are analyzed, issue counts are unlimited, and no broad exclusion presets or test exemptions are configured. Files matching Go's strict generated-file marker are excluded from style diagnostics and formatting, but still participate in package loading. [GOLANGCI]

| ID | What the configuration checks |
| --- | --- |
| `gofmt`, `goimports` | Canonical formatting and import maintenance; exact removal of user-created extra import partitions still needs review. |
| `typecheck` | Source parsing and type correctness before analyzers run. |
| `asasalint` | Missing `...` when forwarding variadic `[]any` arguments. |
| `bidichk` | Dangerous bidirectional control characters in source. |
| `bodyclose` | Recognized HTTP response bodies lacking closure. |
| `containedctx` | Context stored in a struct; fixed external-signature exceptions need a narrow explanation. |
| `contextcheck`, `noctx` | Lost context ancestry and recognized context-free request operations. |
| `copyloopvar` | Redundant loop-variable capture copies under modern Go semantics. |
| `durationcheck` | Accidental duration-by-duration multiplication. |
| `errcheck` | Unchecked errors and type assertions; built-in function exemptions remain enabled and explicit blank-assigned errors are permitted with review. |
| `errname` | Error sentinel prefixes and error type suffixes. |
| `errorlint` (`comparison`, `asserts`) | Non-chain-aware error equality, assertions, and type switches; the `errorf` check is off so intentional identity hiding remains possible. |
| `ineffassign`, `unused` | Ineffective assignments and unused declarations. |
| `makezero` | An initial slice length accidentally retained before appends. |
| `musttag` | Missing serialization tags at recognized marshaling calls. |
| `nilerr`, `nilnesserr` | Nil success returned after a detected error, including known-nil alternate errors. |
| `nolintlint` | Unused directives, missing checker names, or missing explanations. |
| `predeclared` | Builtin shadowing, including names in qualified declarations. |
| `recvcheck` | Inconsistent value/pointer receiver choices. |
| `rowserrcheck`, `sqlclosecheck` | SQL iteration errors and closure of recognized rows/statements. |
| `testableexamples` | Executable examples missing an output expectation. |
| `thelper` | Initial `Helper` call in recognized test, benchmark, TB, and fuzz helpers; the testing parameter is first, or second immediately after a context; parameter-name checks stay off. |
| `tparallel` | Parent/subtest parallelism mistakes; it does not require all tests to be parallel. |

The following subrule IDs belong to `revive`. Only these sixteen rules are enabled; the default and all-rules switches are off. [REVIVE] [GOLANGCI]

| ID | What the configuration checks |
| --- | --- |
| `blank-imports` | Side-effect imports outside main/tests without justification; the house scope is narrower than the comment-based escape. |
| `context-as-argument`, `context-keys-type` | Context parameter first, including before testing.T/B/F/TB in test helpers, and unsafe basic context key types. |
| `deep-exit` | Recognized process exits outside `main`, `init`, `TestMain`, and example functions; forbidden exits in exempt functions still need review. |
| `dot-imports` | Dot imports with no allowed-package list. |
| `error-return`, `error-strings` | Error result position and composable message conventions. |
| `exported` | Exported declaration docs and repeated package qualifiers, including public interface methods and methods on private receivers. |
| `indent-error-flow`, `superfluous-else` | Unnecessary branches after terminating paths. |
| `package-comments`, `package-naming` | Package documentation and package-name conventions; matching a standard-library package name alone is allowed. |
| `receiver-naming` | Receiver names, including consistency and avoidance of `this`/`self`. |
| `redundant-import-alias` | An alias identical to the imported package name. |
| `use-any`, `var-naming` | Modern empty-interface spelling, MixedCaps, and initialism conventions. |

`govet` has `disable-all: true` and the following explicit analyzers. [GOLANGCI]

| IDs | Detection area |
| --- | --- |
| `appends`, `assign`, `bools`, `nilfunc`, `nilness`, `shift`, `unreachable`, `unusedresult`, `unusedwrite` | Suspicious expressions, impossible paths, and ineffective results/writes. |
| `asmdecl`, `framepointer`, `cgocall`, `unsafeptr` | Assembly, cgo, and unsafe-pointer misuse. |
| `atomic`, `atomicalign`, `copylocks`, `waitgroup`, `sigchanyzer` | Synchronization misuse, alignment, and signal channels. |
| `buildtag`, `directive`, `stdversion` | Build constraints, compiler directives, and APIs newer than a file's Go version. |
| `composites`, `structtag`, `ifaceassert`, `stdmethods`, `stringintconv` | Struct literals/tags, method contracts, assertions, and integer-to-string mistakes. |
| `deepequalerrors`, `errorsas`, `reflectvaluecompare` | Invalid error inspection and reflection comparisons. |
| `defers`, `lostcancel` | Defer evaluation mistakes and missing cancellation. |
| `hostport`, `httpmux`, `httpresponse` | Network address construction, routing patterns, and response use. |
| `printf`, `slog`, `sortslice`, `timeformat`, `unmarshal` | Recognized standard-library call contracts. |
| `testinggoroutine`, `tests` | Testing entrypoints and goroutine-local test termination. |

`staticcheck` selects only the following 95 `SA` checks; `S`, `ST`, and `QF` families are not enabled. The explicit set avoids changes from rolling catalog defaults. [GOLANGCI]

| IDs | Detection area |
| --- | --- |
| `SA1000`, `SA1001`, `SA1002`, `SA1003`, `SA1004`, `SA1005`, `SA1006`, `SA1007`, `SA1008` | Invalid patterns, formats, durations, process arguments, URLs, and headers. |
| `SA1010`, `SA1011`, `SA1012`, `SA1013`, `SA1014`, `SA1015`, `SA1016`, `SA1017`, `SA1018`, `SA1019` | Invalid library inputs, context, seek/decode, version-sensitive ticker use, signals, and deprecated APIs. |
| `SA1020`, `SA1021`, `SA1023`, `SA1024`, `SA1025`, `SA1026`, `SA1027`, `SA1028`, `SA1029`, `SA1030`, `SA1031`, `SA1032` | Address/IP, writer, cutset/timer, encoding, atomic, sort, context-key, conversion, and error matching contracts. |
| `SA2000`, `SA2001`, `SA2002`, `SA2003` | WaitGroup ordering, empty critical sections, test termination, and deferred locks. |
| `SA3000`, `SA3001` | TestMain exit handling where applicable and benchmark iteration misuse. |
| `SA4000`, `SA4001`, `SA4003`, `SA4004`, `SA4005`, `SA4006`, `SA4008`, `SA4009` | Ineffective comparisons, loops, receiver writes, and overwritten values. |
| `SA4010`, `SA4011`, `SA4012`, `SA4013`, `SA4014`, `SA4015`, `SA4016`, `SA4017`, `SA4018`, `SA4019` | Lost append results, ineffective breaks/expressions, duplicate conditions, assignments, and build constraints. |
| `SA4020`, `SA4021`, `SA4022`, `SA4023`, `SA4024`, `SA4025`, `SA4026`, `SA4027`, `SA4028`, `SA4029`, `SA4030`, `SA4031`, `SA4032` | Unreachable cases, impossible comparisons, numeric mistakes, and ineffective collection/random/platform operations. |
| `SA5000`, `SA5001`, `SA5002`, `SA5003`, `SA5004`, `SA5005`, `SA5007`, `SA5008`, `SA5009`, `SA5010`, `SA5011`, `SA5012` | Nil maps/dereferences, resource timing, spinning, finalizer cycles, recursion, malformed calls/tags, and impossible assertions. |
| `SA6000`, `SA6001`, `SA6002`, `SA6003`, `SA6005`, `SA6006` | Specific avoidable regexp, conversion, pool, and string/byte costs. |
| `SA9001`, `SA9002`, `SA9003`, `SA9004`, `SA9005`, `SA9006`, `SA9007`, `SA9008`, `SA9009` | Deferred loop cleanup, modes, empty branches, enum types, serialization, shifts, directory removal, and directives. |

`gosec` enables exactly these IDs, at all severities and confidence levels. They implement Go API checks supporting this guide and the shared security baseline. A report still needs assessment of reachability and input trust. [GOLANGCI]

| IDs | Detection area |
| --- | --- |
| `G103`, `G106`, `G107`, `G108` | Unsafe code, insecure SSH configuration, variable HTTP URLs, and profiling endpoints. |
| `G110`, `G112`, `G114`, `G115` | Decompression growth, HTTP timeouts, and integer conversion risks. |
| `G201`, `G202`, `G203`, `G204` | SQL construction, trusted HTML conversions, and process execution. |
| `G304`, `G305` | File paths from variables and archive path traversal. |
| `G401`, `G402`, `G403`, `G404`, `G405`, `G406`, `G407` | Weak cryptography, TLS settings, random sources, and fixed initialization vectors. |
| `G501`, `G502`, `G503`, `G504`, `G505` | Imports of known weak cryptographic packages. |

### Coverage limits and verification

Review still decides interface ownership, embedding, option design, serialization semantics, alias necessity, zero-value choices, useful error context, exposure of causes, goroutine ownership, and test clarity. No enabled check proves absence of races or leaks. `deep-exit` skips `init` and example functions, `blank-imports` accepts justifying comments, and scanners cannot establish that every required doc or wire field is correct. The formatter's directory walk skips vendor, testdata, node_modules, and hidden directories. `nakedret`, `nonamedreturns`, `ireturn`, `inamedparam`, `lll`, `exhaustruct_v5`, `testpackage`, `noinlineerr`, `gochecknoinits`, `gochecknoglobals`, `wrapcheck`, and `prealloc` are intentionally absent for the decisions below. [GOLANGCI] [REVIVE]

Not yet run against Go 1.27.3 or golangci-lint 2.15.0. Configuration verification, formatting, linting, builds, and tests require validation with those pinned tools before adoption.

## Naming

- MUST use MixedCaps for exported identifiers and mixedCaps for unexported identifiers, including constants; preserve initialisms such as `ID` and `HTTP`, and omit private-global underscore prefixes. Why: casing communicates visibility consistently. [GO-REVIEW] [GOOGLE-GO]
- PREFER short lowercase package names without underscores or repeated qualifiers, such as `cache.New` rather than `cache.NewCache`. Why: callers already supply the package context. [EFFECTIVE-GO] [GO-REVIEW]
- MUST use a consistent short type-derived receiver name, avoiding `this` and `self`, and avoid shadowing predeclared identifiers. Why: Go receivers are ordinary parameters and builtins have familiar meanings. [GO-REVIEW] [UBER-GO]
- MUST name error sentinels `ErrX` or `errX` and concrete error types `XError`. Why: names distinguish identities from types at call sites. [UBER-GO]
- PREFER property names without `Get` for cheap accessors and verb names such as `Fetch` for costly or fallible retrieval. Why: Go API names should reveal the operation's cost and role. [GOOGLE-GO] [EFFECTIVE-GO]

## Files and layout

- PREFER one package per directory, organizing files by related behavior rather than imposing one type per file. Why: Go's package is the compilation and visibility boundary. [GOOGLE-GO]
- MUST avoid dot imports, including in external tests. Why: qualified names reveal where an API originates. [GOOGLE-GO]
- PREFER `goimports`' standard-library/other import partition without proto or side-effect subgroups. Why: one tool-compatible policy works across ordinary modules. [UBER-GO] [GO-REVIEW]
- PREFER import aliases only for collisions or meaningful clarity, not solely because a path's last component differs from its package name. Why: routine aliases add another name to maintain. [GO-REVIEW] [GOOGLE-GO]
- MUST restrict side-effect imports to main packages or tests that need registration, with `_ "embed"` allowed for `//go:embed`. Why: reusable libraries should not impose hidden registration behavior. [GOOGLE-GO] [GO-REVIEW]
- PREFER explicit startup functions over `init`; keep unavoidable `init` deterministic, without environment reads, I/O, or goroutines. Why: import-time work hides dependencies and lifetime. [UBER-GO]
- MUST allow package-level sentinel errors and logically constant data while keeping library instance state constructible independently. Why: rejecting every global would also reject idiomatic error identities. [GOOGLE-GO] [UBER-GO]

## Types and data

- PREFER small interfaces defined by actual consumers and concrete return types; return an interface only for justified encapsulation or runtime implementation choice. Why: callers get useful behavior without speculative abstractions. [GO-REVIEW] [GOOGLE-GO]
- PREFER compile-time assertions such as `var _ io.Reader = (*Reader)(nil)` for promised interfaces lacking an ordinary static conversion. Why: the compiler checks the contract without redundant assertions everywhere. [EFFECTIVE-GO] [UBER-GO]
- MUST use pointer receivers for mutation or noncopyable synchronization state, and avoid copying structs containing used locks. Why: copies can separate state from its synchronization. [GO-REVIEW] [GOOGLE-GO]
- PREFER consistent receiver kinds for a type and pass ordinary strings, slices, and interfaces by value rather than by pointer. Why: descriptors are small and pointers to interfaces rarely express the intended ownership. [GO-REVIEW] [UBER-GO]
- MUST use named fields rather than embedding merely for convenience, and keep mutexes in named fields. Why: promoted methods can expose implementation and synchronization details. [UBER-GO]
- MUST copy slices and maps when crossing an ownership boundary that promises isolation; copy nested mutable values when a shallow copy is insufficient. Why: assignment preserves access to shared backing state. [UBER-GO] [GO-SPEC]
- MUST represent instants with `time.Time` and elapsed intervals with `time.Duration`; use `AddDate` for calendar changes. Why: calendar units and elapsed time are different contracts. [UBER-GO]
- MUST give marshaled struct fields explicit format tags, including deliberate exclusions. Why: Go field renames must not silently rename wire fields. [UBER-GO]
- PREFER nil slices and `len(s) == 0` for ordinary empty collections; use non-nil empty slices when a wire contract requires `[]` instead of `null`. Why: allocation and serialization have different requirements. [GO-REVIEW] [UBER-GO]
- MUST key literals of structs from other packages; prefer keys for local structs and omit irrelevant zero fields. Why: keys survive field reordering and highlight meaningful initialization. [GOOGLE-GO] [UBER-GO]
- PREFER `var x T` for a zero-valued struct, `&T{}` for its pointer, `make(map[K]V)` for an empty writable map, and a map literal for known entries. Why: these forms distinguish zero initialization from populated data consistently. [UBER-GO]
- PREFER a named option struct or distinct parameter types for unclear literal arguments; introduce functional options only when default-heavy call sites justify their implementation cost, using closures unless richer option behavior is needed. Why: caller needs matter more than an argument-count threshold. [GOOGLE-GO]
- PREFER parameter and result names when they distinguish otherwise ambiguous values, including interface signatures; prefer explicit return expressions while allowing clear short bare returns or deferred result mutation. Why: names should explain contracts rather than satisfy a blanket syntax rule. [GOOGLE-GO] [GO-REVIEW]
- PREFER concrete types for one implementation and type parameters for demonstrated reuse across types; spell an unconstrained value `any`. Why: modern Go supports generics without requiring speculative abstractions. [GOOGLE-GO]
- PREFER an invalid zero enum value unless zero intentionally represents the useful default. Why: uninitialized values should not silently select unintended behavior. [UBER-GO]

## Errors

- PREFER handling every Go error; when an error cannot affect the result, such as closing a read-only file, discard it explicitly with `_ =` and a short reason comment. Why: a visible, justified discard avoids invented error handling and blanket lint suppressions. [GOLANGCI]

- MUST return a final `error` result for fallible operations and literal `nil` on success; use a separate boolean for ordinary absence. Why: valid zero values must remain distinguishable from failure. [GO-REVIEW] [GOOGLE-GO]
- MUST use `errors.Is` and `errors.As` to inspect potentially wrapped errors instead of comparing messages or asserting a concrete error type directly. Why: wrapping preserves semantics through an error chain. [UBER-GO] [GOOGLE-GO]
- MUST use `%w` when exposing an underlying error for caller inspection, and document that exposed identity as part of the API. Why: wrapping creates a compatibility promise. [UBER-GO] [GOOGLE-GO]
- PREFER returning a Go error unchanged when there is no useful context to add; use `%v` or boundary translation when intentionally hiding its concrete identity. Why: redundant wrapping obscures diagnostics and accidental wrapping exposes internals. [UBER-GO] [GOOGLE-GO]
- MUST keep composable error strings lowercase except proper names/acronyms and omit terminal punctuation. Why: errors are commonly embedded in larger messages. [GO-REVIEW]
- PREFER `errors.New` for static error messages and `fmt.Errorf` for interpolation. Why: the call advertises whether formatting is involved. [UBER-GO]
- MUST use returned errors for ordinary failures and restrict `os.Exit` or fatal logging to `main`; a test harness may use `TestMain` for process exit. Why: library callers retain control of recovery and cleanup. [UBER-GO] [GO-TEST]
- MUST avoid blanket recovery of unexpected panics merely to keep a server running; contain only a deliberately designed private panic protocol and re-panic unrelated failures. Why: unknown panic state may violate invariants. [GOOGLE-GO] [EFFECTIVE-GO]
- MUST register `defer` cleanup after successful acquisition, account for close errors that affect the operation, and close each iteration's resources before an unbounded loop continues. Why: defers execute at function return, not block exit. [EFFECTIVE-GO] [GO-REVIEW]
- MUST check `Rows.Err()` after SQL iteration, close rows/statements, and close successful HTTP response bodies. Why: iteration and transport resources have failure modes beyond their initial call. [GOLANGCI]
- PREFER early error returns and `if err := operation(); err != nil` when the result is local to the condition. Why: the successful path remains easy to follow. [EFFECTIVE-GO] [GOOGLE-GO]

- PREFER `log/slog` key-value attributes for structured Go logs; libraries that log accept a caller-supplied `*slog.Logger` instead of a package global, and report an error once where it is handled. Why: [slog handlers](https://pkg.go.dev/log/slog) let the application control destinations and structure. [GO-SLOG]

## Comments and docs

- MUST document exported Go declarations with identifier-led sentence comments and provide a package comment adjacent to one package clause. Why: Go documentation tools associate comments with declarations. [GO-REVIEW] [GOOGLE-GO]
- MUST document significant error identities, caller cleanup duties, and non-obvious concurrency/cancellation behavior on the relevant Go API. Why: these contracts are not visible in a method signature. [GOOGLE-GO]
- PREFER runnable `Example` functions in `*_test.go` with an `Output:` expectation when output is deterministic. Why: `go test` checks examples alongside the implementation. [GOOGLE-GO] [GOLANGCI]

## Testing

- PREFER the standard `testing` package with explicit checks and named table cases sharing one assertion path; comparison libraries may supply diffs. Why: failures remain direct and easy to diagnose. [GOOGLE-GO] [UBER-GO]
- MUST put Go tests in `*_test.go`; use same-package tests when internals matter and external `package_test` tests for public-client behavior or import-cycle avoidance. Why: both package forms serve useful test boundaries. [GOOGLE-GO]
- MUST call `t.Helper()` in reporting test helpers and call `t.Fatal` or `t.FailNow` only from the test's own goroutine. Why: diagnostics need the caller location and termination affects only the calling goroutine. [GOOGLE-GO]
- PREFER `t.Errorf` for independent mismatches and `t.Fatalf` when further checks would be invalid; include the operation, input, got, and want. Why: Go test output should identify the failure without rerunning a debugger. [GOOGLE-GO] [GO-REVIEW]
- MUST test error presence or `errors.Is`/`errors.As` semantics rather than complete message strings unless exact wording is the contract. Why: contextual wrapping should not invalidate semantic tests. [GOOGLE-GO]
- PREFER `t.Context()`, `t.Cleanup`, and `t.TempDir` for test-scoped lifetime and resources. Why: cleanup then follows the test and its subtests. [GOOGLE-GO] [GO-TEST]
- MUST use `t.Parallel` only when each case's mutable state and process-wide settings are isolated, and join test-created goroutines before the test ends. Why: per-iteration variables do not isolate referenced data or global state. [GOOGLE-GO] [UBER-GO]
- PREFER race-detector runs for concurrent packages and `net/http/httptest` for HTTP boundary tests. Why: real synchronization and transports expose defects that isolated function calls miss. [GOOGLE-GO] [GO-TEST]

## Performance

- PREFER synchronous functions and let callers introduce concurrency. Why: callers can own cancellation and completion without hidden workers. [GO-REVIEW]
- PREFER capacity hints when a final size is known or benchmarks justify them; do not require speculative preallocation everywhere. Why: oversized backing storage also costs memory. [GOOGLE-GO] [UBER-GO]
- PREFER `strconv` for primitive conversions and reuse string-to-byte conversions on measured hot paths. Why: general formatting and repeated allocation can dominate small operations. [UBER-GO]

## Security

- MUST generate keys and security tokens with `crypto/rand`, never `math/rand` or `math/rand/v2`. Why: simulation generators do not provide cryptographic unpredictability. [GO-REVIEW]
- MUST use `html/template` for HTML rendering and avoid converting untrusted strings to trusted template types. Why: trusted-type casts bypass Go's contextual escaping. [EFFECTIVE-GO] [GOLANGCI]
- MUST configure HTTP server timeouts and attach request contexts to outbound operations with context-aware APIs. Why: Go's convenient default network entrypoints can leave work unbounded in time. [GOLANGCI] [GO-REVIEW]
- PREFER avoiding `unsafe` and cgo in ordinary application code, with any necessary use confined to a documented boundary. Why: those APIs bypass ordinary Go memory guarantees. [GOLANGCI]

## Language-specific pitfalls

- MUST return an untyped `nil` for an absent interface or successful `error`, rather than a typed nil pointer converted to that interface. Why: an interface holding a concrete type is non-nil. [GO-FAQ]
- MUST rely on per-iteration variables for Go 1.22+ loops declared with `:=`, avoiding redundant `v := v`; explicitly protect captured preexisting variables assigned with `=`. Why: only newly declared loop variables receive independent iteration storage. [GO-SPEC] [GOLANGCI]
- MUST use comma-ok assertions when a dynamic type is uncertain, initialize maps before writes, and retain the slice returned by `append`. Why: these Go operations otherwise panic or lose updated state. [EFFECTIVE-GO] [GOOGLE-GO]
- MUST distinguish slice length from capacity when constructing an append destination, using zero length if no initial elements are intended. Why: `make([]T, n)` already creates `n` elements. [GO-SPEC] [GOLANGCI]

### Contexts and concurrency

- MUST pass the caller's `context.Context` first through request-related calls, with the testing parameter immediately after any context in test helpers; avoid context fields except when a fixed external API requires one. Why: cancellation and request lifetime must follow the call chain. [GO-REVIEW] [GOOGLE-GO]
- MUST call each derived context's cancel function when its work ends, normally with `defer cancel()` after creation. Why: cancellation releases associated resources promptly. [GO-CONTEXT]
- MUST reserve context values for request-scoped metadata and use private key types; keep ordinary configuration in parameters or fields. Why: basic keys collide and hidden arguments obscure dependencies. [GO-REVIEW] [GO-CONTEXT]
- MUST give every goroutine an owner, a stopping condition, and a way for its owner to wait for completion. Why: abandoned or blocked work leaks resources and can outlive its state. [UBER-GO] [GO-REVIEW]
- MUST bound goroutine creation and ensure potentially blocking channel operations can finish or observe cancellation. Why: limiting active work after spawning does not bound waiting goroutines. [EFFECTIVE-GO] [GOOGLE-GO]
- PREFER directional channel parameters and unbuffered channels or a buffer of one unless the queue's capacity and full behavior are justified. Why: channel contracts should expose permitted operations and backpressure. [GOOGLE-GO] [UBER-GO]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST use mixedCaps without an underscore prefix for private globals (Google excludes ordinary underscores; Uber prefixes private globals). Why: one Go naming rule works at every scope. [GOOGLE-GO] [UBER-GO]
- PREFER the standard-library/other import partition (Uber's two groups versus Google's standard/other/proto/side-effect groups). Why: `goimports` supports the simpler ordinary-module convention. [UBER-GO] [GOOGLE-GO]
- PREFER aliases for collisions or material clarity only (Uber requires path/name-mismatch aliases; the wiki and Google avoid routine renaming). Why: package declarations already establish the local import name. [UBER-GO] [GO-REVIEW] [GOOGLE-GO]
- MUST prohibit dot imports even in external tests (the wiki and Effective Go permit a narrow test case; Google forbids them). Why: origin remains explicit in every file. [GO-REVIEW] [EFFECTIVE-GO] [GOOGLE-GO]
- PREFER no numeric source-width target (Google and the wiki have none; Uber suggests a soft 99 columns). Why: formatter output and readable expressions govern layout. [GOOGLE-GO] [GO-REVIEW] [UBER-GO]
- PREFER simplifying complex expressions before changing layout (Google prioritizes refactoring; Effective Go suggests manually wrapping an uncomfortable line). Why: simpler expressions improve meaning independently of display width. [GOOGLE-GO] [EFFECTIVE-GO]
- PREFER standard `testing` with explicit checks and optional comparison helpers (Google bans assertion frameworks; Uber demonstrates testify). Why: direct diagnostics are a portable default without importing Google's absolute organizational ban. [GOOGLE-GO] [UBER-GO]
- MUST avoid convenience-only embedding (Effective Go embeds a logger for convenience; Uber rejects exposing incidental implementation). Why: named fields preserve deliberate method sets. [EFFECTIVE-GO] [UBER-GO]
- MUST avoid blanket recovery from unexpected server panics (Effective Go demonstrates containment; Google warns of corrupted state). Why: only a designed private panic protocol establishes a safe recovery contract. [EFFECTIVE-GO] [GOOGLE-GO]
- MUST restrict ordinary process exits to `main`, allowing `TestMain` harness exit (Uber requires main-only exits; Google permits its internal fatal logger elsewhere). Why: libraries stay reusable without adopting a Google-specific fatal-logging model. [UBER-GO] [GOOGLE-GO] [GO-TEST]
- PREFER explicit startup with narrowly justified deterministic `init` (Effective Go allows environmental init work; Uber discourages it). Why: startup errors and resource lifetimes stay visible. [EFFECTIVE-GO] [UBER-GO]
- PREFER concrete results with justified encapsulation/runtime-factory exceptions (the wiki favors concrete types; Effective Go hides implementations behind interfaces; Google documents exceptions). Why: a default plus bounded exceptions fits real APIs. [GO-REVIEW] [EFFECTIVE-GO] [GOOGLE-GO]
- PREFER interface assertions only for promised contracts lacking another static conversion (Effective Go reserves them for rare gaps; Uber recommends broader contractual assertions). Why: the compiler catches missing methods without duplicating checks everywhere. [EFFECTIVE-GO] [UBER-GO]
- PREFER named option fields or clearer parameter types over argument-name comments (Uber suggests inline literal labels; Google favors option structures or docs). Why: the API carries the meaning to every call site. [UBER-GO] [GOOGLE-GO]
- PREFER closure-based functional options when options are justified (Google illustrates closures; Uber prefers a private-method Option interface). Why: closures need less scaffolding unless richer option behavior has a concrete use. [GOOGLE-GO] [UBER-GO]
- PREFER selecting options by caller needs and default usage (Uber suggests growing APIs, especially three-plus arguments; Google stresses overhead and call sites). Why: parameter count alone does not justify a framework. [UBER-GO] [GOOGLE-GO]
- PREFER `&T{}` for zero struct pointers (Uber selects it; Google and Effective Go also allow `new(T)`). Why: it extends directly to keyed initialization. [UBER-GO] [GOOGLE-GO] [EFFECTIVE-GO]
- PREFER `make` for empty writable maps and literals for known entries (Uber chooses those forms; Google leaves empty forms interchangeable). Why: the initializer communicates how entries arrive. [UBER-GO] [GOOGLE-GO]
- PREFER `var x T` for zero-valued structs (Uber requires it; Google's decisions allow alternatives while best practices favor zero declarations). Why: one default communicates readiness without explicit empty contents. [UBER-GO] [GOOGLE-GO]
- PREFER `errors.New` for static messages (Uber selects it; Google also permits constant `fmt.Errorf`). Why: the API choice signals that no formatting occurs. [UBER-GO] [GOOGLE-GO]
- PREFER preallocation only for known sizes or measured benefit (Uber emphasizes capacity hints; Google rejects a general readability requirement). Why: speculative reservation can waste memory. [UBER-GO] [GOOGLE-GO]
- PREFER nil empty slices except when serialization or another contract requires non-nil empties (Uber's ordinary return rule favors nil; the wiki makes the wire-format exception explicit). Why: `null` and `[]` may be observably different. [UBER-GO] [GO-REVIEW]
- PREFER leaving `lll` disabled (the optional checker enforces a maximum; Google and the wiki reject rigid widths). Why: a column check would contradict the selected layout policy. [GOLANGCI] [GOOGLE-GO] [GO-REVIEW]
- PREFER omitting irrelevant zero fields and leaving `exhaustruct_v5` disabled (the optional checker can demand every field; Google and Uber permit omission). Why: meaningful fields should remain visible. [GOLANGCI] [GOOGLE-GO] [UBER-GO]
- MUST allow both same-package and external tests, leaving `testpackage` disabled (that checker can require external packages; Google supports both). Why: the needed test boundary decides access. [GOLANGCI] [GOOGLE-GO]
- PREFER informative named results and leave `nonamedreturns` disabled (the optional checker rejects them; the guides allow documentation and deferred mutation). Why: names can express real API meaning. [GOLANGCI] [EFFECTIVE-GO] [GO-REVIEW] [GOOGLE-GO]
- PREFER explicit results while permitting clear short bare returns, leaving `nakedret` disabled (its zero threshold forbids every bare return; the wiki and Google permit short cases). Why: review can assess clarity without an arbitrary function-size cutoff. [GOLANGCI] [GO-REVIEW] [GOOGLE-GO]
- PREFER scoped `if err := ...` checks and leave `noinlineerr` disabled (that checker bans them; Effective Go and Google use them). Why: local errors can remain local without obscuring the successful path. [GOLANGCI] [EFFECTIVE-GO] [GOOGLE-GO]
- PREFER narrowly justified `init` and leave `gochecknoinits` disabled (the optional checker bans all init; Uber permits limited cases and Effective Go is broader). Why: deterministic registration can require an init hook. [GOLANGCI] [UBER-GO] [EFFECTIVE-GO]
- MUST allow sentinel variables and logically constant package data, leaving `gochecknoglobals` disabled (the checker rejects globals; Uber and Google permit these uses). Why: Go's error identities need stable package values. [GOLANGCI] [UBER-GO] [GOOGLE-GO]
- PREFER context-bearing wrapping only, leaving `wrapcheck` disabled (it can demand wrapping every external error; Uber and Google reject redundant annotations). Why: unchanged errors can already contain the full useful diagnostic. [GOLANGCI] [UBER-GO] [GOOGLE-GO]
- PREFER naming interface parameters when informative, leaving `inamedparam` disabled (it requires names; Effective Go and Google accept concise unnamed signatures). Why: a repeated obvious type name adds no contract information. [GOLANGCI] [EFFECTIVE-GO] [GOOGLE-GO]
- PREFER concrete results with the documented exceptions, leaving `ireturn` disabled (it can reject interfaces; Effective Go and Google permit encapsulation and factory cases). Why: blanket enforcement would reject legitimate APIs. [GOLANGCI] [EFFECTIVE-GO] [GOOGLE-GO]
- MUST omit redundant capture copies for loops declaring variables with `:=` under the modern baseline (Uber's old example copies them; Effective Go qualifies the old bug and `copyloopvar` catches redundant copies). Why: Go 1.22+ supplies iteration-local variables, while preexisting `=` variables still need care. [UBER-GO] [EFFECTIVE-GO] [GOLANGCI] [GO-SPEC]
- MUST use `revive` instead of deprecated `golint` (D1: Uber's introduction names golint while its later linting section replaces it). Why: the maintained tool fits the selected v2 runner. [UBER-GO] [GOLANGCI]
- PREFER justified generics under the declared modern Go baseline (D2: Effective Go's append explanation predates caller-selected type parameters; Google permits them). Why: outdated tutorial prose is not a language restriction. [EFFECTIVE-GO] [GOOGLE-GO] [GO-SPEC]
