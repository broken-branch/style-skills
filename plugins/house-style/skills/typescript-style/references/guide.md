# TypeScript style guide

Scope: TypeScript 6.0.3, ES2022 application/library code, Node 24 LTS or newer supported releases (ESM) and browser bundles; NestJS module/provider and class-validation conventions from the 12.3 documentation. React and Vue add their own framework rules. JavaScript tooling files are outside the typed lint profile.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Prettier 3.9.10 | [Root web `.prettierrc.json`](config/.prettierrc.json) | `npx prettier --check .` |
| Linter | ESLint 10.14.0 / @eslint/js 10.0.1; typescript-eslint 8.72.1; eslint-config-prettier 10.1.8 | [`eslint.config.js`](config/eslint.config.js), strictTypeChecked + stylisticTypeChecked | `npx eslint --max-warnings 0 .` |
| Build / type checks | TypeScript 6.0.3 | [`tsconfig.base.json`](config/tsconfig.base.json), project `tsconfig.json` | `npx tsc --noEmit` |
| Tests | New-project default: Vitest 5.0.5 | Project's test configuration and lockfile | Project's declared test command |

Mechanical formatting: the formatter handles this. Copy [the single web config](config/.prettierrc.json) to the consuming repository root as `.prettierrc.json`; do not add competing language configs. TypeScript/TSX and Vue scripts use `singleQuote: true`; standalone `*.css` uses `false`. Vue `<style>` uses the SFC's `true` setting too. Only `*.html` disables embedded-language formatting; Vue scripts/styles remain formatted. [PRETTIER]

Run these commands from the project root after merging the configs and installing the pinned development dependencies. Not yet run against TypeScript 6.0.3 or ESLint 10.14.0 with the listed plugins; Prettier 3.9.10 was validated on a sample.

For adoption, copy/merge the compiler and ESLint configs plus the single root web Prettier config into the consuming project, add the exact compiler/linter/formatter versions above and its chosen test stack to development dependencies and resolve its lockfile, and point its scripts at its source/tests. The ESLint `.js` file is ESM: its package needs `"type": "module"`; a CommonJS project can name the same file `eslint.config.mjs`. The exported `createTypeScriptConfig({ files, tsconfigRootDir })` accepts framework globs and the consuming root. React additions can extend the default TS/TSX scope; Vue also needs its SFC parser, `.vue` project-service support, and TypeScript compatibility rules scoped to `.vue`.

The base deliberately leaves `module`/`moduleResolution`, environment types, and included files to a leaf `tsconfig.json`. Node projects can select `NodeNext`/`NodeNext`; browser bundles select `ESNext`/`Bundler`, add `DOM`/`DOM.Iterable` to `lib`, and choose their JSX setting. Node applications add `"types": ["node"]` with their pinned `@types/node` (TypeScript 6.0 defaults `types` to `[]`). An emitting build overrides `noEmit`, sets `rootDir` (for example, `"./src"`) and `outDir`, and can enable declarations. TypeScript 6.0 defaults `rootDir` to the tsconfig directory, so leaving it implicit can add a `src/` level to emitted paths. A CommonJS build also overrides `verbatimModuleSyntax: false`. This base checks code; it does not prescribe a bundler or run Nest decorators through Node's type stripper. [TS60]

- MUST enable `strict`, `exactOptionalPropertyTypes`, and `noUncheckedIndexedAccess` in TypeScript projects. Why: nullability, omitted properties, and missing indexes need separate checks. [TS-CONFIG]
- MUST include every linted TypeScript source and test in a project-service discoverable `tsconfig.json`, keeping compiler checks alongside typed linting. Why: lint rules need real type information and do not replace compiler diagnostics. [TS-ESLINT-COMPAT]
- MUST review effective rule membership when upgrading strict presets, including utility presets with their own instability warnings. Why: strict configuration contents can change outside major releases. [TS-ESLINT]
- MUST use the newest TypeScript inside typescript-eslint's supported range (6.0.x today); move to 7.x when that range includes it. Why: the published compatibility range currently ends below 6.1.0. [TS-ESLINT-COMPAT]
- MUST run the project's TypeScript type check (`tsc --noEmit` or the framework equivalent) as well as typed ESLint before calling work done. Why: lint rules do not replace compiler diagnostics. [TS-ESLINT-COMPAT]

