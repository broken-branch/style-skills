# Go Code Review Comments: condensed rules

Apply Code Review Comments within each rule’s stated scope, including consumer-owned interfaces and concrete producer results.

Source owner: The Go Authors and Go Wiki contributors. License: [CC-BY-4.0](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

## Tooling

- Apply gofmt to Go files. — [Go Code Review Comments: Gofmt](https://go.dev/wiki/CodeReviewComments#gofmt). <!-- code-review-comments:1 -->
- goimports may replace a plain gofmt run when import maintenance is also desired. — [Go Code Review Comments: Gofmt](https://go.dev/wiki/CodeReviewComments#gofmt). <!-- code-review-comments:2 -->
- Do not enforce a fixed source column limit. — [Go Code Review Comments: Line Length](https://go.dev/wiki/CodeReviewComments#line-length). <!-- code-review-comments:54 -->
- Avoid unwieldy lines while retaining long expressions that remain naturally readable. — [Go Code Review Comments: Line Length](https://go.dev/wiki/CodeReviewComments#line-length). <!-- code-review-comments:55 -->

## Naming

- Capitalize each initialism consistently as a unit. — [Go Code Review Comments: Initialisms](https://go.dev/wiki/CodeReviewComments#initialisms). <!-- code-review-comments:46 -->
- Spell an identifier abbreviation as ID, not Id. — [Go Code Review Comments: Initialisms](https://go.dev/wiki/CodeReviewComments#initialisms). <!-- code-review-comments:47 -->
- Do not force initialism spelling changes onto generated protocol-buffer names. — [Go Code Review Comments: Initialisms](https://go.dev/wiki/CodeReviewComments#initialisms). <!-- code-review-comments:48 -->
- Use mixed capitalization even for constants, beginning unexported names with lowercase. — [Go Code Review Comments: Mixed Caps](https://go.dev/wiki/CodeReviewComments#mixed-caps). <!-- code-review-comments:58 -->
- Name results when their documented roles would otherwise be unclear, particularly for repeated types. — [Go Code Review Comments: Named Result Parameters](https://go.dev/wiki/CodeReviewComments#named-result-parameters). <!-- code-review-comments:59 -->
- Omit return names that simply repeat the function's name or result type. — [Go Code Review Comments: Named Result Parameters](https://go.dev/wiki/CodeReviewComments#named-result-parameters). <!-- code-review-comments:60 -->
- Do not introduce result names just to eliminate local declarations. — [Go Code Review Comments: Named Result Parameters](https://go.dev/wiki/CodeReviewComments#named-result-parameters). <!-- code-review-comments:61 -->
- Avoid duplicating a package qualifier in the names it exports. — [Go Code Review Comments: Package Names](https://go.dev/wiki/CodeReviewComments#package-names). <!-- code-review-comments:67 -->
- Name packages for their responsibility rather than a vague catch-all category. — [Go Code Review Comments: Package Names](https://go.dev/wiki/CodeReviewComments#package-names). <!-- code-review-comments:68 -->
- Choose a compact receiver identifier derived from its type. — [Go Code Review Comments: Receiver Names](https://go.dev/wiki/CodeReviewComments#receiver-names). <!-- code-review-comments:72 -->
- Avoid generic receiver names such as self or this. — [Go Code Review Comments: Receiver Names](https://go.dev/wiki/CodeReviewComments#receiver-names). <!-- code-review-comments:73 -->
- Use one receiver name consistently across methods of the same type. — [Go Code Review Comments: Receiver Names](https://go.dev/wiki/CodeReviewComments#receiver-names). <!-- code-review-comments:74 -->
- Keep local variable identifiers brief where their role is apparent. — [Go Code Review Comments: Variable Names](https://go.dev/wiki/CodeReviewComments#variable-names). <!-- code-review-comments:91 -->
- Use more descriptive names as declaration and use become farther apart. — [Go Code Review Comments: Variable Names](https://go.dev/wiki/CodeReviewComments#variable-names). <!-- code-review-comments:92 -->
- Use conventional short names for obvious, short-lived roles. — [Go Code Review Comments: Variable Names](https://go.dev/wiki/CodeReviewComments#variable-names). <!-- code-review-comments:93 -->
- Give globals and unusual values names that explain their purpose. — [Go Code Review Comments: Variable Names](https://go.dev/wiki/CodeReviewComments#variable-names). <!-- code-review-comments:94 -->

## Files and layout

- Keep an import's declared name unless a collision requires renaming. — [Go Code Review Comments: Imports](https://go.dev/wiki/CodeReviewComments#imports). <!-- code-review-comments:33 -->
- Resolve collisions by renaming the package most specific to the current project where possible. — [Go Code Review Comments: Imports](https://go.dev/wiki/CodeReviewComments#imports). <!-- code-review-comments:34 -->
- Divide import groups with empty lines. — [Go Code Review Comments: Imports](https://go.dev/wiki/CodeReviewComments#imports). <!-- code-review-comments:35 -->
- List standard-library imports before other groups. — [Go Code Review Comments: Imports](https://go.dev/wiki/CodeReviewComments#imports). <!-- code-review-comments:36 -->
- Keep blank imports in main or in tests needing their initialization effects. — [Go Code Review Comments: Import Blank](https://go.dev/wiki/CodeReviewComments#import-blank). <!-- code-review-comments:37 -->
- Avoid bringing imported names into ordinary package scope with dot imports. — [Go Code Review Comments: Import Dot](https://go.dev/wiki/CodeReviewComments#import-dot). <!-- code-review-comments:38 -->
- An external test package required to avoid an import cycle may dot-import its subject package. — [Go Code Review Comments: Import Dot](https://go.dev/wiki/CodeReviewComments#import-dot). <!-- code-review-comments:39 -->

## Types and data

- Thread the caller's context explicitly through request-handling calls. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:5 -->
- Place a context argument first in the usual function signature. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:6 -->
- Accept the request's existing context instead of starting a background context inside its processing. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:7 -->
- Pass contexts to the methods that need them instead of retaining them in structs. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:8 -->
- A context field can be necessary when implementing an unchangeable external or standard-library interface. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:9 -->
- Accept context.Context itself rather than inventing a replacement context abstraction. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:10 -->
- Keep ordinary parameters out of context values; reserve values for appropriate request metadata. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:11 -->
- An immutable context may be shared by calls with the same deadline, cancellation, and request information. — [Go Code Review Comments: Contexts](https://go.dev/wiki/CodeReviewComments#contexts). <!-- code-review-comments:12 -->
- Before copying a foreign struct, check whether its internals alias shared state. — [Go Code Review Comments: Copying](https://go.dev/wiki/CodeReviewComments#copying). <!-- code-review-comments:13 -->
- Usually avoid copying objects operated on through pointer receivers. — [Go Code Review Comments: Copying](https://go.dev/wiki/CodeReviewComments#copying). <!-- code-review-comments:14 -->
- Declare an empty slice with var unless a non-nil value is needed. — [Go Code Review Comments: Declaring Empty Slices](https://go.dev/wiki/CodeReviewComments#declaring-empty-slices). <!-- code-review-comments:18 -->
- Allocate an empty non-nil slice when an observable contract, such as serialization, requires it. — [Go Code Review Comments: Declaring Empty Slices](https://go.dev/wiki/CodeReviewComments#declaring-empty-slices). <!-- code-review-comments:19 -->
- Design APIs so nil and other empty slices normally mean the same thing. — [Go Code Review Comments: Declaring Empty Slices](https://go.dev/wiki/CodeReviewComments#declaring-empty-slices). <!-- code-review-comments:20 -->
- Define interfaces where their behavior is consumed instead of automatically beside the implementation. — [Go Code Review Comments: Interfaces](https://go.dev/wiki/CodeReviewComments#interfaces). <!-- code-review-comments:49 -->
- Default to concrete producer return types so adding methods does not require widening an implementation-owned interface. — [Go Code Review Comments: Interfaces](https://go.dev/wiki/CodeReviewComments#interfaces). <!-- code-review-comments:50 -->
- Wait for a real consumer's requirements before introducing an interface. — [Go Code Review Comments: Interfaces](https://go.dev/wiki/CodeReviewComments#interfaces). <!-- code-review-comments:52 -->
- Name a result when a deferred closure must modify it. — [Go Code Review Comments: Named Result Parameters](https://go.dev/wiki/CodeReviewComments#named-result-parameters). <!-- code-review-comments:63 -->
- Do not introduce a read-only pointer parameter solely to avoid copying a few bytes. — [Go Code Review Comments: Pass Values](https://go.dev/wiki/CodeReviewComments#pass-values). <!-- code-review-comments:69 -->
- Normally pass string and interface descriptors by value. — [Go Code Review Comments: Pass Values](https://go.dev/wiki/CodeReviewComments#pass-values). <!-- code-review-comments:70 -->
- A pointer can suit a struct that is already large or likely to grow. — [Go Code Review Comments: Pass Values](https://go.dev/wiki/CodeReviewComments#pass-values). <!-- code-review-comments:71 -->
- Use value receivers for maps, functions, channels, and slices unless a slice method must replace its descriptor. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:75 -->
- Use a pointer receiver for methods that change receiver state. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:76 -->
- Keep a struct with a mutex or other noncopyable synchronization state behind pointer receivers. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:77 -->
- Prefer pointer receivers for large array or struct values. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:78 -->
- Use a pointer when the method must observe changes to its receiver made concurrently or by nested calls. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:79 -->
- Prefer a pointer receiver when referenced mutable data makes value-like semantics misleading. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:80 -->
- Small immutable structs, arrays, and scalar values can reasonably use value receivers. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:81 -->
- Keep receiver kinds consistent throughout a type's method set. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:83 -->
- If receiver choice remains uncertain, choose a pointer. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:84 -->

## Errors

- Return ordinary failures through error results rather than panic. — [Go Code Review Comments: Don't Panic](https://go.dev/wiki/CodeReviewComments#dont-panic). <!-- code-review-comments:23 -->
- Use lowercase error text except where a name or acronym warrants capitalization. — [Go Code Review Comments: Error Strings](https://go.dev/wiki/CodeReviewComments#error-strings). <!-- code-review-comments:24 -->
- Omit final punctuation from errors that will be composed into larger messages. — [Go Code Review Comments: Error Strings](https://go.dev/wiki/CodeReviewComments#error-strings). <!-- code-review-comments:25 -->
- Whole log messages need not follow the capitalization and punctuation rules for composable errors. — [Go Code Review Comments: Error Strings](https://go.dev/wiki/CodeReviewComments#error-strings). <!-- code-review-comments:26 -->
- Inspect returned errors rather than assigning them to the blank identifier. — [Go Code Review Comments: Handle Errors](https://go.dev/wiki/CodeReviewComments#handle-errors). <!-- code-review-comments:31 -->
- Resolve a failure locally or propagate it; use panic only for exceptional situations. — [Go Code Review Comments: Handle Errors](https://go.dev/wiki/CodeReviewComments#handle-errors). <!-- code-review-comments:32 -->
- Exported functions should indicate invalid or absent results with a separate trailing error or boolean. — [Go Code Review Comments: In-Band Errors](https://go.dev/wiki/CodeReviewComments#in-band-errors). <!-- code-review-comments:40 -->
- Use separate status results for private helpers too when useful. — [Go Code Review Comments: In-Band Errors](https://go.dev/wiki/CodeReviewComments#in-band-errors). <!-- code-review-comments:41 -->
- An empty, nil, or zero result needs no separate failure marker when it is an ordinary acceptable result. — [Go Code Review Comments: In-Band Errors](https://go.dev/wiki/CodeReviewComments#in-band-errors). <!-- code-review-comments:42 -->
- Deal with failures first so successful execution stays minimally indented. — [Go Code Review Comments: Indent Error Flow](https://go.dev/wiki/CodeReviewComments#indent-error-flow). <!-- code-review-comments:43 -->

## Comments and docs

- Use full sentences for declaration documentation. — [Go Code Review Comments: Comment Sentences](https://go.dev/wiki/CodeReviewComments#comment-sentences). <!-- code-review-comments:3 -->
- Begin a declaration's doc sentence with its name and end it with a period. — [Go Code Review Comments: Comment Sentences](https://go.dev/wiki/CodeReviewComments#comment-sentences). <!-- code-review-comments:4 -->
- Supply documentation for all exported declarations at package scope. — [Go Code Review Comments: Doc Comments](https://go.dev/wiki/CodeReviewComments#doc-comments). <!-- code-review-comments:21 -->
- Explain private types and functions when their purpose or behavior needs clarification. — [Go Code Review Comments: Doc Comments](https://go.dev/wiki/CodeReviewComments#doc-comments). <!-- code-review-comments:22 -->
- Explain a goroutine's termination conditions when the structure alone does not reveal them. — [Go Code Review Comments: Goroutine Lifetimes](https://go.dev/wiki/CodeReviewComments#goroutine-lifetimes). <!-- code-review-comments:30 -->
- Place package documentation immediately before the package clause. — [Go Code Review Comments: Package Comments](https://go.dev/wiki/CodeReviewComments#package-comments). <!-- code-review-comments:64 -->
- For a command package, document the program with a natural sentence that includes its name. — [Go Code Review Comments: Package Comments](https://go.dev/wiki/CodeReviewComments#package-comments). <!-- code-review-comments:65 -->
- Start publicly displayed package prose with a capital, including a leading binary name. — [Go Code Review Comments: Package Comments](https://go.dev/wiki/CodeReviewComments#package-comments). <!-- code-review-comments:66 -->

## Testing

- A new package should include an executable usage example or test demonstrating a complete basic interaction. — [Go Code Review Comments: Examples](https://go.dev/wiki/CodeReviewComments#examples). <!-- code-review-comments:27 -->
- Do not add an interface to an implementation package solely for test mocks. — [Go Code Review Comments: Interfaces](https://go.dev/wiki/CodeReviewComments#interfaces). <!-- code-review-comments:51 -->
- Prefer exercising an implementation's public API in tests. — [Go Code Review Comments: Interfaces](https://go.dev/wiki/CodeReviewComments#interfaces). <!-- code-review-comments:53 -->
- Failure messages should identify the operation, inputs, observed output, and wanted output. — [Go Code Review Comments: Useful Test Failures](https://go.dev/wiki/CodeReviewComments#useful-test-failures). <!-- code-review-comments:87 -->
- Display the observed result before the expected result in diagnostics. — [Go Code Review Comments: Useful Test Failures](https://go.dev/wiki/CodeReviewComments#useful-test-failures). <!-- code-review-comments:88 -->
- Make helper failures understandable to someone who does not know the test's implementation. — [Go Code Review Comments: Useful Test Failures](https://go.dev/wiki/CodeReviewComments#useful-test-failures). <!-- code-review-comments:89 -->
- Use named cases or table entries when they make a failing scenario easier to locate. — [Go Code Review Comments: Useful Test Failures](https://go.dev/wiki/CodeReviewComments#useful-test-failures). <!-- code-review-comments:90 -->

## Concurrency and performance

- Make each goroutine's exit condition, or deliberate lifetime-long operation, evident. — [Go Code Review Comments: Goroutine Lifetimes](https://go.dev/wiki/CodeReviewComments#goroutine-lifetimes). <!-- code-review-comments:28 -->
- Prefer concurrency structures whose goroutine lifetimes can be understood directly. — [Go Code Review Comments: Goroutine Lifetimes](https://go.dev/wiki/CodeReviewComments#goroutine-lifetimes). <!-- code-review-comments:29 -->
- Measure allocation behavior before selecting a value receiver for an assumed performance gain. — [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type). <!-- code-review-comments:82 -->
- Prefer synchronous functions that complete their results, callbacks, and channel interactions before returning. — [Go Code Review Comments: Synchronous Functions](https://go.dev/wiki/CodeReviewComments#synchronous-functions). <!-- code-review-comments:85 -->
- Leave the decision to run an operation concurrently to its caller. — [Go Code Review Comments: Synchronous Functions](https://go.dev/wiki/CodeReviewComments#synchronous-functions). <!-- code-review-comments:86 -->

## Security

- Use crypto/rand for key generation, even for short-lived keys. — [Go Code Review Comments: Crypto Rand](https://go.dev/wiki/CodeReviewComments#crypto-rand). <!-- code-review-comments:15 -->
- Exclude both math/rand variants from cryptographic key generation. — [Go Code Review Comments: Crypto Rand](https://go.dev/wiki/CodeReviewComments#crypto-rand). <!-- code-review-comments:16 -->
- For text keys, use crypto/rand.Text or hex/base64 encoding of cryptographically random bytes. — [Go Code Review Comments: Crypto Rand](https://go.dev/wiki/CodeReviewComments#crypto-rand). <!-- code-review-comments:17 -->

## Language-specific pitfalls

- Leave out else after a branch that already returns or continues. — [Go Code Review Comments: Indent Error Flow](https://go.dev/wiki/CodeReviewComments#indent-error-flow). <!-- code-review-comments:44 -->
- Declare a value before the if when the continuing path also needs it. — [Go Code Review Comments: Indent Error Flow](https://go.dev/wiki/CodeReviewComments#indent-error-flow). <!-- code-review-comments:45 -->
- Wrap at meaningful boundaries and reconsider names, parameters, or function structure when readability suffers. — [Go Code Review Comments: Line Length](https://go.dev/wiki/CodeReviewComments#line-length). <!-- code-review-comments:56 -->
- Judge function size by readability instead of a numeric line limit. — [Go Code Review Comments: Line Length](https://go.dev/wiki/CodeReviewComments#line-length). <!-- code-review-comments:57 -->
- Use explicit return expressions in longer functions; bare returns can suit very small ones. — [Go Code Review Comments: Named Result Parameters](https://go.dev/wiki/CodeReviewComments#named-result-parameters). <!-- code-review-comments:62 -->

## Original worked examples

Original code under this skill's license: [context propagation and concrete results](examples/catalog.go), [ownership and cancellation checks](examples/catalog_test.go), [synchronous catalog use](examples/example_test.go).
