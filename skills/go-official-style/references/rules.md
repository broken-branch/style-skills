# Effective Go: condensed rules

Effective Go is a historical core-language guide, not a complete account of current Go. Apply its interface-only abstraction advice only when the implementation will expose no additional methods.

Source owner: The Go Authors. License: [CC-BY-4.0](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

## Tooling

- Let gofmt determine formatting; reshape awkward code rather than overriding its output. — [Effective Go: Formatting](https://go.dev/doc/effective_go#formatting). <!-- effective-go:3 -->
- Indent with tabs, using spaces only where needed. — [Effective Go: Formatting](https://go.dev/doc/effective_go#formatting). <!-- effective-go:4 -->
- Leave source width unrestricted by a fixed column count. — [Effective Go: Formatting](https://go.dev/doc/effective_go#formatting). <!-- effective-go:5 -->
- Wrap an unreadably long line and indent its continuation one tab further. — [Effective Go: Formatting](https://go.dev/doc/effective_go#formatting). <!-- effective-go:6 -->
- Write semicolons only where Go syntax needs an explicit separator. — [Effective Go: Semicolons](https://go.dev/doc/effective_go#semicolons). <!-- effective-go:24 -->
- Place a control construct's opening brace on its header line. — [Effective Go: Semicolons](https://go.dev/doc/effective_go#semicolons). <!-- effective-go:25 -->

## Naming

- Choose a brief, descriptive package name consisting of one lowercase word. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:11 -->
- Keep package names free of underscores and interior capitals. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:12 -->
- Let the package qualifier supply context instead of repeating it in exported names. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:14 -->
- Call the constructor New when its package already names the single exported type. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:15 -->
- Use documentation to explain a concise identifier instead of lengthening it excessively. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:17 -->
- Name ordinary getters without a Get prefix. — [Effective Go: Getters](https://go.dev/doc/effective_go#Getters). <!-- effective-go:18 -->
- Name accessors for their property; prefix a corresponding mutator with Set when one is needed. — [Effective Go: Getters](https://go.dev/doc/effective_go#Getters). <!-- effective-go:19 -->
- Derive a single-method interface's name from the action it performs, commonly with an -er suffix. — [Effective Go: Interface names](https://go.dev/doc/effective_go#interface-names). <!-- effective-go:20 -->
- Reserve conventional method names for their customary contracts and signatures. — [Effective Go: Interface names](https://go.dev/doc/effective_go#interface-names). <!-- effective-go:21 -->
- Adopt the conventional method spelling and signature when implementing its established contract. — [Effective Go: Interface names](https://go.dev/doc/effective_go#interface-names). <!-- effective-go:22 -->
- Join identifier words with mixed capitalization instead of underscores. — [Effective Go: MixedCaps](https://go.dev/doc/effective_go#mixed-caps). <!-- effective-go:23 -->
- Rebinding the original name in a type switch is acceptable when the case-specific value reads more clearly. — [Effective Go: Type switch](https://go.dev/doc/effective_go#type_switch). <!-- effective-go:36 -->
- Name return values when that disambiguates their roles or improves the API documentation. — [Effective Go: Named result parameters](https://go.dev/doc/effective_go#named-results). <!-- effective-go:39 -->

## Files and layout

- Usually match the package name to the directory's last path element. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:13 -->
- Avoid dot imports apart from the external-test case explained in the review guidance. — [Effective Go: Package names](https://go.dev/doc/effective_go#package-names). <!-- effective-go:16 -->
- Place temporary package-silencing declarations just below imports and mark them for later removal. — [Effective Go: Unused imports and variables](https://go.dev/doc/effective_go#blank_unused). <!-- effective-go:82 -->
- Remove unused imports or put them to real use before leaving development scaffolding behind. — [Effective Go: Unused imports and variables](https://go.dev/doc/effective_go#blank_unused). <!-- effective-go:83 -->
- Mark an import with _ when its initialization side effects are its only purpose. — [Effective Go: Import for side effect](https://go.dev/doc/effective_go#blank_import). <!-- effective-go:84 -->

## Types and data

- Return several results directly instead of filling caller-provided output pointers. — [Effective Go: Multiple return values](https://go.dev/doc/effective_go#multiple-returns). <!-- effective-go:38 -->
- Make the zero-initialized form of a type useful wherever feasible. — [Effective Go: Allocation with new](https://go.dev/doc/effective_go#allocation_new). <!-- effective-go:45 -->
- Provide a constructor when the required initial state cannot be represented by a usable zero value. — [Effective Go: Constructors and composite literals](https://go.dev/doc/effective_go#composite_literals). <!-- effective-go:46 -->
- Prefer a composite literal over a sequence of individual field assignments. — [Effective Go: Constructors and composite literals](https://go.dev/doc/effective_go#composite_literals). <!-- effective-go:47 -->
- Use field keys when selective or reordered struct initialization helps. — [Effective Go: Constructors and composite literals](https://go.dev/doc/effective_go#composite_literals). <!-- effective-go:48 -->
- Returning a pointer to a local value or composite literal is a valid allocation technique. — [Effective Go: Constructors and composite literals](https://go.dev/doc/effective_go#composite_literals). <!-- effective-go:49 -->
- Initialize slices, channels, and maps with make when needed; its result is the initialized value. — [Effective Go: Allocation with make](https://go.dev/doc/effective_go#allocation_make). <!-- effective-go:50 -->
- Favor slices; use arrays for fixed dimensions or layout requirements rather than routinely passing array pointers. — [Effective Go: Arrays](https://go.dev/doc/effective_go#arrays). <!-- effective-go:51 -->
- Pass buffer access as a slice so its bounds travel with its elements. — [Effective Go: Slices](https://go.dev/doc/effective_go#slices). <!-- effective-go:52 -->
- Propagate a changed slice descriptor after growth or reallocation. — [Effective Go: Slices](https://go.dev/doc/effective_go#slices). <!-- effective-go:53 -->
- Allocate each row separately when a two-dimensional slice needs independently resizable rows. — [Effective Go: Two-dimensional slices](https://go.dev/doc/effective_go#two_dimensional_slices). <!-- effective-go:54 -->
- Rows may share one backing allocation when growth cannot spill into neighboring rows. — [Effective Go: Two-dimensional slices](https://go.dev/doc/effective_go#two_dimensional_slices). <!-- effective-go:55 -->
- A map of booleans is a reasonable representation for a simple set. — [Effective Go: Maps](https://go.dev/doc/effective_go#maps). <!-- effective-go:56 -->
- Use the lookup's boolean result when absence differs from a stored zero value. — [Effective Go: Maps](https://go.dev/doc/effective_go#maps). <!-- effective-go:57 -->
- Ignore the map value with _ for membership-only lookups. — [Effective Go: Maps](https://go.dev/doc/effective_go#maps). <!-- effective-go:58 -->
- Delete map entries directly; deleting an absent key needs no guard. — [Effective Go: Maps](https://go.dev/doc/effective_go#maps). <!-- effective-go:59 -->
- Implement String() string to customize a type's usual textual representation. — [Effective Go: Printing](https://go.dev/doc/effective_go#printing). <!-- effective-go:61 -->
- Retain append's result because growth can replace the backing storage. — [Effective Go: Append](https://go.dev/doc/effective_go#append). <!-- effective-go:65 -->
- Expand the source slice with ... to append its elements individually. — [Effective Go: Append](https://go.dev/doc/effective_go#append). <!-- effective-go:66 -->
- Represent suitable enumerations with iota and grouped constant expressions. — [Effective Go: Constants](https://go.dev/doc/effective_go#constants). <!-- effective-go:67 -->
- Give a named scalar type a formatting method when a unit-aware representation aids readability. — [Effective Go: Constants](https://go.dev/doc/effective_go#constants). <!-- effective-go:68 -->
- Choose a pointer receiver when changing or replacing the receiver value. — [Effective Go: Pointers vs. Values](https://go.dev/doc/effective_go#pointers_vs_values). <!-- effective-go:70 -->
- Use an established method signature when it enables a useful standard interface. — [Effective Go: Pointers vs. Values](https://go.dev/doc/effective_go#pointers_vs_values). <!-- effective-go:71 -->
- Describe a caller's required behavior with a narrowly scoped interface. — [Effective Go: Interfaces](https://go.dev/doc/effective_go#interfaces). <!-- effective-go:72 -->
- Convert to a compatible type to reuse its methods instead of duplicating their implementation. — [Effective Go: Conversions](https://go.dev/doc/effective_go#conversions). <!-- effective-go:73 -->
- Prefer hiding a concrete type when it exists only to implement an interface and will never expose methods beyond that contract. — [Effective Go: Generality](https://go.dev/doc/effective_go#generality). <!-- effective-go:75 -->
- In that interface-only case, prefer an interface-returning constructor so implementations can be exchanged locally. — [Effective Go: Generality](https://go.dev/doc/effective_go#generality). <!-- effective-go:76 -->
- Adapt a function to an interface through a named function type and a forwarding method. — [Effective Go: Interfaces and methods](https://go.dev/doc/effective_go#interface_methods). <!-- effective-go:78 -->
- Add a compile-time blank assignment when a required interface implementation has no other static check. — [Effective Go: Interface checks](https://go.dev/doc/effective_go#blank_implements). <!-- effective-go:85 -->
- Skip redundant interface assertions when ordinary conversions already verify implementation. — [Effective Go: Interface checks](https://go.dev/doc/effective_go#blank_implements). <!-- effective-go:86 -->
- Build composite interfaces by embedding existing ones rather than duplicating their methods. — [Effective Go: Embedding](https://go.dev/doc/effective_go#embedding). <!-- effective-go:87 -->
- Struct embedding can expose an inner type's methods for reuse. — [Effective Go: Embedding](https://go.dev/doc/effective_go#embedding). <!-- effective-go:88 -->
- Embedding can offer convenient access to another component's methods. — [Effective Go: Embedding](https://go.dev/doc/effective_go#embedding). <!-- effective-go:90 -->

## Errors

- Check failures along the way and let successful execution proceed straight downward. — [Effective Go: If](https://go.dev/doc/effective_go#if). <!-- effective-go:28 -->
- Report failure or status separately from a useful function result. — [Effective Go: Multiple return values](https://go.dev/doc/effective_go#multiple-returns). <!-- effective-go:37 -->
- Use the two-result type assertion when a dynamic-type mismatch must be handled. — [Effective Go: Interface conversions and type assertions](https://go.dev/doc/effective_go#interface_conversions). <!-- effective-go:74 -->
- Examine error results rather than throwing them away with _. — [Effective Go: The blank identifier in multiple assignment](https://go.dev/doc/effective_go#blank_assign). <!-- effective-go:80 -->
- Return informative errors alongside normal results when an operation fails. — [Effective Go: Errors](https://go.dev/doc/effective_go#errors). <!-- effective-go:102 -->
- Include the responsible package or operation in error messages when useful. — [Effective Go: Errors](https://go.dev/doc/effective_go#errors). <!-- effective-go:103 -->
- Provide structured error information when callers must identify recoverable cases. — [Effective Go: Errors](https://go.dev/doc/effective_go#errors). <!-- effective-go:104 -->
- Represent routine failure with an error return. — [Effective Go: Panic](https://go.dev/doc/effective_go#panic). <!-- effective-go:105 -->
- Libraries should return a recoverable failure instead of panicking when callers could respond to it. — [Effective Go: Panic](https://go.dev/doc/effective_go#panic). <!-- effective-go:106 -->
- Panic may indicate an impossible condition or initialization failure that makes a library unusable. — [Effective Go: Panic](https://go.dev/doc/effective_go#panic). <!-- effective-go:107 -->
- Call recover directly from the function registered with defer. — [Effective Go: Recover](https://go.dev/doc/effective_go#recover). <!-- effective-go:108 -->
- A server may recover inside a worker goroutine to isolate its failure. — [Effective Go: Recover](https://go.dev/doc/effective_go#recover). <!-- effective-go:109 -->
- A parser may carry a private panic internally and convert it to an error at its public boundary. — [Effective Go: Recover](https://go.dev/doc/effective_go#recover). <!-- effective-go:110 -->
- Recover only the intended private panic type and re-panic unrelated failures. — [Effective Go: Recover](https://go.dev/doc/effective_go#recover). <!-- effective-go:111 -->

## Comments and docs

- Default to line comments introduced by //. — [Effective Go: Commentary](https://go.dev/doc/effective_go#commentary). <!-- effective-go:8 -->
- Choose block comments for package prose, comments embedded in expressions, or temporarily disabled regions when useful. — [Effective Go: Commentary](https://go.dev/doc/effective_go#commentary). <!-- effective-go:9 -->
- Attach documentation immediately above its declaration, with no intervening empty line. — [Effective Go: Commentary](https://go.dev/doc/effective_go#commentary). <!-- effective-go:10 -->

## Concurrency and performance

- Synchronize access to server state shared by concurrent operations. — [Effective Go: Interfaces and methods](https://go.dev/doc/effective_go#interface_methods). <!-- effective-go:77 -->
- Prefer channel-based ownership transfer when it makes shared-state coordination easier to reason about. — [Effective Go: Share by communicating](https://go.dev/doc/effective_go#sharing). <!-- effective-go:91 -->
- Choose a mutex when direct locking better suits the state being protected. — [Effective Go: Share by communicating](https://go.dev/doc/effective_go#sharing). <!-- effective-go:92 -->
- Provide a completion notification when other code must wait for background work. — [Effective Go: Goroutines](https://go.dev/doc/effective_go#goroutines). <!-- effective-go:93 -->
- Use an unbuffered channel when a handoff should also synchronize sender and receiver. — [Effective Go: Channels](https://go.dev/doc/effective_go#channels). <!-- effective-go:94 -->
- A buffered channel may serve as a concurrency-limiting semaphore. — [Effective Go: Channels](https://go.dev/doc/effective_go#channels). <!-- effective-go:95 -->
- Bound goroutine creation with admission control or a fixed-size worker pool. — [Effective Go: Channels](https://go.dev/doc/effective_go#channels). <!-- effective-go:96 -->
- Give concurrent requests separate reply channels when independent responses are needed. — [Effective Go: Channels of channels](https://go.dev/doc/effective_go#chan_of_chan). <!-- effective-go:97 -->
- Parallelize independent pieces and wait for all required pieces to finish. — [Effective Go: Parallelization](https://go.dev/doc/effective_go#parallel). <!-- effective-go:98 -->
- Size parallel work with the user's GOMAXPROCS choice in mind. — [Effective Go: Parallelization](https://go.dev/doc/effective_go#parallel). <!-- effective-go:99 -->
- Distinguish coordinating concurrent work from actually executing on multiple CPUs. — [Effective Go: Parallelization](https://go.dev/doc/effective_go#parallel). <!-- effective-go:100 -->
- A bounded channel free list with nonblocking access can recycle buffers without retaining an unlimited surplus. — [Effective Go: A leaky buffer](https://go.dev/doc/effective_go#leaky_buffer). <!-- effective-go:101 -->

## Security

- Render HTML through a context-aware template engine that escapes inserted values. — [Effective Go: A web server](https://go.dev/doc/effective_go#web_server). <!-- effective-go:112 -->

## Language-specific pitfalls

- Choose idiomatic Go designs instead of transplanting another language's object model. — [Effective Go: Introduction](https://go.dev/doc/effective_go#introduction). <!-- effective-go:1 -->
- Consult standard-library implementations, docs, and executable examples when selecting Go idioms. — [Effective Go: Introduction](https://go.dev/doc/effective_go#introduction). <!-- effective-go:2 -->
- Remove parentheses that add nothing around conditions or simple expressions. — [Effective Go: Formatting](https://go.dev/doc/effective_go#formatting). <!-- effective-go:7 -->
- Expand even small if bodies over multiple lines, particularly terminating branches. — [Effective Go: If](https://go.dev/doc/effective_go#if). <!-- effective-go:26 -->
- Remove else when the preceding branch cannot reach the following code. — [Effective Go: If](https://go.dev/doc/effective_go#if). <!-- effective-go:27 -->
- Traverse a collection or channel with range when it describes the intended iteration. — [Effective Go: For](https://go.dev/doc/effective_go#for). <!-- effective-go:29 -->
- Declare only the first range variable when the index or key is sufficient. — [Effective Go: For](https://go.dev/doc/effective_go#for). <!-- effective-go:30 -->
- Discard the first range result with _ when consuming only values. — [Effective Go: For](https://go.dev/doc/effective_go#for). <!-- effective-go:31 -->
- Advance related loop variables with one parallel assignment. — [Effective Go: For](https://go.dev/doc/effective_go#for). <!-- effective-go:32 -->
- Consider a switch without an expression for successive boolean tests. — [Effective Go: Switch](https://go.dev/doc/effective_go#switch). <!-- effective-go:33 -->
- List equivalent switch alternatives together in one comma-separated case. — [Effective Go: Switch](https://go.dev/doc/effective_go#switch). <!-- effective-go:34 -->
- Label a break when it must leave an outer loop rather than the enclosing switch. — [Effective Go: Switch](https://go.dev/doc/effective_go#switch). <!-- effective-go:35 -->
- A short, clear function may use a bare return with named results. — [Effective Go: Named result parameters](https://go.dev/doc/effective_go#named-results). <!-- effective-go:40 -->
- Use defer for cleanup that must run whichever return path is taken. — [Effective Go: Defer](https://go.dev/doc/effective_go#defer). <!-- effective-go:41 -->
- Register cleanup near the corresponding resource acquisition. — [Effective Go: Defer](https://go.dev/doc/effective_go#defer). <!-- effective-go:42 -->
- Remember that deferred arguments are captured when execution reaches defer. — [Effective Go: Defer](https://go.dev/doc/effective_go#defer). <!-- effective-go:43 -->
- Plan for defers to execute last-in-first-out at function return, not at block completion. — [Effective Go: Defer](https://go.dev/doc/effective_go#defer). <!-- effective-go:44 -->
- Choose an unformatted fmt print operation when interpolation is unnecessary. — [Effective Go: Printing](https://go.dev/doc/effective_go#printing). <!-- effective-go:60 -->
- Keep String from invoking itself again through formatting of its receiver. — [Effective Go: Printing](https://go.dev/doc/effective_go#printing). <!-- effective-go:62 -->
- Break recursive formatting with conversion to a method-free underlying type or an appropriate non-string format verb. — [Effective Go: Printing](https://go.dev/doc/effective_go#printing). <!-- effective-go:63 -->
- Expand a variadic argument slice with ... when forwarding its individual arguments. — [Effective Go: Printing](https://go.dev/doc/effective_go#printing). <!-- effective-go:64 -->
- Use init for declaration-inexpressible setup or state validation needed before normal execution. — [Effective Go: The init function](https://go.dev/doc/effective_go#init). <!-- effective-go:69 -->
- Discard an irrelevant assignment result with _ instead of creating a placeholder variable. — [Effective Go: The blank identifier in multiple assignment](https://go.dev/doc/effective_go#blank_assign). <!-- effective-go:79 -->
- Use blank assignments that suppress unused-value diagnostics only while developing. — [Effective Go: Unused imports and variables](https://go.dev/doc/effective_go#blank_unused). <!-- effective-go:81 -->
- Initialize an embedded pointer before invoking methods that require a non-nil receiver. — [Effective Go: Embedding](https://go.dev/doc/effective_go#embedding). <!-- effective-go:89 -->

## Original worked examples

Original code under this skill's license: [interface-only construction](examples/run_reader.go), [partial reads and EOF](examples/run_reader_test.go), [standard-interface composition](examples/example_test.go).