ESLint 10 needs Node `^20.19.0 || ^22.13.0 || >=24`; the house Node 24+ baseline satisfies it. React repositories use the [documented ESLint 9.39.5 exception](related/react.md#tooling), including @eslint/js 9.39.5 at the common dependency root. The factory uses that installed preset; do not mix ESLint 10 recommended rules into a React 9 installation. [ESLint migration](https://eslint.org/docs/latest/use/migrate-to-10.0.0)

The dated [ESLint 10.14.0 source](https://github.com/eslint/eslint/blob/v10.14.0/packages/js/src/configs/eslint-recommended.js) and [@eslint/js 10.0.1 metadata](https://github.com/eslint/eslint/blob/v10.14.0/packages/js/package.json) supersede the registry's older `[ESLINT]` source link for this profile. The static recommended-preset diff adds `no-unassigned-vars`, `no-useless-assignment`, and `preserve-caught-error`: 150 enabled TypeScript/core rules versus 147 on React's ESLint 9. Runtime loading remains pending.

### Compiler and formatter enforcement

The following option IDs describe the supplied compiler configuration; unspecified `noUnusedLocals`/`noUnusedParameters` are handled by ESLint instead. [TS-CONFIG]

| Option ID | Enforced behavior |
| --- | --- |
| `strict` | Enables `alwaysStrict`, `noImplicitAny`, `noImplicitThis`, `strictBindCallApply`, `strictBuiltinIteratorReturn`, `strictFunctionTypes`, `strictNullChecks`, `strictPropertyInitialization`, `useUnknownInCatchVariables` in 6.0.3. |
| `exactOptionalPropertyTypes` | Distinguishes omitted properties from explicit `undefined`. |
| `noUncheckedIndexedAccess` | Adds absence to unchecked indexed lookups. |
| `noPropertyAccessFromIndexSignature` | Uses bracket access for undeclared dictionary keys. |
| `noImplicitOverride` | Requires `override` on overriding concrete members. |
| `noImplicitReturns` | Checks value-returning paths. |
| `noFallthroughCasesInSwitch` | Rejects nonempty case fallthrough. |
| `allowUnreachableCode: false`, `allowUnusedLabels: false` | Rejects syntactically unreachable statements and unused labels. |
| `forceConsistentCasingInFileNames` | Checks import-path casing consistency. |
| `isolatedModules`, `verbatimModuleSyntax` | Checks isolated compilation constraints and explicit type/value imports. |
| `noUncheckedSideEffectImports` | Reports unresolved side-effect imports. |
| `skipLibCheck: false` | Includes declaration files in checking. |
| `target`, `lib`, `useDefineForClassFields` | ES2022 API/emit assumptions and native field semantics. |
| `noEmit` | Check-only default; not an extra correctness diagnostic. |

Prettier has option IDs rather than lint-rule IDs: `printWidth`, `tabWidth`, `useTabs`, `semi`, `singleQuote`, `trailingComma`, `arrowParens`, `endOfLine`, plus per-file `overrides` for CSS quoting and HTML embedded formatting/whitespace/attributes. Its `printWidth` is a wrapping preference, not a maximum-line-length assertion. [PRETTIER]

### ESLint enforcement inventory

Every enabled rule ID for TypeScript files under ESLint 10 (150) is listed below, including inherited rules. All have error severity. This is a configuration inventory; human rules and their exceptions follow in the remaining sections. Preset membership was compared with the pinned upstream sources; runtime ESLint loading remains unverified. [ESLINT] [TS-ESLINT]

| Rule ID | Check / configured scope |
| --- | --- |
| `@typescript-eslint/adjacent-overload-signatures` | Keep one function's overload signatures together. |
| `@typescript-eslint/array-type` | Simple elements use T[]; complex elements use Array<T>, including readonly forms. |
| `@typescript-eslint/await-thenable` | Await only a promise-like value. |
| `@typescript-eslint/ban-ts-comment` | Bans suppression directives; explained ts-expect-error (10+ characters) only in *.type-test.ts. |
| `@typescript-eslint/ban-tslint-comment` | Remove obsolete TSLint configuration comments. |
| `@typescript-eslint/class-literal-property-style` | Represent a class's constant literal property consistently, using a field by default rather than an equivalent getter. |
| `@typescript-eslint/consistent-generic-constructors` | Put generic construction arguments on the constructor by default rather than solely on the left-side type annotation. |
| `@typescript-eslint/consistent-indexed-object-style` | Use Record for eligible indexed object contracts by default, or the configured index-signature alternative. |
| `@typescript-eslint/consistent-type-assertions` | Uses as assertions; rejects assertions directly on object literals. |
| `@typescript-eslint/consistent-type-definitions` | Use interfaces for object contracts by default, or the selected consistent type-alias alternative. |
| `@typescript-eslint/consistent-type-exports` | Marks type-only re-exports explicitly. |
| `@typescript-eslint/dot-notation` | Use dot access for known identifier-like members where the type/visibility rules permit it. |
| `@typescript-eslint/explicit-member-accessibility` | Omits public; parameter-property exceptions are reviewed manually. |
| `@typescript-eslint/explicit-module-boundary-types` | Requires explicit exported function/method parameter and return types, with rule-defined expression allowances. |
| `@typescript-eslint/no-array-constructor` | Create ordinary arrays with literal syntax rather than a generic Array constructor. |
| `@typescript-eslint/no-array-delete` | Do not delete an array slot, leaving a hole instead of removing an element. |
| `@typescript-eslint/no-base-to-string` | Convert an object to text only when it has a meaningful string representation. |
| `@typescript-eslint/no-confusing-non-null-assertion` | Do not place a non-null assertion where it looks like another operator. |
| `@typescript-eslint/no-confusing-void-expression` | Keep void-valued calls in a position that does not suggest a meaningful result. |
| `@typescript-eslint/no-deprecated` | Do not use an API marked deprecated. |
| `@typescript-eslint/no-duplicate-enum-values` | Give enum members distinct explicitly initialized values. |
| `@typescript-eslint/no-duplicate-type-constituents` | Remove duplicate members from a union/intersection type. |
| `@typescript-eslint/no-dynamic-delete` | Do not delete dynamically computed object keys when the configured object design forbids it. |
| `@typescript-eslint/no-empty-function` | Do not leave a function body empty without an allowed intentional case. |
| `@typescript-eslint/no-empty-object-type` | Avoid an accidentally unconstrained non-nullish empty-object type. |
| `@typescript-eslint/no-explicit-any` | Do not explicitly use any without a scoped justified exception. |
| `@typescript-eslint/no-extra-non-null-assertion` | Remove repeated or otherwise redundant non-null assertions. |
| `@typescript-eslint/no-extraneous-class` | Rejects unnecessary classes; decorated framework classes are allowed. |
| `@typescript-eslint/no-floating-promises` | Checks unhandled promises, including void-discarded promises and async IIFEs. |
| `@typescript-eslint/no-for-in-array` | Do not iterate an array with for-in. |
| `@typescript-eslint/no-generated-empty-object-type` | Avoid type operations unintentionally producing an empty-object/non-nullish type. |
| `@typescript-eslint/no-implied-eval` | Do not invoke eval-like string execution through indirect APIs. |
| `@typescript-eslint/no-import-type-side-effects` | Uses a top-level import type when all specifiers are types. |
| `@typescript-eslint/no-inferrable-types` | Omit a primitive annotation already obvious from a literal initializer/default. |
| `@typescript-eslint/no-invalid-void-type` | Keep void types in meaningful result/generic positions. |
| `@typescript-eslint/no-meaningless-void-operator` | Use void only when it actually discards a meaningful result. |
| `@typescript-eslint/no-misused-new` | Use new and constructor signatures only in their valid class/interface roles. |
| `@typescript-eslint/no-misused-promises` | Do not pass a promise into a synchronous Boolean/callback/object position that cannot handle it. |
| `@typescript-eslint/no-misused-spread` | Avoid spreads whose operand type makes their copied contents surprising. |
| `@typescript-eslint/no-mixed-enums` | Do not mix numeric and string enum values in one enum. |
| `@typescript-eslint/no-namespace` | Avoid TypeScript namespace declarations except the rule's configured ambient/definition allowances. |
| `@typescript-eslint/no-non-null-asserted-nullish-coalescing` | Do not assert away null on the left of a nullish-coalescing fallback. |
| `@typescript-eslint/no-non-null-asserted-optional-chain` | Do not immediately cancel optional-chain nullability with a non-null assertion. |
| `@typescript-eslint/no-non-null-assertion` | Do not bypass null checks with a postfix non-null assertion. |
| `@typescript-eslint/no-redundant-type-constituents` | Remove union/intersection constituents that are redundant or erase useful type information. |
| `@typescript-eslint/no-require-imports` | Use module imports rather than require calls. |
| `@typescript-eslint/no-this-alias` | Do not save this in a redundant alias binding. |
| `@typescript-eslint/no-unnecessary-boolean-literal-compare` | Use the Boolean expression directly instead of redundantly comparing it to true/false. |
| `@typescript-eslint/no-unnecessary-condition` | Remove conditions whose type proves their outcome constant. |
| `@typescript-eslint/no-unnecessary-template-expression` | Remove unnecessary template interpolation wrappers. |
| `@typescript-eslint/no-unnecessary-type-arguments` | Omit a type argument already supplied by its default. |
| `@typescript-eslint/no-unnecessary-type-assertion` | Remove an assertion that leaves the expression's type unchanged. |
| `@typescript-eslint/no-unnecessary-type-constraint` | Remove a generic constraint that imposes no useful restriction. |
| `@typescript-eslint/no-unnecessary-type-conversion` | Remove conversions that change neither value nor type. |
| `@typescript-eslint/no-unnecessary-type-parameters` | Remove a generic parameter not relating two or more positions. |
| `@typescript-eslint/no-unsafe-argument` | Do not feed an any-typed argument into a typed parameter unchecked. |
| `@typescript-eslint/no-unsafe-assignment` | Do not propagate any into typed variable/property assignments unchecked. |
| `@typescript-eslint/no-unsafe-call` | Do not call an any-typed value without a safe callable contract. |
| `@typescript-eslint/no-unsafe-declaration-merging` | Do not merge declarations in a way that promises members absent from their runtime implementation. |
| `@typescript-eslint/no-unsafe-enum-assignment` | Assign enum-typed locations from the corresponding enum rather than unrelated raw values. |
| `@typescript-eslint/no-unsafe-enum-comparison` | Compare an enum to values belonging to that enum rather than unrelated raw values. |
| `@typescript-eslint/no-unsafe-function-type` | Use a specific callable signature rather than the unsafe broad Function type. |
| `@typescript-eslint/no-unsafe-member-access` | Do not access arbitrary members through any. |
| `@typescript-eslint/no-unsafe-return` | Do not return any through a typed result contract unchecked. |
| `@typescript-eslint/no-unsafe-unary-minus` | Apply numeric negation only to a supported numeric type. |
| `@typescript-eslint/no-unused-expressions` | Do not leave an expression whose result and side effects are unused. |
| `@typescript-eslint/no-unused-vars` | Checks all parameters/caught errors; required unused parameters may start with _. |
| `@typescript-eslint/no-useless-constructor` | Omit a constructor whose behavior is already provided implicitly. |
| `@typescript-eslint/no-useless-default-assignment` | Remove a default initializer proven unreachable/unneeded for that input. |
| `@typescript-eslint/no-wrapper-object-types` | Use primitive types rather than boxed wrapper object types. |
| `@typescript-eslint/only-throw-error` | Throw Error instances rather than unrelated values. |
| `@typescript-eslint/prefer-as-const` | Use a const assertion instead of restating a value's literal type. |
| `@typescript-eslint/prefer-find` | Use find instead of filtering the whole array and selecting its first result. |
| `@typescript-eslint/prefer-for-of` | Use for-of when a loop only needs consecutive array elements. |
| `@typescript-eslint/prefer-function-type` | Represent a callable contract with a function type instead of a one-call-signature interface. |
| `@typescript-eslint/prefer-includes` | Use includes rather than a numeric indexOf membership comparison. |
| `@typescript-eslint/prefer-literal-enum-member` | Give enum members simple literal values rather than arbitrary calculations. |
| `@typescript-eslint/prefer-namespace-keyword` | If an allowed TypeScript namespace is necessary, spell it namespace rather than the older module keyword. |
| `@typescript-eslint/prefer-nullish-coalescing` | Use nullish coalescing when only null/undefined should trigger a fallback. |
| `@typescript-eslint/prefer-optional-chain` | Use optional chaining for equivalent repeated existence guards. |
| `@typescript-eslint/prefer-promise-reject-errors` | Reject promises with Error objects rather than primitive reasons. |
| `@typescript-eslint/prefer-readonly` | Detects private fields assigned only during construction; public fields/collection inputs still need review. |
| `@typescript-eslint/prefer-reduce-type-parameter` | Pass a type argument to reduce rather than asserting the accumulator's type. |
| `@typescript-eslint/prefer-regexp-exec` | Use RegExp.exec rather than non-global String.match when testing/extracting one match. |
| `@typescript-eslint/prefer-return-this-type` | Return this in a polymorphic method signature when only the receiver itself is returned. |
| `@typescript-eslint/prefer-string-starts-ends-with` | Use startsWith/endsWith for equivalent prefix/suffix checks. |
| `@typescript-eslint/related-getter-setter-pairs` | Make a getter's type assignable to its corresponding setter input. |
| `@typescript-eslint/require-await` | Do not mark a function async when it neither returns a promise nor performs awaiting. |
| `@typescript-eslint/restrict-plus-operands` | Keep plus operands in compatible numeric/bigint/string domains according to the preset's allowances. |
| `@typescript-eslint/restrict-template-expressions` | Interpolate strings in templates, allowing only the extra scalar categories explicitly permitted by configuration. |
| `@typescript-eslint/return-await` | Requires return await for promises returned from async functions. |
| `@typescript-eslint/strict-boolean-expressions` | Rejects string/number truthiness and nullable primitive conditions; nullable-object existence checks are allowed. |
| `@typescript-eslint/switch-exhaustiveness-check` | Checks missing union/enum cases even when a default branch exists. |
| `@typescript-eslint/triple-slash-reference` | Prefer ES imports to the restricted triple-slash reference directives. |
| `@typescript-eslint/unbound-method` | Do not call/pass an unbound method in a way that loses its required receiver. |
| `@typescript-eslint/unified-signatures` | Unify overloads that can be represented clearly with a union or optional/rest parameter. |
| `@typescript-eslint/use-unknown-in-catch-callback-variable` | Type promise rejection callbacks as unknown and narrow before treating their values as errors. |
| `eqeqeq` | Checks strict equality, permitting == null and != null for both nullish values. |
| `for-direction` | Core correctness check from @eslint/js recommended. |
| `no-async-promise-executor` | Core correctness check from @eslint/js recommended. |
| `no-case-declarations` | Core correctness check from @eslint/js recommended. |
| `no-compare-neg-zero` | Core correctness check from @eslint/js recommended. |
| `no-cond-assign` | Core correctness check from @eslint/js recommended. |
| `no-constant-binary-expression` | Core correctness check from @eslint/js recommended. |
| `no-constant-condition` | Core correctness check from @eslint/js recommended. |
| `no-control-regex` | Core correctness check from @eslint/js recommended. |
| `no-debugger` | Core correctness check from @eslint/js recommended. |
| `no-delete-var` | Core correctness check from @eslint/js recommended. |
| `no-dupe-else-if` | Core correctness check from @eslint/js recommended. |
| `no-duplicate-case` | Core correctness check from @eslint/js recommended. |
| `no-empty` | Core correctness check from @eslint/js recommended. |
| `no-empty-character-class` | Core correctness check from @eslint/js recommended. |
| `no-empty-pattern` | Core correctness check from @eslint/js recommended. |
| `no-empty-static-block` | Core correctness check from @eslint/js recommended. |
| `no-eval` | Rejects eval calls. |
| `no-ex-assign` | Core correctness check from @eslint/js recommended. |
| `no-extend-native` | Rejects extensions to built-in prototypes. |
| `no-extra-boolean-cast` | Core correctness check from @eslint/js recommended. |
| `no-fallthrough` | Core correctness check from @eslint/js recommended. |
| `no-global-assign` | Core correctness check from @eslint/js recommended. |
| `no-invalid-regexp` | Core correctness check from @eslint/js recommended. |
| `no-irregular-whitespace` | Core correctness check from @eslint/js recommended. |
| `no-loss-of-precision` | Core correctness check from @eslint/js recommended. |
| `no-misleading-character-class` | Core correctness check from @eslint/js recommended. |
| `no-new-func` | Rejects Function-constructor code generation. |
| `no-nonoctal-decimal-escape` | Core correctness check from @eslint/js recommended. |
| `no-octal` | Core correctness check from @eslint/js recommended. |
| `no-prototype-builtins` | Core correctness check from @eslint/js recommended. |
| `no-regex-spaces` | Core correctness check from @eslint/js recommended. |
| `no-restricted-syntax` | Rejects default declarations, direct export let, and const enum; *.config.{ts,mts,cts} permits only default declarations, and other framework defaults need a scoped override. |
| `no-self-assign` | Core correctness check from @eslint/js recommended. |
| `no-shadow-restricted-names` | Core correctness check from @eslint/js recommended. |
| `no-sparse-arrays` | Core correctness check from @eslint/js recommended. |
| `no-unassigned-vars` | Rejects variables read without ever being assigned a value. |
| `no-unsafe-finally` | Core correctness check from @eslint/js recommended. |
| `no-unsafe-optional-chaining` | Core correctness check from @eslint/js recommended. |
| `no-unused-labels` | Core correctness check from @eslint/js recommended. |
| `no-unused-private-class-members` | Core correctness check from @eslint/js recommended. |
| `no-useless-assignment` | Rejects assignments whose values are never read before replacement. |
| `no-useless-backreference` | Core correctness check from @eslint/js recommended. |
| `no-useless-catch` | Core correctness check from @eslint/js recommended. |
| `no-useless-escape` | Core correctness check from @eslint/js recommended. |
| `no-var` | Use const/let rather than var. |
| `prefer-const` | Use const for a binding never reassigned. |
| `prefer-rest-params` | Use rest parameters rather than arguments. |
| `prefer-spread` | Use call spread rather than manual apply. |
| `preserve-caught-error` | Requires preserving a caught error as the cause when throwing a replacement Error. |
| `require-yield` | Core correctness check from @eslint/js recommended. |
| `use-isnan` | Core correctness check from @eslint/js recommended. |
| `valid-typeof` | Core correctness check from @eslint/js recommended. |

`reportUnusedDisableDirectives: error` is an ESLint configuration diagnostic, not a rule ID. `eslint-config-prettier` runs last and disables competing layout rules, including core `no-unexpected-multiline`; Prettier checks layout separately. TypeScript compatibility disables core checks already performed by the compiler or TypeScript-aware rules: `constructor-super`, `getter-return`, `no-class-assign`, `no-const-assign`, `no-dupe-args`, `no-dupe-class-members`, `no-dupe-keys`, `no-func-assign`, `no-import-assign`, `no-new-native-nonconstructor`, `no-new-symbol`, `no-obj-calls`, `no-redeclare`, `no-setter-return`, `no-this-before-super`, `no-undef`, `no-unreachable`, `no-unsafe-negation`, `no-with`; replacements also disable `no-array-constructor`, `no-implied-eval`, `no-unused-expressions`, `no-unused-vars`, `no-useless-constructor`, `no-throw-literal`, `prefer-promise-reject-errors`, `require-await`, `no-return-await`, `dot-notation`, and `no-empty-function`. [ESLINT] [TS-ESLINT] [PRETTIER]

Deliberately disabled/not enabled: `@typescript-eslint/non-nullable-type-assertion-style` conflicts with banning postfix `!`; `@typescript-eslint/consistent-type-imports` overlaps compiler import checks and has decorator-metadata caveats; `@typescript-eslint/parameter-properties` is unnecessary for a preference; `@typescript-eslint/explicit-function-return-type` would overconstrain local inference. The `all` preset is not used. [TS-ESLINT]

Review-only checks include domain naming, constant intent, justified assertions, module initialization effects, public-field/input immutability, runtime validation completeness, Nest provider scope and wiring, runtime DTO imports, callback receiver behavior beyond the rule's analysis, event-loop blocking, and request-versus-process failure classification. `no-restricted-syntax` catches direct `export let`, not every later re-export of a mutable binding. The configs do not enforce HTTP headers, password policy, production runtime settings, or framework integration tests.

## Naming

- PREFER UpperCamelCase for types/classes and lowerCamelCase for ordinary functions, variables, and properties; reserve CONSTANT_CASE for intended module-lifetime constants. Why: casing communicates the symbol's role. [GOOGLE-TS]
- PREFER treating acronyms as words, such as `HttpClient` and `parseUrl`, without `I` interface prefixes or underscore privacy markers. Why: TypeScript already exposes symbol kinds and visibility. [GOOGLE-TS]
- MUST reserve a leading underscore for a required unused parameter rather than hiding unused locals or imports. Why: the lint exemption has a narrow callback/interface purpose. [GOOGLE-TS] [TS-ESLINT]

## Files and layout

- MUST use type-only imports/exports for erased contracts. Why: runtime dependencies must match the emitted module graph. [TS-CONFIG]
- MUST use ES module imports and named exports for application code, except framework-required default exports. Why: explicit symbols make dependencies and refactors predictable. [GOOGLE-TS]
- MUST keep exported mutable bindings behind functions instead of exporting or re-exporting `let` variables. Why: module consumers should not depend on changing bindings as implicit state APIs. [GOOGLE-TS]
- PREFER relative imports inside a feature and explicit public entry points between packages. Why: dependencies stay local while package internals can change. [GOOGLE-TS] [NODE-PRACTICES]
- MUST write Node ESM relative specifiers for the emitted files, such as `./service.js`, and use `node:` for built-in imports. Why: runtime resolution must match the compiled module graph. [TS-CONFIG] [NODE-PRACTICES]
- PREFER explicit bootstrap functions for I/O and registration, retaining documented side-effect imports for necessary polyfills or framework registration. Why: ordinary imports should not start services or make network requests. [GOOGLE-TS] [NODE-PRACTICES]

Tool configs matching `**/*.config.{ts,mts,cts}` (for example Vite, Vitest, and Playwright) automatically permit default exports while retaining the `export let` and `const enum` bans. Include them in a discoverable `tsconfig.json`, or a `tsconfig.node.json` referenced by it, so project service can load them. Framework route defaults still need their own narrow override. [Vite configuration](https://vite.dev/config/) [TS-ESLINT-COMPAT]

### NestJS

- MUST use value imports for Nest DTO classes and implicit DI class tokens. Why: metadata needs constructors that exist at runtime. [TS-CONFIG] [NEST]
- MUST group Nest controllers, services, and DTOs by feature and import modules that export needed providers. Why: the DI graph follows explicit feature boundaries. [NEST]
- MUST keep bootstrap in `main.ts`, root wiring in `app.module.ts`, and transport mapping in controllers with business work in providers. Why: Nest's application graph and request adapters have distinct responsibilities. [NEST]
- MUST inject Nest dependencies through constructors using runtime classes or explicit shared tokens. Why: erased interfaces cannot identify providers. [NEST]
- MUST register a shared provider in one host module, export its token, and import that module from consumers. Why: registering the class repeatedly can create separate service instances. [NEST]
- PREFER singleton providers and explicit module imports; use request scope or global modules only for a documented lifecycle need. Why: request scope propagates through consumers and global modules hide dependencies. [NEST]
- MUST use concrete DTO classes with validation decorators and a configured `ValidationPipe` for Nest's class-based request validation. Why: a TypeScript annotation alone does not run validation. [NEST-VALIDATION]
- PREFER `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })` for class-based HTTP DTOs, with explicit conversion/parse rules for query and route values. Why: unexpected properties are rejected and implicit JavaScript coercions need deliberate handling. [NEST-VALIDATION]
- MUST enable `experimentalDecorators` and `emitDecoratorMetadata` in Nest leaf configs when using legacy metadata-based DI and validation, and retain class value imports. Why: standard decorators and erased imports do not supply the same runtime metadata. [TS-CONFIG] [NEST]
- MUST keep `strictPropertyInitialization` enabled; use a documented field definite-assignment declaration only for DTO properties guaranteed by runtime validation/hydration, never as a general service-field shortcut. Why: a DTO's external initialization is distinct from ordinary construction. [TS-CONFIG] [NEST-VALIDATION]
- PREFER small typed custom parameter decorators and compatible `applyDecorators` compositions for repeated Nest request policies. Why: the framework provides this extension mechanism. [NEST]
- MUST set `validateCustomDecorators: true` when a `ValidationPipe` must validate values supplied by custom decorators. Why: that validation path is not enabled implicitly. [NEST]
- PREFER direct provider/module imports over barrels and remove DI cycles before considering `forwardRef`. Why: circular module initialization can leave constructor metadata undefined. [NEST]
- MUST use `forwardRef` on both sides of an unavoidable Nest module/provider cycle and avoid depending on constructor order. Why: deferred resolution does not establish deterministic initialization. [NEST]
- PREFER async provider factories for dependencies that require initialization before use. Why: Nest awaits their resolution before constructing consumers. [NEST]

The permitted DTO declaration `field!: T` is a definite-assignment assertion, not the prohibited expression `value!`. Its correctness requires a validation test; `@typescript-eslint/no-non-null-assertion` does not establish that invariant. Nest's actual dependency graph, emitted metadata, and transport validation remain application checks.

## Types and data

- MUST use `unknown` for opaque values and narrow before accessing members; do not introduce `any`. Why: unchecked values otherwise spread through typed APIs. [GOOGLE-TS] [TS-ESLINT]
- MUST narrow nullable values instead of using postfix `!` or casting away nullability. Why: assertions do not establish runtime presence. [TS-ESLINT]
- MUST annotate exported function and method boundaries while allowing inference for local implementation details. Why: callers need stable contracts without redundant local annotations. [TS-ESLINT] [GOOGLE-TS]
- MUST use interfaces for structural object contracts and type aliases for unions, tuples, and type transformations. Why: each construct communicates its intended role. [GOOGLE-TS] [TS-ESLINT]
- MUST mark fields that never change after construction `readonly` and use readonly collection contracts for nonmutating inputs. Why: TypeScript can detect accidental writes. [GOOGLE-TS] [TS-ESLINT]
- MUST use `const` unless reassignment requires `let`; never use `var`. Why: block-scoped bindings prevent accidental reassignment and hoisting surprises. [GOOGLE-TS]
- MUST distinguish `field?: T` from `field: T | undefined` and explicitly allow `undefined` when present-but-undefined is valid. Why: presence tests and serialization distinguish these contracts. [TS-CONFIG]
- MUST handle every member when switching on a discriminated union or enum. Why: adding a variant must expose missing branches. [TS-ESLINT]
- MUST compare numbers, strings, and nullable primitives explicitly in conditions, preserving valid zero and empty-string values. Why: truthiness conflates absence with legitimate data. [TS-ESLINT]
- PREFER `??` for absence fallbacks and `?.` for optional access. Why: nullish operations preserve valid falsy values. [TS-ESLINT]
- MUST use `T[]`/`readonly T[]` for simple array elements and `Array<T>`/`ReadonlyArray<T>` for complex elements. Why: the configured array-simple rule makes nested types consistent. [GOOGLE-TS] [TS-ESLINT]
- PREFER a type annotation or `satisfies` for object construction instead of an `as` assertion. Why: construction should be checked against the intended shape. [GOOGLE-TS] [TS-ESLINT]
- MUST use lowercase primitive types and concrete callable signatures instead of boxed types, broad `Function`, or `{}` as an opaque-value type. Why: those types promise a different or insufficiently checked domain. [GOOGLE-TS] [TS-ESLINT]
- PREFER `Map`/`Set` for dynamic key collections and `Record<K, V>` for fixed dictionary contracts. Why: collection operations avoid prototype-key and dynamic-delete traps. [GOOGLE-TS] [TS-ESLINT]

## Errors

- MUST construct application failures with `Error` or its subclasses and reject with error objects. Why: callers need stack and cause information. [GOOGLE-TS]
- MUST treat caught values and promise rejection callbacks as `unknown` until narrowed before property access. Why: JavaScript dependencies can throw any value. [TS-CONFIG] [TS-ESLINT]
- MUST await, return, or attach a rejection handler to every promise; bare `void promise` is insufficient. Why: discarded failures escape the owning operation. [TS-ESLINT]
- MUST use `return await` when returning a promise from an `async` function. Why: rejection stays inside its error-handling and cleanup scope. [TS-ESLINT]
- MUST use `{ cause: originalError }` when wrapping an error, preserving even an unknown upstream rejection value without reading its properties. Why: JavaScript's cause slot can retain evidence without unsafe assumptions. [TS-CONFIG] [GOOGLE-TS]
- MUST handle Node stream/EventEmitter error events or use promise-based APIs that propagate them, such as `pipeline`. Why: an outer synchronous `try` does not catch a later emitted error. [NODE-PRACTICES]
- MUST map expected request failures to responses while treating uncaught process-level exceptions as fatal; use synchronous final cleanup and external restart supervision. Why: invalid requests should not kill the service, but uncaught failures can leave process state corrupted. [NODE-PRACTICES] [NODE-RUNTIME]

A terminal rejection handler must itself be safe; linting can see that a handler exists, but cannot prove its logging/recovery path cannot reject. Passing a caught unknown value unchanged as an error's cause is permitted; claiming it has an Error's properties requires narrowing.

## Comments and docs

- MUST use JSDoc for TypeScript API documentation, place it before decorators, and omit redundant type/visibility tags. Why: the signature already supplies types and documentation tools associate comments with declarations. [GOOGLE-TS]
- PREFER `@deprecated` with migration guidance for a deprecated TypeScript API. Why: editors and typed linting can surface the replacement path. [GOOGLE-TS] [TS-ESLINT]

## Testing

- MUST await or return asynchronous assertions, and use the runner's rejection/throw assertions instead of a `try` that can catch its own failed assertion. Why: asynchronous failures must reach the test runner. [GOOGLE-TS] [TS-ESLINT]
- MUST keep `@ts-ignore`, `@ts-nocheck`, and production `@ts-expect-error` out of TypeScript; permit explained `@ts-expect-error` only in `*.type-test.ts`. Why: negative type tests need a checked failure, while production errors need fixes. [GOOGLE-TS] [TS-ESLINT]
- MUST type-check negative type fixtures without executing them, and confirm their intended diagnostics after changing the fixture. Why: an unrelated compiler error can accidentally satisfy `@ts-expect-error`. [TS-ESLINT] [TS-CONFIG]
- PREFER Vitest for new TypeScript projects, with colocated `*.test.ts` or Nest `*.spec.ts` tests and separate integration suites; retain an established runner when appropriate. Why: one default covers typed unit tests while repository-specific integration needs remain explicit. [NEST] [NODE-PRACTICES]
- MUST use Nest testing modules to check provider wiring, override external providers through their tokens, and await application initialization and closure. Why: constructing a service alone cannot exercise the DI graph or application lifecycle. [NEST-TESTING]
- MUST exercise Nest DTO validation with malformed, missing, and extra fields and with the actual application pipes. Why: a class type does not prove the transport validation configuration. [NEST-VALIDATION] [NEST-TESTING]

The new-project test baseline is [Vitest 5.0.5](https://github.com/vitest-dev/vitest/releases/tag/v5.0.5); resolve compatible Vite/environment dependencies in the consuming lockfile. The tiny `node:test` harness here remains dependency-free and uses Node's experimental `stripTypeScriptTypes` only to execute erasable fixtures, not as a production build or type check.

## Performance

- MUST keep synchronous I/O and sustained CPU work off Node request/event-loop paths, using async APIs and workers where appropriate. Why: one blocked event loop delays unrelated requests. [NODE-PRACTICES]
- PREFER prototype methods over per-instance arrow fields, using stable bound arrows where callback registration/removal requires them. Why: ordinary methods avoid per-instance closures while stable handlers retain identity. [GOOGLE-TS]
- PREFER sequential `for...of` for dependent async operations and bounded concurrency for independent operations. Why: `forEach(async ...)` does not await completion and unbounded promise batches can exhaust resources. [TS-ESLINT] [NODE-PRACTICES]

## Security

- MUST avoid `eval`, `new Function`, and string-valued timer execution in application TypeScript. Why: JavaScript can interpret data as executable code. [GOOGLE-TS] [TS-ESLINT]
- MUST use `crypto.randomBytes` or `crypto.randomUUID` for Node security tokens, never `Math.random`. Why: general-purpose randomness is unsuitable for unpredictable credentials. [NODE-PRACTICES]
HTTP headers, browser response caching, framing, and human-password expiration follow [shared Security](shared.md#security) for every server language.

## Language-specific pitfalls

- PREFER named function declarations for ordinary functions and arrows for callbacks. Why: declarations expose intent and callbacks retain lexical `this`. [GOOGLE-TS]
- PREFER inline arrows that forward only the intended callback arguments, naming complex/reused callbacks when useful. Why: extra callback arguments and a lost receiver can change behavior. [GOOGLE-TS]
- MUST initialize fields that depend on constructor parameter properties inside the constructor body. Why: native field initializers run before parameter-property assignment. [GOOGLE-TS] [TS-CONFIG]
- PREFER constructor parameter properties for direct assignments, including `private readonly` Nest dependencies. Why: the declaration expresses the injected field without duplicate boilerplate. [GOOGLE-TS] [NEST]
- MUST omit redundant `public` modifiers except when a non-readonly public constructor parameter property needs one. Why: public is TypeScript's default, while parameter properties require a modifier. [GOOGLE-TS]
- MUST use ordinary enums rather than `const enum` when an enum is required. Why: const-enum inlining creates cross-package and isolated-compilation hazards. [GOOGLE-TS] [TS-CONFIG]
- MUST use strict equality except intentional `== null`/`!= null` tests covering both nullish values. Why: other coercive comparisons hide mismatched domains. [GOOGLE-TS] [ESLINT]
- MUST check numeric conversions with `Number.isFinite` and appropriate range/integer tests. Why: JavaScript conversions can produce `NaN` or silently lose precision. [GOOGLE-TS]
- MUST avoid extending built-in prototypes and spreading class instances as if they were plain records. Why: prototype behavior and nonenumerable state do not survive an ordinary shallow spread. [GOOGLE-TS] [TS-ESLINT]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- PREFER typed Nest custom decorators for repeated framework policies: Google's source-local rule prohibits defining decorators, while Nest documents them as an extension API. Why: Nest's supported abstraction fits this framework scope. [GOOGLE-TS] [NEST]
- MUST use interfaces for structural-only contracts and classes for reflected Nest DTOs: Google favors structural interfaces, while Nest needs runtime metatypes. Why: the two uses require different runtime representations. [GOOGLE-TS] [NEST]
- MUST narrow caught values from `unknown`: Google assumes Error-only throws in its controlled codebase, while TypeScript and typed ESLint protect against arbitrary JavaScript throws. Why: arbitrary dependencies do not share Google's enforced invariant. [GOOGLE-TS] [TS-CONFIG] [TS-ESLINT]
- MUST let the root `.prettierrc.json` select statement termination through `semi: true`: Google requires explicit termination, while Node Best Practices permits either safe style. Why: the formatter makes one reproducible choice. [GOOGLE-TS] [NODE-PRACTICES] [PRETTIER]
- PREFER function declarations for ordinary named functions and arrows for callbacks: Google distinguishes these roles, while Node Best Practices broadly favors arrows. Why: context determines whether lexical `this` is useful. [GOOGLE-TS] [NODE-PRACTICES]
- PREFER inline forwarding arrows for short callbacks and named helpers for complex/reused callbacks: Google permits inline arrows, while Node Best Practices names every closure for profiling. Why: argument and receiver correctness outweigh a blanket naming requirement. [GOOGLE-TS] [NODE-PRACTICES]
- PREFER CONSTANT_CASE only for intended module-lifetime constants: Google ties casing to constancy, while Node Best Practices also uppercases mutable global/static values. Why: casing should not imply immutability that is absent. [GOOGLE-TS] [NODE-PRACTICES]
- MUST annotate exported boundaries while inferring local implementation types: Google leaves returns to local policy, Node Best Practices recommends explicit contracts, and ESLint offers an all-functions rule. Why: `explicit-module-boundary-types` protects APIs with less local noise. [GOOGLE-TS] [NODE-PRACTICES] [TS-ESLINT]
- MUST configure array-simple notation: Google distinguishes simple and complex elements, while the stylistic default uses suffixes throughout. Why: an explicit `array-type` override enforces the selected Google convention. [GOOGLE-TS] [TS-ESLINT]
- MUST limit explained `@ts-expect-error` to `*.type-test.ts`: Google prohibits ordinary production suppressions, while the recommended/strict defaults allow explained ones broadly. Why: the file-scoped override preserves negative testing without weakening production checking. [GOOGLE-TS] [TS-ESLINT]
- PREFER straightforward constructor parameter properties: Google and Nest use them, while the optional `all` preset's parameter-properties default forbids them. Why: we select strict/stylistic and leave that optional prohibition disabled. [GOOGLE-TS] [NEST] [TS-ESLINT]
- MUST omit redundant public modifiers with the constructor parameter-property exception: Google omits public, while the optional explicit-accessibility default requires it. Why: the configured no-public policy matches the selected convention. [GOOGLE-TS] [TS-ESLINT]
- MUST narrow instead of postfix `!`: Google permits justified assertions and stylistic can suggest `!`, while strict forbids it. Why: disabling `non-nullable-type-assertion-style` prevents contradictory fixes while retaining strict null safety. [GOOGLE-TS] [TS-ESLINT]
- MUST use `return await` in async functions: Node Best Practices always awaits, while ESLint's optional in-try-catch mode forbids ordinary-context awaits and its strict default allows either there. Why: selecting the always mode gives one rule compatible with error scopes. [NODE-PRACTICES] [TS-ESLINT]
- PREFER explicit bootstrap effects with documented registration/polyfill import exceptions: Node Best Practices avoids import-time effects, while Google permits intentional side-effect imports. Why: required initialization remains visible without making every import active. [NODE-PRACTICES] [GOOGLE-TS]
- MUST retain ESLint with the typed strict/stylistic profiles even if Nest scaffolds oxlint: Node Best Practices favors ESLint, while the current Nest scaffold chooses another engine. Why: the required typed rules need their configured engine; scaffold defaults do not replace them. [NODE-PRACTICES] [NEST] [TS-ESLINT]
- MUST follow [shared Security](shared.md#security) and current OWASP human-password rotation guidance over the Node-linked page's frequent-rotation advice. Why: compromise/leak and authenticator changes warrant resets; arbitrary periodic resets do not. [NODE-PRACTICES] [OWASP]
- MUST follow [shared Security](shared.md#security) and current OWASP HTTP-header guidance over Node's historical XSS-filter, Expect-CT, and HPKP recipes. Why: obsolete browser defenses must not be copied into new middleware. [NODE-PRACTICES] [OWASP]
- MUST distinguish expected request errors from fatal uncaught process failures: Node Best Practices' restart advice and request-level crash avoidance apply to different failure scopes. Why: invalid requests need responses, while a corrupted process cannot safely resume. [NODE-PRACTICES] [NODE-RUNTIME]
- MUST treat each preset's explicit instability warning as authoritative when the shared-configs introduction lists fewer exceptions. Why: the stricter per-preset warning avoids assuming an unsupported stability guarantee. [TS-ESLINT]
