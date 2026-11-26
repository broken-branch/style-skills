# Uber Go rules

Condensed Uber Go Style Guide. The editor setup and example lint configuration are omitted. Public atomic and goroutine-leak libraries remain part of the source guidance.

Source owner: Uber Technologies, Inc. License: [Apache-2.0](../LICENSE). Changes by style-skills contributors: rules restated and shortened, examples omitted, source-local rules removed, and scope/version clarifications identified. Unofficial; no endorsement is implied.

## Quick rules

Read the topic sections below; each retained source rule appears once.

## Tooling

- Use gofmt to handle source formatting. — [Uber: Introduction](https://github.com/uber-go/guide/blob/master/style.md#introduction). <!-- uber-go-style:1 -->
- Treat the introduction's golint advice as dated; the Linting section's revive recommendation supersedes it. — [Uber: Introduction](https://github.com/uber-go/guide/blob/master/style.md#introduction). <!-- uber-go-style:4 -->
- Use 99 columns as a soft source-width target. — [Uber: Avoid overly long lines](https://github.com/uber-go/guide/blob/master/style.md#avoid-overly-long-lines). <!-- uber-go-style:87 -->
- Wrap before the width target when sensible, allowing justified longer lines. — [Uber: Avoid overly long lines](https://github.com/uber-go/guide/blob/master/style.md#avoid-overly-long-lines). <!-- uber-go-style:88 -->
- Keep extracted printf format text in a constant so vet can analyze it. — [Uber: Format Strings outside Printf](https://github.com/uber-go/guide/blob/master/style.md#format-strings-outside-printf). <!-- uber-go-style:149 -->
- Apply linting consistently throughout the repository. — [Uber: Linting](https://github.com/uber-go/guide/blob/master/style.md#linting). <!-- uber-go-style:166 -->
- Use errcheck, goimports, revive, govet, and staticcheck as the guide's suggested minimum checks. — [Uber: Linting](https://github.com/uber-go/guide/blob/master/style.md#linting). <!-- uber-go-style:167 -->
- Replace deprecated golint with revive. — [Uber: Linting](https://github.com/uber-go/guide/blob/master/style.md#linting). <!-- uber-go-style:168 -->
- Prefer golangci-lint to run the selected checks. — [Uber: Lint Runners](https://github.com/uber-go/guide/blob/master/style.md#lint-runners). <!-- uber-go-style:169 -->
- Add linters according to the project's needs. — [Uber: Lint Runners](https://github.com/uber-go/guide/blob/master/style.md#lint-runners). <!-- uber-go-style:170 -->

## Naming

- Include the unit in a field's name when an external duration must be numeric. — [Uber: Use time.Time and time.Duration with external systems](https://github.com/uber-go/guide/blob/master/style.md#use-timetime-and-timeduration-with-external-systems). <!-- uber-go-style:27 -->
- Name sentinel variables with Err when exported and err when private. — [Uber: Error Naming](https://github.com/uber-go/guide/blob/master/style.md#error-naming). <!-- uber-go-style:42 -->
- For private sentinel errors, err takes precedence over the usual underscore prefix. — [Uber: Error Naming](https://github.com/uber-go/guide/blob/master/style.md#error-naming). <!-- uber-go-style:43 -->
- Use an Error suffix for custom error type names. — [Uber: Error Naming](https://github.com/uber-go/guide/blob/master/style.md#error-naming). <!-- uber-go-style:44 -->
- Do not shadow Go's predeclared identifiers with application names. — [Uber: Avoid Using Built-In Names](https://github.com/uber-go/guide/blob/master/style.md#avoid-using-built-in-names). <!-- uber-go-style:58 -->
- Keep package identifiers lowercase and free of underscores. — [Uber: Package Names](https://github.com/uber-go/guide/blob/master/style.md#package-names). <!-- uber-go-style:95 -->
- Choose compact package names that rarely need an import alias. — [Uber: Package Names](https://github.com/uber-go/guide/blob/master/style.md#package-names). <!-- uber-go-style:96 -->
- Prefer a singular noun for a package name. — [Uber: Package Names](https://github.com/uber-go/guide/blob/master/style.md#package-names). <!-- uber-go-style:97 -->
- Avoid catch-all package names that fail to describe a responsibility. — [Uber: Package Names](https://github.com/uber-go/guide/blob/master/style.md#package-names). <!-- uber-go-style:98 -->
- Use mixed capitalization for function identifiers. — [Uber: Function Names](https://github.com/uber-go/guide/blob/master/style.md#function-names). <!-- uber-go-style:99 -->
- Underscores may group related scenarios in test function names. — [Uber: Function Names](https://github.com/uber-go/guide/blob/master/style.md#function-names). <!-- uber-go-style:100 -->
- Begin private package variables and constants with an underscore. — [Uber: Prefix Unexported Globals with _](https://github.com/uber-go/guide/blob/master/style.md#prefix-unexported-globals-with-_). <!-- uber-go-style:113 -->
- Private sentinel errors may use err instead of the underscore convention. — [Uber: Prefix Unexported Globals with _](https://github.com/uber-go/guide/blob/master/style.md#prefix-unexported-globals-with-_). <!-- uber-go-style:114 -->
- Choose a familiar printf-style name for a formatting helper when possible. — [Uber: Naming Printf-style Functions](https://github.com/uber-go/guide/blob/master/style.md#naming-printf-style-functions). <!-- uber-go-style:150 -->
- Otherwise suffix a formatting helper with f and configure vet to recognize it if needed. — [Uber: Naming Printf-style Functions](https://github.com/uber-go/guide/blob/master/style.md#naming-printf-style-functions). <!-- uber-go-style:151 -->
- Call a test table tests and its current row tt. — [Uber: Test Tables](https://github.com/uber-go/guide/blob/master/style.md#test-tables). <!-- uber-go-style:153 -->
- Prefix test inputs with give and expected values with want. — [Uber: Test Tables](https://github.com/uber-go/guide/blob/master/style.md#test-tables). <!-- uber-go-style:154 -->

## Files and layout

- Migrate style across at least a whole package so competing conventions do not coexist within it. — [Uber: Be Consistent](https://github.com/uber-go/guide/blob/master/style.md#be-consistent). <!-- uber-go-style:90 -->
- Group related declarations of imports, types, constants, and variables. — [Uber: Group Similar Declarations](https://github.com/uber-go/guide/blob/master/style.md#group-similar-declarations). <!-- uber-go-style:91 -->
- Keep unrelated declarations separate unless the adjacent-variable exception applies. — [Uber: Group Similar Declarations](https://github.com/uber-go/guide/blob/master/style.md#group-similar-declarations). <!-- uber-go-style:92 -->
- Group neighboring variable declarations, especially local ones, even when their roles differ. — [Uber: Group Similar Declarations](https://github.com/uber-go/guide/blob/master/style.md#group-similar-declarations). <!-- uber-go-style:93 -->
- Separate imports into standard-library and non-standard-library groups, in that order. — [Uber: Import Group Ordering](https://github.com/uber-go/guide/blob/master/style.md#import-group-ordering). <!-- uber-go-style:94 -->
- Add an explicit alias when an imported package's name differs from its path's last element. — [Uber: Import Aliasing](https://github.com/uber-go/guide/blob/master/style.md#import-aliasing). <!-- uber-go-style:101 -->
- Otherwise add an alias only to resolve a direct name collision. — [Uber: Import Aliasing](https://github.com/uber-go/guide/blob/master/style.md#import-aliasing). <!-- uber-go-style:102 -->
- Arrange functions roughly in the order readers encounter calls. — [Uber: Function Grouping and Ordering](https://github.com/uber-go/guide/blob/master/style.md#function-grouping-and-ordering). <!-- uber-go-style:103 -->
- Keep methods of the same receiver together. — [Uber: Function Grouping and Ordering](https://github.com/uber-go/guide/blob/master/style.md#function-grouping-and-ordering). <!-- uber-go-style:104 -->
- Place exported functions near the beginning, after type, constant, and variable declarations. — [Uber: Function Grouping and Ordering](https://github.com/uber-go/guide/blob/master/style.md#function-grouping-and-ordering). <!-- uber-go-style:105 -->
- A constructor may sit directly after its type and before the type's other methods. — [Uber: Function Grouping and Ordering](https://github.com/uber-go/guide/blob/master/style.md#function-grouping-and-ordering). <!-- uber-go-style:106 -->
- Move standalone utility functions toward the end of the file. — [Uber: Function Grouping and Ordering](https://github.com/uber-go/guide/blob/master/style.md#function-grouping-and-ordering). <!-- uber-go-style:107 -->
- List embedded struct fields first, then separate named fields with an empty line. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:115 -->

## Types and data

- Pass interfaces directly in normal APIs rather than pointers to interface values. — [Uber: Pointers to Interfaces](https://github.com/uber-go/guide/blob/master/style.md#pointers-to-interfaces). <!-- uber-go-style:5 -->
- Store a pointer implementation in an interface when its methods need to modify implementation state. — [Uber: Pointers to Interfaces](https://github.com/uber-go/guide/blob/master/style.md#pointers-to-interfaces). <!-- uber-go-style:6 -->
- Check interface satisfaction at compile time when required by public contracts, related implementations, or callers' expectations. — [Uber: Verify Interface Compliance](https://github.com/uber-go/guide/blob/master/style.md#verify-interface-compliance). <!-- uber-go-style:7 -->
- Use the implementation type's zero value in the compile-time interface assignment. — [Uber: Verify Interface Compliance](https://github.com/uber-go/guide/blob/master/style.md#verify-interface-compliance). <!-- uber-go-style:8 -->
- Distinguish value and pointer method sets and require an addressable value for an implicit pointer-method call. — [Uber: Receivers and Interfaces](https://github.com/uber-go/guide/blob/master/style.md#receivers-and-interfaces). <!-- uber-go-style:9 -->
- Supply a pointer implementation when the interface requires methods absent from the value's method set. — [Uber: Receivers and Interfaces](https://github.com/uber-go/guide/blob/master/style.md#receivers-and-interfaces). <!-- uber-go-style:10 -->
- Use a sync mutex's ready-to-use zero value instead of allocating an unnecessary pointer. — [Uber: Zero-value Mutexes are Valid](https://github.com/uber-go/guide/blob/master/style.md#zero-value-mutexes-are-valid). <!-- uber-go-style:11 -->
- Keep mutexes as value fields inside structs accessed through pointers. — [Uber: Zero-value Mutexes are Valid](https://github.com/uber-go/guide/blob/master/style.md#zero-value-mutexes-are-valid). <!-- uber-go-style:12 -->
- Use a named mutex field rather than embedding, even for private structs. — [Uber: Zero-value Mutexes are Valid](https://github.com/uber-go/guide/blob/master/style.md#zero-value-mutexes-are-valid). <!-- uber-go-style:13 -->
- Copy incoming slices or maps when retaining caller-owned storage would expose internal state to later caller mutation. — [Uber: Receiving Slices and Maps](https://github.com/uber-go/guide/blob/master/style.md#receiving-slices-and-maps). <!-- uber-go-style:14 -->
- Copy outgoing slices or maps when callers should not be able to mutate internal backing data. — [Uber: Returning Slices and Maps](https://github.com/uber-go/guide/blob/master/style.md#returning-slices-and-maps). <!-- uber-go-style:15 -->
- Begin iota enumerations at one by default. — [Uber: Start Enums at One](https://github.com/uber-go/guide/blob/master/style.md#start-enums-at-one). <!-- uber-go-style:20 -->
- Reserve an enum's zero value for an intentional usable default when appropriate. — [Uber: Start Enums at One](https://github.com/uber-go/guide/blob/master/style.md#start-enums-at-one). <!-- uber-go-style:21 -->
- Use the time package for calendar calculations instead of assuming fixed calendar-unit lengths. — [Uber: Use time to handle time](https://github.com/uber-go/guide/blob/master/style.md#use-time-to-handle-time). <!-- uber-go-style:22 -->
- Represent points in time with time.Time and operate on them through its methods. — [Uber: Use time.Time for instants of time](https://github.com/uber-go/guide/blob/master/style.md#use-timetime-for-instants-of-time). <!-- uber-go-style:23 -->
- Represent elapsed intervals with time.Duration. — [Uber: Use time.Duration for periods of time](https://github.com/uber-go/guide/blob/master/style.md#use-timeduration-for-periods-of-time). <!-- uber-go-style:24 -->
- Use AddDate for calendar changes and Add for fixed durations. — [Uber: Use time.Duration for periods of time](https://github.com/uber-go/guide/blob/master/style.md#use-timeduration-for-periods-of-time). <!-- uber-go-style:25 -->
- Preserve time.Time and time.Duration across external boundaries when the protocol supports them. — [Uber: Use time.Time and time.Duration with external systems](https://github.com/uber-go/guide/blob/master/style.md#use-timetime-and-timeduration-with-external-systems). <!-- uber-go-style:26 -->
- Usually encode an instant as RFC 3339 text when a typed time.Time cannot cross the boundary. — [Uber: Use time.Time and time.Duration with external systems](https://github.com/uber-go/guide/blob/master/style.md#use-timetime-and-timeduration-with-external-systems). <!-- uber-go-style:28 -->
- Inject dependencies rather than changing global variables or function values. — [Uber: Avoid Mutable Globals](https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals). <!-- uber-go-style:54 -->
- Avoid exported struct embedding that exposes internals or prevents changing the implementation. — [Uber: Avoid Embedding Types in Public Structs](https://github.com/uber-go/guide/blob/master/style.md#avoid-embedding-types-in-public-structs). <!-- uber-go-style:55 -->
- Use explicit forwarding methods to expose the intended API without revealing an inner type. — [Uber: Avoid Embedding Types in Public Structs](https://github.com/uber-go/guide/blob/master/style.md#avoid-embedding-types-in-public-structs). <!-- uber-go-style:56 -->
- Treat changes to promoted public members as possible compatibility breaks. — [Uber: Avoid Embedding Types in Public Structs](https://github.com/uber-go/guide/blob/master/style.md#avoid-embedding-types-in-public-structs). <!-- uber-go-style:57 -->
- Tag serialized fields explicitly so renaming Go fields does not accidentally alter their wire names. — [Uber: Use field tags in marshaled structs](https://github.com/uber-go/guide/blob/master/style.md#use-field-tags-in-marshaled-structs). <!-- uber-go-style:71 -->
- Declare package-scope variables with var. — [Uber: Top-level Variable Declarations](https://github.com/uber-go/guide/blob/master/style.md#top-level-variable-declarations). <!-- uber-go-style:110 -->
- Let the initializer infer a variable's type when it is exactly the intended type. — [Uber: Top-level Variable Declarations](https://github.com/uber-go/guide/blob/master/style.md#top-level-variable-declarations). <!-- uber-go-style:111 -->
- Write the type explicitly when it deliberately differs from the initializer's type. — [Uber: Top-level Variable Declarations](https://github.com/uber-go/guide/blob/master/style.md#top-level-variable-declarations). <!-- uber-go-style:112 -->
- Embed a type only when doing so adds meaningful semantics. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:116 -->
- Keep mutexes in named fields rather than embedding them. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:117 -->
- Do not embed solely to save typing or improve appearance. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:118 -->
- Ensure embedding does not complicate construction or use of the containing type. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:119 -->
- Preserve a usable zero value for the containing type. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:120 -->
- Do not expose private types or irrelevant members through promotion. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:121 -->
- Keep embedding compatible with the outer type's intended copying, meaning, and API. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:122 -->
- Embed the inner type in its customary pointer or value form. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:123 -->
- Do not let embedding disclose internal representation or grant unintended control over it. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:124 -->
- Keep the behavior of promoted operations unsurprising to callers. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:125 -->
- Use a named field if some of the inner type's public members should not belong to the outer API. — [Uber: Embedding in Structs](https://github.com/uber-go/guide/blob/master/style.md#embedding-in-structs). <!-- uber-go-style:126 -->
- Use := for local declarations with an explicit initial value. — [Uber: Local Variable Declarations](https://github.com/uber-go/guide/blob/master/style.md#local-variable-declarations). <!-- uber-go-style:127 -->
- Use var when zero initialization is the clearest intent. — [Uber: Local Variable Declarations](https://github.com/uber-go/guide/blob/master/style.md#local-variable-declarations). <!-- uber-go-style:128 -->
- Return nil instead of manufacturing an empty slice when the API allows it. — [Uber: nil is a valid slice](https://github.com/uber-go/guide/blob/master/style.md#nil-is-a-valid-slice). <!-- uber-go-style:129 -->
- Check a slice's length to determine emptiness. — [Uber: nil is a valid slice](https://github.com/uber-go/guide/blob/master/style.md#nil-is-a-valid-slice). <!-- uber-go-style:130 -->
- Append directly to a zero-value slice without making an empty allocation first. — [Uber: nil is a valid slice](https://github.com/uber-go/guide/blob/master/style.md#nil-is-a-valid-slice). <!-- uber-go-style:131 -->
- Account for serializers that distinguish nil from allocated empty slices. — [Uber: nil is a valid slice](https://github.com/uber-go/guide/blob/master/style.md#nil-is-a-valid-slice). <!-- uber-go-style:132 -->
- Keep constants local unless shared use or a public contract requires broader visibility. — [Uber: Reduce Scope of Variables](https://github.com/uber-go/guide/blob/master/style.md#reduce-scope-of-variables). <!-- uber-go-style:136 -->
- Replace an opaque boolean parameter with a descriptive enum when practical. — [Uber: Avoid Naked Parameters](https://github.com/uber-go/guide/blob/master/style.md#avoid-naked-parameters). <!-- uber-go-style:138 -->
- Choose raw string literals when they remove distracting escape sequences. — [Uber: Use Raw String Literals to Avoid Escaping](https://github.com/uber-go/guide/blob/master/style.md#use-raw-string-literals-to-avoid-escaping). <!-- uber-go-style:139 -->
- Use field names in nearly all struct literals. — [Uber: Use Field Names to Initialize Structs](https://github.com/uber-go/guide/blob/master/style.md#use-field-names-to-initialize-structs). <!-- uber-go-style:140 -->
- Omit zero-valued fields that contribute no useful information. — [Uber: Omit Zero Value Fields in Structs](https://github.com/uber-go/guide/blob/master/style.md#omit-zero-value-fields-in-structs). <!-- uber-go-style:142 -->
- Include explicit zero-valued fields when their names clarify intent, particularly in tests. — [Uber: Omit Zero Value Fields in Structs](https://github.com/uber-go/guide/blob/master/style.md#omit-zero-value-fields-in-structs). <!-- uber-go-style:143 -->
- Use var for a struct intended to contain only zero values. — [Uber: Use var for Zero Value Structs](https://github.com/uber-go/guide/blob/master/style.md#use-var-for-zero-value-structs). <!-- uber-go-style:144 -->
- Construct struct pointers with &T{} rather than new(T). — [Uber: Initializing Struct References](https://github.com/uber-go/guide/blob/master/style.md#initializing-struct-references). <!-- uber-go-style:145 -->
- Initialize empty or programmatically filled maps with make. — [Uber: Initializing Maps](https://github.com/uber-go/guide/blob/master/style.md#initializing-maps). <!-- uber-go-style:146 -->
- Use a literal when a map starts with a fixed collection of entries. — [Uber: Initializing Maps](https://github.com/uber-go/guide/blob/master/style.md#initializing-maps). <!-- uber-go-style:148 -->
- Use functional options for growing public APIs with optional inputs, especially constructors already taking three or more arguments. — [Uber: Functional Options](https://github.com/uber-go/guide/blob/master/style.md#functional-options). <!-- uber-go-style:163 -->
- Prefer an Option interface whose private apply method updates private option state. — [Uber: Functional Options](https://github.com/uber-go/guide/blob/master/style.md#functional-options). <!-- uber-go-style:164 -->
- Prefer that interface to closure-only options when comparison, debugging, or future methods matter. — [Uber: Functional Options](https://github.com/uber-go/guide/blob/master/style.md#functional-options). <!-- uber-go-style:165 -->

## Errors

- Create fixed-message errors with errors.New when callers do not need identity matching. — [Uber: Error Types](https://github.com/uber-go/guide/blob/master/style.md#error-types). <!-- uber-go-style:30 -->
- Use fmt.Errorf for contextual errors whose identity callers need not recognize. — [Uber: Error Types](https://github.com/uber-go/guide/blob/master/style.md#error-types). <!-- uber-go-style:31 -->
- Expose a package-level sentinel for a fixed error condition that callers must identify. — [Uber: Error Types](https://github.com/uber-go/guide/blob/master/style.md#error-types). <!-- uber-go-style:32 -->
- Provide a custom error type when callers need to inspect variable error details. — [Uber: Error Types](https://github.com/uber-go/guide/blob/master/style.md#error-types). <!-- uber-go-style:33 -->
- Maintain exported error types and values as public API. — [Uber: Error Types](https://github.com/uber-go/guide/blob/master/style.md#error-types). <!-- uber-go-style:34 -->
- Forward a downstream error directly if it already contains sufficient context. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:35 -->
- Add missing context briefly with fmt.Errorf. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:36 -->
- Normally wrap with %w when callers should be able to inspect the underlying cause. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:37 -->
- Use %v when the underlying error's identity should stay outside the API. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:38 -->
- Document and test sentinel identities and error types intentionally exposed through wrapping. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:39 -->
- Avoid piling repetitive failure announcements onto an error as it travels upward. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:40 -->
- When recording an error outside a return chain, make the surrounding entry clearly identify it as a failure. — [Uber: Error Wrapping](https://github.com/uber-go/guide/blob/master/style.md#error-wrapping). <!-- uber-go-style:41 -->
- Resolve or propagate a failure once instead of both logging and returning it. — [Uber: Handle Errors Once](https://github.com/uber-go/guide/blob/master/style.md#handle-errors-once). <!-- uber-go-style:45 -->
- Use errors.Is or errors.As for recovery based on documented error identities. — [Uber: Handle Errors Once](https://github.com/uber-go/guide/blob/master/style.md#handle-errors-once). <!-- uber-go-style:46 -->
- Propagate unresolved failures with context; log only when handling them and continuing with reduced behavior. — [Uber: Handle Errors Once](https://github.com/uber-go/guide/blob/master/style.md#handle-errors-once). <!-- uber-go-style:47 -->
- Use the assertion's boolean result to handle a possible dynamic-type mismatch. — [Uber: Handle Type Assertion Failures](https://github.com/uber-go/guide/blob/master/style.md#handle-type-assertion-failures). <!-- uber-go-style:48 -->
- Avoid production panics and return failures so callers can choose a response. — [Uber: Don't Panic](https://github.com/uber-go/guide/blob/master/style.md#dont-panic). <!-- uber-go-style:49 -->
- Do not use panic and recover as routine control flow for errors. — [Uber: Don't Panic](https://github.com/uber-go/guide/blob/master/style.md#dont-panic). <!-- uber-go-style:50 -->
- Unrecoverable startup setup can justify a panic. — [Uber: Don't Panic](https://github.com/uber-go/guide/blob/master/style.md#dont-panic). <!-- uber-go-style:51 -->
- Confine process termination through os.Exit or fatal logging to main. — [Uber: Exit in Main](https://github.com/uber-go/guide/blob/master/style.md#exit-in-main). <!-- uber-go-style:66 -->
- Return errors from other functions rather than terminating the process. — [Uber: Exit in Main](https://github.com/uber-go/guide/blob/master/style.md#exit-in-main). <!-- uber-go-style:67 -->
- Prefer a single process-exit invocation in main. — [Uber: Exit Once](https://github.com/uber-go/guide/blob/master/style.md#exit-once). <!-- uber-go-style:68 -->
- Choose the helper's signature freely while keeping actual process termination centralized. — [Uber: Exit Once](https://github.com/uber-go/guide/blob/master/style.md#exit-once). <!-- uber-go-style:70 -->
- Return or continue early for exceptional cases so the ordinary path remains shallow. — [Uber: Reduce Nesting](https://github.com/uber-go/guide/blob/master/style.md#reduce-nesting). <!-- uber-go-style:108 -->

## Comments and docs

- Annotate an unclear literal argument with a block comment naming its parameter. — [Uber: Avoid Naked Parameters](https://github.com/uber-go/guide/blob/master/style.md#avoid-naked-parameters). <!-- uber-go-style:137 -->

## Testing

- Use `go.uber.org/goleak` to check packages that start goroutines for leaks. — [Uber — Goroutine lifetime](https://github.com/uber-go/guide/blob/master/style.md#dont-fire-and-forget-goroutines).

- Stop a failed test with t.Fatal or t.FailNow instead of panic. — [Uber: Don't Panic](https://github.com/uber-go/guide/blob/master/style.md#dont-panic). <!-- uber-go-style:52 -->
- Extract fallible application flow into a testable helper returning an error or exit status. — [Uber: Exit Once](https://github.com/uber-go/guide/blob/master/style.md#exit-once). <!-- uber-go-style:69 -->
- A table row with at most three fields may use positional initialization. — [Uber: Use Field Names to Initialize Structs](https://github.com/uber-go/guide/blob/master/style.md#use-field-names-to-initialize-structs). <!-- uber-go-style:141 -->
- Use tables and subtests for multiple input/output scenarios with common validation. — [Uber: Test Tables](https://github.com/uber-go/guide/blob/master/style.md#test-tables). <!-- uber-go-style:152 -->
- Treat assertion-library selection as unspecified by the Test Tables prose; its illustrated library use is not a mandate. — [Uber: Test Tables](https://github.com/uber-go/guide/blob/master/style.md#test-tables). <!-- uber-go-style:155 -->
- Split tables into simpler tables or standalone tests when row handling needs complicated branches. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:156 -->
- Keep each test table focused on a small behavioral area. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:157 -->
- Avoid long chains of assertions that depend on previous assertions succeeding. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:158 -->
- Aim for every row to use all fields and run the same validation. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:159 -->
- A simple branch separating successful and failing cases can remain in a table. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:160 -->
- Keep otherwise comparable input variants together when that makes their differences clear. — [Uber: Avoid Unnecessary Complexity in Table Tests](https://github.com/uber-go/guide/blob/master/style.md#avoid-unnecessary-complexity-in-table-tests). <!-- uber-go-style:161 -->
- Give parallel subtests distinct iteration values; rebind captured loop variables for pre-Go-1.22 semantics or reused variables, while Go 1.22+ range-declared variables already have per-iteration scope. — [Uber: Parallel Tests](https://github.com/uber-go/guide/blob/master/style.md#parallel-tests). <!-- uber-go-style:162 -->

## Concurrency and performance

- Uber recommends `go.uber.org/atomic` to avoid untyped atomic access. Version note: Go 1.19+ also supplies typed `sync/atomic` values; choose deliberately when applying the source to newer Go. — [Uber — atomic types](https://github.com/uber-go/guide/blob/master/style.md#use-gouberorgatomic).

- Remove defer for speed only when measurements show its small overhead matters on the actual hot path. — [Uber: Defer to Clean Up](https://github.com/uber-go/guide/blob/master/style.md#defer-to-clean-up). <!-- uber-go-style:17 -->
- Default channel buffering to zero or one slot. — [Uber: Channel Size is One or None](https://github.com/uber-go/guide/blob/master/style.md#channel-size-is-one-or-none). <!-- uber-go-style:18 -->
- Justify larger channel buffers by their capacity, full-buffer behavior, and operation under load. — [Uber: Channel Size is One or None](https://github.com/uber-go/guide/blob/master/style.md#channel-size-is-one-or-none). <!-- uber-go-style:19 -->
- Ensure production goroutines do not leak. — [Uber: Don't fire-and-forget goroutines](https://github.com/uber-go/guide/blob/master/style.md#dont-fire-and-forget-goroutines). <!-- uber-go-style:72 -->
- Give each goroutine a known completion condition or a signal that requests shutdown. — [Uber: Don't fire-and-forget goroutines](https://github.com/uber-go/guide/blob/master/style.md#dont-fire-and-forget-goroutines). <!-- uber-go-style:74 -->
- Make it possible to wait for all goroutines started by an operation. — [Uber: Don't fire-and-forget goroutines](https://github.com/uber-go/guide/blob/master/style.md#dont-fire-and-forget-goroutines). <!-- uber-go-style:75 -->
- Wait for several goroutines with a WaitGroup. — [Uber: Wait for goroutines to exit](https://github.com/uber-go/guide/blob/master/style.md#wait-for-goroutines-to-exit). <!-- uber-go-style:76 -->
- Use a completion channel when waiting for a single worker is sufficient. — [Uber: Wait for goroutines to exit](https://github.com/uber-go/guide/blob/master/style.md#wait-for-goroutines-to-exit). <!-- uber-go-style:77 -->
- Put background work behind an owner with explicit startup and shutdown methods. — [Uber: No goroutines in init](https://github.com/uber-go/guide/blob/master/style.md#no-goroutines-in-init). <!-- uber-go-style:79 -->
- Have shutdown both request termination and wait until the worker has stopped. — [Uber: No goroutines in init](https://github.com/uber-go/guide/blob/master/style.md#no-goroutines-in-init). <!-- uber-go-style:80 -->
- Apply hot-path performance advice where execution cost matters rather than throughout the code indiscriminately. — [Uber: Performance](https://github.com/uber-go/guide/blob/master/style.md#performance). <!-- uber-go-style:81 -->
- Prefer strconv for conversions between strings and primitive values on hot paths. — [Uber: Prefer strconv over fmt](https://github.com/uber-go/guide/blob/master/style.md#prefer-strconv-over-fmt). <!-- uber-go-style:82 -->
- Cache a fixed string's byte conversion when a hot path would otherwise repeat it. — [Uber: Avoid repeated string-to-byte conversions](https://github.com/uber-go/guide/blob/master/style.md#avoid-repeated-string-to-byte-conversions). <!-- uber-go-style:83 -->
- Supply a known map capacity hint to reduce growth on a hot path. — [Uber: Specifying Map Capacity Hints](https://github.com/uber-go/guide/blob/master/style.md#specifying-map-capacity-hints). <!-- uber-go-style:84 -->
- Treat map capacity as a hint, not a guarantee of allocation-free insertion. — [Uber: Specifying Map Capacity Hints](https://github.com/uber-go/guide/blob/master/style.md#specifying-map-capacity-hints). <!-- uber-go-style:85 -->
- Preallocate known slice capacity, particularly for repeated append operations on hot paths. — [Uber: Specifying Slice Capacity](https://github.com/uber-go/guide/blob/master/style.md#specifying-slice-capacity). <!-- uber-go-style:86 -->
- Include a known size hint when creating a map. — [Uber: Initializing Maps](https://github.com/uber-go/guide/blob/master/style.md#initializing-maps). <!-- uber-go-style:147 -->

## Language-specific pitfalls

- Register resource closure and mutex unlocking with defer. — [Uber: Defer to Clean Up](https://github.com/uber-go/guide/blob/master/style.md#defer-to-clean-up). <!-- uber-go-style:16 -->
- Allow for the time package's omission of leap seconds when the application depends on them. — [Uber: Use time.Time and time.Duration with external systems](https://github.com/uber-go/guide/blob/master/style.md#use-timetime-and-timeduration-with-external-systems). <!-- uber-go-style:29 -->
- Prefer explicit startup functions to init. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:59 -->
- Keep necessary init work reproducible across environments and executions. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:60 -->
- Do not make init depend on another initializer's order or effects. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:61 -->
- Avoid inspecting or changing process, host, environment, directory, or argument state inside init. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:62 -->
- Keep system I/O, including file and network access, out of init. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:63 -->
- Move setup that needs those effects into main or another explicit lifecycle phase. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:64 -->
- Complex static initialization, registration, or deterministic precomputation may warrant init. — [Uber: Avoid init](https://github.com/uber-go/guide/blob/master/style.md#avoid-init). <!-- uber-go-style:65 -->
- Do not launch goroutines during init. — [Uber: No goroutines in init](https://github.com/uber-go/guide/blob/master/style.md#no-goroutines-in-init). <!-- uber-go-style:78 -->
- Favor consistent choices when context leaves several acceptable styles. — [Uber: Be Consistent](https://github.com/uber-go/guide/blob/master/style.md#be-consistent). <!-- uber-go-style:89 -->
- Consider assigning a default first and overriding it in one if instead of assigning in both branches. — [Uber: Unnecessary Else](https://github.com/uber-go/guide/blob/master/style.md#unnecessary-else). <!-- uber-go-style:109 -->
- Limit variables and constants to the smallest useful scope. — [Uber: Reduce Scope of Variables](https://github.com/uber-go/guide/blob/master/style.md#reduce-scope-of-variables). <!-- uber-go-style:133 -->
- Do not introduce extra nesting just to narrow a declaration's scope. — [Uber: Reduce Scope of Variables](https://github.com/uber-go/guide/blob/master/style.md#reduce-scope-of-variables). <!-- uber-go-style:134 -->
- Declare a result outside an if initializer when later code also uses it. — [Uber: Reduce Scope of Variables](https://github.com/uber-go/guide/blob/master/style.md#reduce-scope-of-variables). <!-- uber-go-style:135 -->

## Where the sources disagree

Within Uber's guide, follow [Linting](https://github.com/uber-go/guide/blob/master/style.md#linting) over the stale introduction for golint versus revive. Its [Parallel Tests](https://github.com/uber-go/guide/blob/master/style.md#parallel-tests) warning needs the [Go 1.22 language change](https://go.dev/doc/go1.22#language) qualifier shown above; this is an identified version clarification, not wording from Uber.

## Worked examples

Read [original worked examples and their source tags](examples.md) for small applications of this guide.
