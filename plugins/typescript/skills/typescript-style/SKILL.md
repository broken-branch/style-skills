---
name: typescript-style
description: "Write, edit, or review .ts and tsconfig.json using house TypeScript style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: typescript
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# TypeScript style (house)

Our blend of the best TypeScript guides, in our own words. Every rule in the full guide names its source.

Scope: TypeScript 6.0.3, ES2022 application/library code, Node 24 LTS or newer supported releases (ESM) and browser bundles; NestJS module/provider and class-validation conventions from the 12.3 documentation. React and Vue add their own framework rules. JavaScript tooling files are outside the typed lint profile.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST enable `strict`, `exactOptionalPropertyTypes`, and `noUncheckedIndexedAccess` in TypeScript projects. Why: nullability, omitted properties, and missing indexes need separate checks. [TS-CONFIG]
- MUST use `unknown` for opaque values and narrow before accessing members; do not introduce `any`. Why: unchecked values otherwise spread through typed APIs. [GOOGLE-TS] [TS-ESLINT]
- MUST narrow nullable values instead of using postfix `!` or casting away nullability. Why: assertions do not establish runtime presence. [TS-ESLINT]
- MUST await, return, or attach a rejection handler to every promise; bare `void promise` is insufficient. Why: discarded failures escape the owning operation. [TS-ESLINT]
- MUST use `return await` when returning a promise from an `async` function. Why: rejection stays inside its error-handling and cleanup scope. [TS-ESLINT]
- MUST construct application failures with `Error` or its subclasses and reject with error objects. Why: callers need stack and cause information. [GOOGLE-TS]
- MUST treat caught values and promise rejection callbacks as `unknown` until narrowed before property access. Why: JavaScript dependencies can throw any value. [TS-CONFIG] [TS-ESLINT]
- MUST use ES module imports and named exports for application code, except framework-required default exports. Why: explicit symbols make dependencies and refactors predictable. [GOOGLE-TS]
- MUST annotate exported function and method boundaries while allowing inference for local implementation details. Why: callers need stable contracts without redundant local annotations. [TS-ESLINT] [GOOGLE-TS]
- MUST use `const` unless reassignment requires `let`; never use `var`. Why: block-scoped bindings prevent accidental reassignment and hoisting surprises. [GOOGLE-TS]
- MUST use interfaces for structural object contracts and type aliases for unions, tuples, and type transformations. Why: each construct communicates its intended role. [GOOGLE-TS] [TS-ESLINT]
- MUST handle every member when switching on a discriminated union or enum. Why: adding a variant must expose missing branches. [TS-ESLINT]
- MUST compare numbers, strings, and nullable primitives explicitly in conditions, preserving valid zero and empty-string values. Why: truthiness conflates absence with legitimate data. [TS-ESLINT]
- PREFER `??` for absence fallbacks and `?.` for optional access. Why: nullish operations preserve valid falsy values. [TS-ESLINT]
- PREFER UpperCamelCase for types/classes and lowerCamelCase for ordinary functions, variables, and properties; reserve CONSTANT_CASE for intended module-lifetime constants. Why: casing communicates the symbol's role. [GOOGLE-TS]
- MUST mark fields that never change after construction `readonly` and use readonly collection contracts for nonmutating inputs. Why: TypeScript can detect accidental writes. [GOOGLE-TS] [TS-ESLINT]
- MUST keep `@ts-ignore`, `@ts-nocheck`, and production `@ts-expect-error` out of TypeScript; permit explained `@ts-expect-error` only in `*.type-test.ts`. Why: negative type tests need a checked failure, while production errors need fixes. [GOOGLE-TS] [TS-ESLINT]
- PREFER named function declarations for ordinary functions and arrows for callbacks. Why: declarations expose intent and callbacks retain lexical `this`. [GOOGLE-TS]
- MUST initialize fields that depend on constructor parameter properties inside the constructor body. Why: native field initializers run before parameter-property assignment. [GOOGLE-TS] [TS-CONFIG]
- MUST use type-only imports/exports for erased contracts. Why: runtime dependencies must match the emitted module graph. [TS-CONFIG]
- MUST run the project's TypeScript type check (`tsc --noEmit` or the framework equivalent) as well as typed ESLint before calling work done. Why: lint rules do not replace compiler diagnostics. [TS-ESLINT-COMPAT]
- MUST use value imports for Nest DTO classes and implicit DI class tokens. Why: metadata needs constructors that exist at runtime. [TS-CONFIG] [NEST]
- MUST group Nest controllers, services, and DTOs by feature and import modules that export needed providers. Why: the DI graph follows explicit feature boundaries. [NEST]
- MUST inject Nest dependencies through constructors using runtime classes or explicit shared tokens. Why: erased interfaces cannot identify providers. [NEST]
- MUST use concrete DTO classes with validation decorators and a configured `ValidationPipe` for Nest's class-based request validation. Why: a TypeScript annotation alone does not run validation. [NEST-VALIDATION]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [typed result boundary](references/examples/result.ts), [validated batch record](references/examples/batch.ts), [typed adapter module](references/examples/batch_service.ts).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
