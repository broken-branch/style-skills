# Google Rust Style Guide: condensed rules

General Rust guidance, with reusable-library requirements distinguished from application preferences. Codebase-specific rules and exceptions are omitted.

Google inherits the official formatting and API guides where it makes no different choice. Keep the stated library/application distinctions and exceptions; do not turn its defaults into blanket lint prohibitions.

## Quick rules

Each source rule appears once below; read the sections relevant to the change.

## Tooling

- Favor code that remains readable and maintainable over reducing the author's immediate effort. — [Google Rust Style Guide: Goals of the style guide](https://google.github.io/styleguide/rustguide.html#goals-of-the-style-guide). <!-- GOOGLE:002 -->
- Prefer conventions that support reliable automated editing. — [Google Rust Style Guide: Goals of the style guide](https://google.github.io/styleguide/rustguide.html#goals-of-the-style-guide). <!-- GOOGLE:003 -->
- Depart from established Rust practice only for a concrete benefit. — [Google Rust Style Guide: Goals of the style guide](https://google.github.io/styleguide/rustguide.html#goals-of-the-style-guide). <!-- GOOGLE:004 -->
- Keep a style requirement only when its benefit justifies author and reviewer effort. — [Google Rust Style Guide: Goals of the style guide](https://google.github.io/styleguide/rustguide.html#goals-of-the-style-guide). <!-- GOOGLE:005 -->
- Settle recurring stylistic disputes with a few consistent arbitrary choices. — [Google Rust Style Guide: Goals of the style guide](https://google.github.io/styleguide/rustguide.html#goals-of-the-style-guide). <!-- GOOGLE:006 -->
- Use the codebase's chosen formatter. — [Google Rust Style Guide: Use the appropriate formatting tool](https://google.github.io/styleguide/rustguide.html#formatting-other). <!-- GOOGLE:034 -->
- Configure width 100, lowercase hex, formatted macro matchers, and escaped invisible literal characters, omitting unsupported settings on stable-only projects. — [Google Rust Style Guide: Use the appropriate formatting tool](https://google.github.io/styleguide/rustguide.html#formatting-other). <!-- GOOGLE:036 -->
- Reserve `rustfmt::skip` for justified alignment or generated material, ideally generating the latter at build time instead of checking it in. — [Google Rust Style Guide: Opting out of automatic formatting](https://google.github.io/styleguide/rustguide.html#formatting-optout). <!-- GOOGLE:037 -->
- Do not disable formatting solely to retain personal visual preferences. — [Google Rust Style Guide: Opting out of automatic formatting](https://google.github.io/styleguide/rustguide.html#formatting-optout). <!-- GOOGLE:038 -->

## Naming

- Name leaf modules and files for their principal type or abstraction, using a descriptive alternative when none dominates. — [Google Rust Style Guide: Name source files and leaf modules after the primary user-defined item](https://google.github.io/styleguide/rustguide.html#userdefined-item). <!-- GOOGLE:016 -->
- Follow standard method names, including the borrowing, copying, and consuming meanings of `as_`, `to_`, and `into_`. — [Google Rust Style Guide: Naming methods](https://google.github.io/styleguide/rustguide.html#naming-methods). <!-- GOOGLE:084 -->
- Give lifetimes meaningful names, especially in type declarations. — [Google Rust Style Guide: Naming lifetimes](https://google.github.io/styleguide/rustguide.html#lifetimes). <!-- GOOGLE:085 -->
- Allow anonymous or short lifetimes for very generic abstractions, one or two local relationships, and higher-ranked bounds; name larger sets descriptively. — [Google Rust Style Guide: Naming lifetimes](https://google.github.io/styleguide/rustguide.html#lifetimes). <!-- GOOGLE:086 -->
- Choose short generic names reflecting the parameter's purpose or main trait bound; meaningful single letters are fine. — [Google Rust Style Guide: Naming generic parameters](https://google.github.io/styleguide/rustguide.html#generic-parameters). <!-- GOOGLE:087 -->
- Use `T` and `U` for broadly reusable, largely unconstrained parameters. — [Google Rust Style Guide: Naming generic parameters](https://google.github.io/styleguide/rustguide.html#generic-parameters). <!-- GOOGLE:088 -->
- Suffix extension-trait names with `Ext`. — [Google Rust Style Guide: Naming extension traits](https://google.github.io/styleguide/rustguide.html#naming-extension-traits). <!-- GOOGLE:089 -->
- Call primary construction `new`, alternatives `new_with_...`, and fallible construction `try_new`. — [Google Rust Style Guide: Naming initialization functions](https://google.github.io/styleguide/rustguide.html#naming-initialization-functions). <!-- GOOGLE:090 -->
- Name value conversions `from_...`, also implementing `From` when the transformation satisfies its infallible contract. — [Google Rust Style Guide: Naming initialization functions](https://google.github.io/styleguide/rustguide.html#naming-initialization-functions). <!-- GOOGLE:091 -->
- Avoid obscure project jargon, acronyms, and abbreviations made by stripping interior letters. — [Google Rust Style Guide: Avoid abbreviations](https://google.github.io/styleguide/rustguide.html#avoid-abbreviations). <!-- GOOGLE:092 -->
- Prefer complete words, allowing abbreviations understood outside the project after reviewer judgment. — [Google Rust Style Guide: Avoid abbreviations](https://google.github.io/styleguide/rustguide.html#avoid-abbreviations). <!-- GOOGLE:093 -->
- Name reads after the field, returning a borrow or copied value, and suffix mutable-borrow accessors with `_mut`. — [Google Rust Style Guide: Getters and setters](https://google.github.io/styleguide/rustguide.html#getters-and-setters). <!-- GOOGLE:112 -->
- Use `take_...` to return a field's old value while leaving absence or a default behind. — [Google Rust Style Guide: Getters and setters](https://google.github.io/styleguide/rustguide.html#getters-and-setters). <!-- GOOGLE:113 -->
- Use `set_...` for assignment and `replace_...` when assignment also returns the old value. — [Google Rust Style Guide: Getters and setters](https://google.github.io/styleguide/rustguide.html#getters-and-setters). <!-- GOOGLE:114 -->
- Name callback-based access `with_...` or `with_mut_...`. — [Google Rust Style Guide: Getters and setters](https://google.github.io/styleguide/rustguide.html#getters-and-setters). <!-- GOOGLE:115 -->

## Files and layout

- Keep parent modules focused on declarations and re-exports, with little coordinating implementation. — [Google Rust Style Guide: Don’t implement APIs in non-leaf modules](https://google.github.io/styleguide/rustguide.html#non-leaf-modules). <!-- GOOGLE:017 -->
- An inline test or binding module does not by itself stop its parent being a leaf module. — [Google Rust Style Guide: Don’t implement APIs in non-leaf modules](https://google.github.io/styleguide/rustguide.html#non-leaf-modules). <!-- GOOGLE:018 -->
- Normally enumerate imports and avoid defining a glob-oriented prelude. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:019 -->
- Permit an inline module to glob-import its parent's names. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:020 -->
- Permit variant globs inside an enum's methods or functions chiefly concerned with that enum. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:021 -->
- Permit a parent module to re-export a child's public interface through a glob. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:022 -->
- Permit glob merging of same-named C++ namespaces across crates only inside a private module dedicated to that interop. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:023 -->
- Use a dependency's recommended prelude only after reviewer agreement. — [Google Rust Style Guide: Don’t use glob imports](https://google.github.io/styleguide/rustguide.html#glob-imports). <!-- GOOGLE:024 -->
- Restrict each grouped `use` to one module's members, splitting deeper paths into other declarations. — [Google Rust Style Guide: A use statement should import items from one module](https://google.github.io/styleguide/rustguide.html#use-statement). <!-- GOOGLE:025 -->
- Import traits within their consuming functions unless their methods are used throughout the file. — [Google Rust Style Guide: Prefer locally-scoped trait imports](https://google.github.io/styleguide/rustguide.html#prefer-local-trait-imports). <!-- GOOGLE:026 -->
- Call free functions from other modules or crates through their module name; the source’s exceptions, including usual direct C++ calls, still apply. — [Google Rust Style Guide: Qualify calls to top-level functions with a module name](https://google.github.io/styleguide/rustguide.html#toplevel-functions). <!-- GOOGLE:027 -->
- Allow direct function imports when names are already distinctive or qualification would introduce a module-name collision. — [Google Rust Style Guide: Qualify calls to top-level functions with a module name](https://google.github.io/styleguide/rustguide.html#toplevel-functions). <!-- GOOGLE:028 -->
- Import type and trait names so their ordinary uses do not need qualification. — [Google Rust Style Guide: Type names should be imported and used unqualified](https://google.github.io/styleguide/rustguide.html#type-names). <!-- GOOGLE:030 -->
- Rename or qualify colliding types; qualification also suits a related family of types. — [Google Rust Style Guide: Type names should be imported and used unqualified](https://google.github.io/styleguide/rustguide.html#type-names). <!-- GOOGLE:031 -->
- Keep qualified paths in generated code, macros, or files where numerous minor imports would obscure the import list. — [Google Rust Style Guide: Type names should be imported and used unqualified](https://google.github.io/styleguide/rustguide.html#type-names). <!-- GOOGLE:032 -->

## Types and data

- Apply API-design rules strictly to reusable libraries and as strong recommendations in applications. — [Google Rust Style Guide: Apply API design rules in context](https://google.github.io/styleguide/rustguide.html#api-design-context). <!-- GOOGLE:008 -->
- Keep application interfaces specific to current needs, generalizing only when justified. — [Google Rust Style Guide: Apply API design rules in context](https://google.github.io/styleguide/rustguide.html#api-design-context). <!-- GOOGLE:009 -->
- Begin with unique ownership and borrows; adopt `Rc` or `Arc` after review when avoiding sharing would make maintenance unreasonable. — [Google Rust Style Guide: Avoid Rc and Arc](https://google.github.io/styleguide/rustguide.html#avoid-rc-arc). <!-- GOOGLE:039 -->
- Prefer borrowing to unnecessary deep copies, accepting cloning when it substantially simplifies ownership. — [Google Rust Style Guide: Prefer borrows over deep copies](https://google.github.io/styleguide/rustguide.html#prefer-borrows). <!-- GOOGLE:040 -->
- Accept immutable borrowed data as `&T`, `&[T]`, `&str`, or `Option<&T>` rather than references to owning containers. — [Google Rust Style Guide: Accept flexible references for immutable data](https://google.github.io/styleguide/rustguide.html#flexible-references). <!-- GOOGLE:042 -->
- Use an appropriate alternative input representation for noncontiguous text such as ropes or cords. — [Google Rust Style Guide: Accept flexible references for immutable data](https://google.github.io/styleguide/rustguide.html#flexible-references). <!-- GOOGLE:043 -->
- Return an iterator when lazy evaluation or caller-selected collection storage is useful. — [Google Rust Style Guide: Iterators vs. owned collections in return types](https://google.github.io/styleguide/rustguide.html#return-iterators). <!-- GOOGLE:044 -->
- An application may simply return `Vec` when iterator flexibility and performance offer no material benefit. — [Google Rust Style Guide: Iterators vs. owned collections in return types](https://google.github.io/styleguide/rustguide.html#return-iterators). <!-- GOOGLE:045 -->
- Return `Vec` when consumers mostly collect, data already resides in one, indexing matters, cheap allocation makes a loop clearer, or constructing a collection is the purpose. — [Google Rust Style Guide: Iterators vs. owned collections in return types](https://google.github.io/styleguide/rustguide.html#return-iterators). <!-- GOOGLE:046 -->
- For reusable APIs that only traverse inputs, accept iterators or `IntoIterator`. — [Google Rust Style Guide: Iterators vs. slices in function parameters](https://google.github.io/styleguide/rustguide.html#accept-iterators). <!-- GOOGLE:047 -->
- Accept slices when indexing or contiguity matters, or when they simplify an application API without meaningful cost. — [Google Rust Style Guide: Iterators vs. slices in function parameters](https://google.github.io/styleguide/rustguide.html#accept-iterators). <!-- GOOGLE:048 -->
- Use library `impl Into<T>` parameters only when call-site convenience outweighs generic, binary-size, and inference costs. — [Google Rust Style Guide: Accepting Into](https://google.github.io/styleguide/rustguide.html#accepting-into). <!-- GOOGLE:049 -->
- Use `impl Into<T>` parameters very sparingly in applications. — [Google Rust Style Guide: Accepting Into](https://google.github.io/styleguide/rustguide.html#accepting-into). <!-- GOOGLE:050 -->
- Prefer an enum when a Boolean parameter would obscure the choice being made. — [Google Rust Style Guide: Prefer enum over bool in APIs](https://google.github.io/styleguide/rustguide.html#enum-vs-bool). <!-- GOOGLE:051 -->
- Choose a newtype for different meaning, a distinct interface, independent representation changes, or dangerous interchangeability. — [Google Rust Style Guide: Newtypes versus type aliases](https://google.github.io/styleguide/rustguide.html#newtypes-vs-type-aliases). <!-- GOOGLE:058 -->
- Favor named fields over tuples or multi-field tuple structs unless local meaning is obvious; single-field newtypes are exempt. — [Google Rust Style Guide: Prefer named fields over tuples and non-newtype tuple structs](https://google.github.io/styleguide/rustguide.html#prefer-named-fields). <!-- GOOGLE:059 -->
- Anticipate useful traits in foundational libraries, adding application trait implementations as needs arise. — [Google Rust Style Guide: Add trait implementations when they become necessary](https://google.github.io/styleguide/rustguide.html#traits-yagni). <!-- GOOGLE:060 -->
- Implement the matching standard trait for an operation, optionally retaining an inherent counterpart for discoverability. — [Google Rust Style Guide: Implement known standard library traits instead of custom methods](https://google.github.io/styleguide/rustguide.html#known-traits). <!-- GOOGLE:061 -->
- Use `derive` when it supplies the required behavior instead of reproducing that implementation manually. — [Google Rust Style Guide: Use #&#91;derive()&#93; if possible](https://google.github.io/styleguide/rustguide.html#derive). <!-- GOOGLE:062 -->
- Favor bounded generic library inputs over trait objects unless smaller generated code justifies dynamic dispatch. — [Google Rust Style Guide: Generics versus dyn Trait](https://google.github.io/styleguide/rustguide.html#generics-vs-dyn-trait). <!-- GOOGLE:063 -->
- Define traits to serve generic bounds, opaque or dynamic interfaces, or justified extension methods. — [Google Rust Style Guide: When to define a trait versus an inherent implementation](https://google.github.io/styleguide/rustguide.html#trait-vs-inherent-impl). <!-- GOOGLE:064 -->
- Put ordinary methods in inherent implementations; avoid traits whose sole purpose is dividing files or categorizing methods. — [Google Rust Style Guide: When to define a trait versus an inherent implementation](https://google.github.io/styleguide/rustguide.html#trait-vs-inherent-impl). <!-- GOOGLE:065 -->
- Usually let a type's owning team define its extension traits, except for widely useful and familiar framework extensions. — [Google Rust Style Guide: Extension traits](https://google.github.io/styleguide/rustguide.html#extension-traits). <!-- GOOGLE:066 -->
- Distinguish method-adding extension traits from abstractions deliberately accepting foreign implementations. — [Google Rust Style Guide: Extension traits](https://google.github.io/styleguide/rustguide.html#extension-traits). <!-- GOOGLE:067 -->
- For exposed-field types, consider implementing traits available on every field. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:068 -->
- Offer `Copy` when maintaining the promise through foreseeable evolution is reasonable. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:070 -->
- Make ordinary values `Clone`, allowing resource ownership to justify exceptions. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:071 -->
- Implement `Default` when a type has parameterless `new` or another meaningful default. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:072 -->
- Begin equality support with `PartialEq`, adding `Eq` only when every value equals itself. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:073 -->
- Begin comparison support with `PartialOrd`, adding `Ord` only when the ordering is total. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:074 -->
- Provide `Hash` and `Eq` for likely map keys or cached values, plus `Ord` when total ordering is meaningful. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:075 -->
- Pair a major `From` construction path with a discoverable inherent constructor. — [Google Rust Style Guide: Pair important From impls with explicit constructor methods](https://google.github.io/styleguide/rustguide.html#from-impls). <!-- GOOGLE:076 -->
- Make public-field options structures `Default` so callers can initialize them with struct-update syntax. — [Google Rust Style Guide: Options structs should implement Default](https://google.github.io/styleguide/rustguide.html#options-should-implement-default). <!-- GOOGLE:077 -->
- Consider callback access to interior-mutable data instead of exposing a particular guard implementation. — [Google Rust Style Guide: More on accessors that accept closures](https://google.github.io/styleguide/rustguide.html#closure-accessors). <!-- GOOGLE:116 -->
- Use callback mutation when it enables validation or follow-up work and a copying setter would be unsuitable. — [Google Rust Style Guide: More on accessors that accept closures](https://google.github.io/styleguide/rustguide.html#closure-accessors). <!-- GOOGLE:117 -->
- A callback accessor may forward the callback result; distinguish shared and mutable names when both exist, while a sole mutable form may use `with_...`. — [Google Rust Style Guide: More on accessors that accept closures](https://google.github.io/styleguide/rustguide.html#closure-accessors). <!-- GOOGLE:118 -->
- Provide `is_empty` alongside `len`. — [Google Rust Style Guide: Implement expected API sets together](https://google.github.io/styleguide/rustguide.html#expected-api-sets). <!-- GOOGLE:119 -->
- Promise `const` usability only when it can be maintained or affected clients can be helped to migrate. — [Google Rust Style Guide: Use const functions responsibly](https://google.github.io/styleguide/rustguide.html#const-functions). <!-- GOOGLE:121 -->
- Keep operator overloads consistent with their mathematical or logical meaning instead of using them as unrelated shorthand. — [Google Rust Style Guide: Avoid overloading for non-mathematical purposes](https://google.github.io/styleguide/rustguide.html#operator-overloads). <!-- GOOGLE:122 -->
- Use `non_exhaustive` for cross-team public enums unless variants are permanently fixed or all affected users will be migrated. — [Google Rust Style Guide: Apply #&#91;non_exhaustive&#93; to publicly-exposed enums](https://google.github.io/styleguide/rustguide.html#non-exhaustive-enums). <!-- GOOGLE:123 -->
- A narrowly used enum may omit `non_exhaustive` when adding variants has limited impact. — [Google Rust Style Guide: Apply #&#91;non_exhaustive&#93; to publicly-exposed enums](https://google.github.io/styleguide/rustguide.html#non-exhaustive-enums). <!-- GOOGLE:124 -->
- Use `non_exhaustive` for cross-team public structs whose public field set may change. — [Google Rust Style Guide: Apply #&#91;non_exhaustive&#93; to public structs with public fields](https://google.github.io/styleguide/rustguide.html#non-exhaustive-structs). <!-- GOOGLE:125 -->
- Allow exhaustive struct construction for effectively fixed fields, a commitment to migrate users, or intentional functional record update. — [Google Rust Style Guide: Apply #&#91;non_exhaustive&#93; to public structs with public fields](https://google.github.io/styleguide/rustguide.html#non-exhaustive-structs). <!-- GOOGLE:126 -->
- A struct used in few places may remain exhaustive when resulting breakage is limited. — [Google Rust Style Guide: Apply #&#91;non_exhaustive&#93; to public structs with public fields](https://google.github.io/styleguide/rustguide.html#non-exhaustive-structs). <!-- GOOGLE:127 -->
- Mark functions `must_use` when ignoring their results prevents correct use, including pure queries. — [Google Rust Style Guide: #&#91;must_use&#93; on functions](https://google.github.io/styleguide/rustguide.html#must-use-on-functions). <!-- GOOGLE:128 -->
- Require handling of errors and other essential outcomes without repeating `must_use` already present on the result type. — [Google Rust Style Guide: #&#91;must_use&#93; on functions](https://google.github.io/styleguide/rustguide.html#must-use-on-functions). <!-- GOOGLE:129 -->
- Put `must_use` on types representing essential results or deferred work when their producing functions otherwise need it. — [Google Rust Style Guide: #&#91;must_use&#93; on types](https://google.github.io/styleguide/rustguide.html#must-use-on-types). <!-- GOOGLE:130 -->
- Provide sufficient explicit types for a project-familiar reader to infer the omitted ones. — [Google Rust Style Guide: Don’t overuse type inference](https://google.github.io/styleguide/rustguide.html#type-inference). <!-- GOOGLE:132 -->
- Prefer annotating variables to adding turbofish arguments; use inference placeholders in required turbofishes where useful. — [Google Rust Style Guide: Don’t overuse type inference](https://google.github.io/styleguide/rustguide.html#type-inference). <!-- GOOGLE:133 -->
- Consider annotations for generic conversions such as `into` or `parse` and complicated iterator outputs. — [Google Rust Style Guide: Don’t overuse type inference](https://google.github.io/styleguide/rustguide.html#type-inference). <!-- GOOGLE:134 -->

## Errors

- Represent expected failure with `Option` when callers need no reason for the absence. — [Google Rust Style Guide: Reporting errors](https://google.github.io/styleguide/rustguide.html#reporting-errors). <!-- GOOGLE:053 -->
- Use `Result` for recoverable failures whose details guide the caller's response. — [Google Rust Style Guide: Reporting errors](https://google.github.io/styleguide/rustguide.html#reporting-errors). <!-- GOOGLE:054 -->
- Use panic for bugs or violated preconditions that require fixing rather than routine recovery. — [Google Rust Style Guide: Reporting errors](https://google.github.io/styleguide/rustguide.html#reporting-errors). <!-- GOOGLE:055 -->
- Follow a codebase policy requiring `Result` even for broken invariants. — [Google Rust Style Guide: Reporting errors](https://google.github.io/styleguide/rustguide.html#reporting-errors). <!-- GOOGLE:056 -->
- Permit assertion panics in tests and nonfatal-error panics in developer-facing programs. — [Google Rust Style Guide: Reporting errors](https://google.github.io/styleguide/rustguide.html#reporting-errors). <!-- GOOGLE:057 -->
- Make errors `Copy` when their fields allow it and that commitment suits the API. — [Google Rust Style Guide: Specific guidance for important traits](https://google.github.io/styleguide/rustguide.html#important-traits). <!-- GOOGLE:069 -->
- Match on a value instead of first checking its state and then using a panicking accessor. — [Google Rust Style Guide: Prefer pattern matching over check-then-unwrap](https://google.github.io/styleguide/rustguide.html#dont-check-then-unwrap). <!-- GOOGLE:135 -->
- When an invariant requires panic on access failure, use `expect` and explain the invariant. — [Google Rust Style Guide: Prefer expect over unwrap](https://google.github.io/styleguide/rustguide.html#expect-over-unwrap). <!-- GOOGLE:136 -->
- Do not make first-party correctness depend on recovery through `catch_unwind`. — [Google Rust Style Guide: Don’t call panic::catch_unwind](https://google.github.io/styleguide/rustguide.html#catch-unwind). <!-- GOOGLE:145 -->
- Allow a last-resort defensive catch in unwinding environments only after review confirms strong panic avoidance and independence from successful catching. — [Google Rust Style Guide: Don’t call panic::catch_unwind](https://google.github.io/styleguide/rustguide.html#catch-unwind). <!-- GOOGLE:146 -->

## Comments and docs

- When retaining a Boolean parameter, consider an inline explanation beside a literal argument. — [Google Rust Style Guide: Prefer enum over bool in APIs](https://google.github.io/styleguide/rustguide.html#enum-vs-bool). <!-- GOOGLE:052 -->
- Document public interfaces and consider enabling `missing_docs` to detect gaps. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:094 -->
- Provide enough examples to explain the crate without requiring a separate example for every function. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:095 -->
- Specify which input conditions can make a function panic. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:096 -->
- Use conventional capitalization and punctuation without explaining elementary Rust syntax. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:098 -->
- Omit comments that repeat evident behavior, allowing the documentation lint where needed; obvious enum variants need not each have prose. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:099 -->
- Use `///` on items and opening `//!` comments for module or crate documentation. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:100 -->
- Write rustdoc in Markdown using the official documentation-comment conventions. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:101 -->
- Use `//` for implementation notes and internal TODOs, even beside public rustdoc. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:102 -->
- Prefer directly authored source documentation to macro-generated documentation. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:103 -->

## Testing

- Consider assertion diagnostics that explain the invariant, relevant values, and whether misuse or an implementation defect is suspected. — [Google Rust Style Guide: Use context strings to clarify assertions](https://google.github.io/styleguide/rustguide.html#assertion-context). <!-- GOOGLE:139 -->
- Move useful assertion explanations into failure messages, especially when users may encounter them. — [Google Rust Style Guide: Use context strings to clarify assertions](https://google.github.io/styleguide/rustguide.html#assertion-context). <!-- GOOGLE:140 -->
- Avoid assertion messages that merely repeat the asserted expression. — [Google Rust Style Guide: Use context strings to clarify assertions](https://google.github.io/styleguide/rustguide.html#assertion-context). <!-- GOOGLE:141 -->

## Performance

- Include copy costs in ownership decisions and distinguish deep copies from normal `Rc` or `Arc` handle cloning. — [Google Rust Style Guide: Prefer borrows over deep copies](https://google.github.io/styleguide/rustguide.html#prefer-borrows). <!-- GOOGLE:041 -->

## Security

- Document the invariants required by unsafe functions and traits. — [Google Rust Style Guide: When and how to write documentation](https://google.github.io/styleguide/rustguide.html#writing-doc). <!-- GOOGLE:097 -->
- Introduce unsafe operations only when safe Rust cannot deliver the required behavior. — [Google Rust Style Guide: Unsafe code](https://google.github.io/styleguide/rustguide.html#unsafe). <!-- GOOGLE:104 -->
- Wrap necessary unsafe code in a safe abstraction separate from business logic, ideally a small crate with few external dependencies. — [Google Rust Style Guide: Unsafe code](https://google.github.io/styleguide/rustguide.html#unsafe). <!-- GOOGLE:105 -->
- Explain why each unsafe operation is valid in a `SAFETY:` comment. — [Google Rust Style Guide: Unsafe code](https://google.github.io/styleguide/rustguide.html#unsafe). <!-- GOOGLE:106 -->
- Document why safe alternatives fall short and provide benchmarks for speed claims, with justification scoped to the relevant block, file, or target. — [Google Rust Style Guide: Unsafe code](https://google.github.io/styleguide/rustguide.html#unsafe). <!-- GOOGLE:107 -->

## Language-specific pitfalls

- Do not recover or continue operating on a poisoned mutex's contents. — [Google Rust Style Guide: Handling poison](https://google.github.io/styleguide/rustguide.html#poison). <!-- GOOGLE:078 -->
- Prefer ordinary Rust, then declarative macros, then other generators, with procedural macros last. — [Google Rust Style Guide: Macros](https://google.github.io/styleguide/rustguide.html#macros). <!-- GOOGLE:082 -->
- Balance generation benefits against tooling limitations, unfamiliar syntax, and harder automated refactoring. — [Google Rust Style Guide: Macros](https://google.github.io/styleguide/rustguide.html#macros). <!-- GOOGLE:083 -->
- Avoid unstable compiler or library features unless the codebase authorizes an exception. — [Google Rust Style Guide: No unstable features](https://google.github.io/styleguide/rustguide.html#unstable-features). <!-- GOOGLE:108 -->
- Do not access another owner's `doc(hidden)` items. — [Google Rust Style Guide: Do not access items marked #&#91;doc(hidden)&#93; that you don’t own](https://google.github.io/styleguide/rustguide.html#doc-hidden). <!-- GOOGLE:120 -->
- Avoid executing user code through initialization mechanisms before `main`. — [Google Rust Style Guide: Do not run code before main()](https://google.github.io/styleguide/rustguide.html#global-initialization). <!-- GOOGLE:131 -->
- When matching a non-exhaustive enum, mention known variants explicitly, including ignored ones alongside the future wildcard. — [Google Rust Style Guide: Don’t omit patterns on non_exhaustive enums when matching](https://google.github.io/styleguide/rustguide.html#non-exhaustive-enum-matching). <!-- GOOGLE:137 -->
- Prefer `if let` or `let-else` when only a subset matters, retaining `match` when it reads better. — [Google Rust Style Guide: Don’t omit patterns on non_exhaustive enums when matching](https://google.github.io/styleguide/rustguide.html#non-exhaustive-enum-matching). <!-- GOOGLE:138 -->
- Replace hard-to-follow iterator chains with straightforward iteration when clearer. — [Google Rust Style Guide: Don’t use iterator combinator chains when direct iteration is clearer](https://google.github.io/styleguide/rustguide.html#combinator-chains). <!-- GOOGLE:142 -->
- Name a composed iterator in a local before looping instead of embedding its construction in the loop header. — [Google Rust Style Guide: Don’t use iterator combinator chains when direct iteration is clearer](https://google.github.io/styleguide/rustguide.html#combinator-chains). <!-- GOOGLE:143 -->
- Usually prefer `for` to `for_each`, retaining concise combinators that clearly express useful work. — [Google Rust Style Guide: Don’t use iterator combinator chains when direct iteration is clearer](https://google.github.io/styleguide/rustguide.html#combinator-chains). <!-- GOOGLE:144 -->
- Use `format!` or `write!` for joining at least three strings or filling literal templates instead of chained addition or repeated replacement. — [Google Rust Style Guide: Prefer format! / write! for concatenation and substitution](https://google.github.io/styleguide/rustguide.html#prefer-format-or-write). <!-- GOOGLE:148 -->

## Where the sources disagree

- Use the official formatting and API guidelines where Google's rules do not override them. — [Google Rust Style Guide: Follow public Rust style rules](https://google.github.io/styleguide/rustguide.html#public-rules). <!-- GOOGLE:007 -->

## Original worked examples

See [sources.md](sources.md) for original code, source tags and reading pointers.
