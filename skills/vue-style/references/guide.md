# Vue style guide

Scope: owned Vue 3.5+ applications and component libraries using compiled Single-File Components (SFCs), Composition API, and TypeScript 6.0.3. Build/test tools use Node 24 LTS or a newer supported release. Vue 2, in-DOM templates, and existing Options API migrations need separate profiles; this guide does not authorize a migration.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow. [TypeScript](related/typescript.md) supplies the script-language baseline; NestJS rules apply only to NestJS code.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

## Quick rules

- MUST write each component as one `.vue` SFC using `<script setup lang="ts">` and Composition API. Why: one component model gives templates direct typed bindings. [VUE-SFC] [VUE-LINT]
- MUST run `vue-tsc --noEmit` with `vueCompilerOptions.strictTemplates: true` over Vue SFCs and their TypeScript dependencies. Why: bundler transpilation and script linting do not check template contracts. [VUE-TS]
- MUST use PascalCase filenames and component bindings with multi-word names, except the root `App.vue`. Why: component identities remain distinct from native elements. [VUE-STYLE] [VUE-LINT]
- MUST declare props in camelCase and pass component prop attributes in kebab-case. Why: one declaration/use convention removes SFC casing choices. [VUE-STYLE] [VUE-LINT]
- MUST emit ordinary custom events in camelCase and listen with kebab-case attributes, preserving Vue model events such as `update:modelValue`. Why: event conventions must retain framework contracts. [VUE-LINT] [VUE-MODEL]
- MUST declare props with `defineProps<Props>()` and emitted payloads with a typed `defineEmits` event-to-tuple map. Why: consumers get checked component inputs and outputs. [VUE-TS] [VUE-LINT]
- MUST destructure declared props with `const { value = fallback } = defineProps<Props>()`, using defaults only when meaningful. Why: Vue 3.5 preserves reactive reads and supports per-instance defaults in this syntax. [VUE-PROPS] [VUE-TS] [VUE-LINT]
- MUST leave incoming props and their nested objects/arrays unmodified; request owner updates through declared events. Why: child writes otherwise bypass the parent's state ownership. [VUE-PROPS] [VUE-LINT]
- PREFER `ref` for component state and read or write `.value` in script; top-level template refs unwrap automatically. Why: ref identity survives value replacement. [VUE-REACTIVITY]
- MUST give `ref` and `shallowRef` an inferable initial type or an explicit generic, including nullability where needed. Why: empty initialization must not create untyped mutable state. [VUE-TS] [VUE-LINT]
- MUST keep computed getters synchronous, side-effect-free, and value-returning. Why: cached derivation must not start asynchronous work or mutate its inputs. [VUE-REACTIVITY] [VUE-LINT]
- MUST pass a ref or getter such as `() => id` for a destructured prop to watchers and reactive composables, not its current value `id`. Why: later prop changes must remain observable. [VUE-WATCH] [VUE-COMPOSABLES]
- MUST use `useTemplateRef` for static template refs and handle null before accessing their value. Why: elements can be absent before mount or after conditional removal. [VUE-TEMPLATE-REFS] [VUE-LINT]
- MUST use shared `InjectionKey<T>` symbols for typed injection and check an absent required provider explicitly. Why: a type parameter cannot guarantee a provider exists. [VUE-TS]
- MUST avoid child-only defaults in `defineModel`; initialize defaults in the owning parent. Why: otherwise parent and child model values can start out different. [VUE-MODEL] [VUE-LINT]
- MUST give each `v-for` item a unique, stable primitive key, placing the key on the `template v-for` wrapper for grouped siblings. Why: identity must follow the item when the list changes. [VUE-STYLE] [VUE-LINT]
- MUST keep `v-if`, `v-else-if`, and `v-else` off elements carrying `v-for`; filter with computed data or use a separate wrapper. Why: Vue 3 evaluates `v-if` before the iteration scope exists. [VUE-STYLE] [VUE-LINT]
- PREFER simple template expressions, moving branching or repeated computation into named computed values or functions. Why: templates should make rendering relationships easy to inspect. [VUE-STYLE]
- MUST import child components directly in script setup and register custom directives explicitly. Why: template dependencies remain resolvable by tooling. [VUE-SFC] [VUE-LINT]
- MUST use `scoped` styles or CSS Modules for ordinary application SFC styles, with plain CSS limited to explicitly configured App/layout/library paths. Why: ordinary component styles must not leak globally. [VUE-STYLE] [VUE-LINT]
- MUST register lifecycle hooks and component-owned watchers synchronously during setup; call lifecycle-dependent composables there too. Why: Vue needs the active component to own and dispose of them. [VUE-LIFECYCLE] [VUE-WATCH] [VUE-COMPOSABLES]
- MUST cancel or invalidate stale asynchronous watcher work and register `onWatcherCleanup` before the first await. Why: a superseded request must not overwrite current component state. [VUE-WATCH]
- MUST name composables `useX` and keep them in TypeScript modules. Why: callers can recognize functions that own reactive behavior. [VUE-COMPOSABLES]
- MUST render text through interpolation and keep `v-html` out of ordinary components; never compile untrusted strings as Vue templates. Why: raw markup and executable templates bypass Vue's safe text rendering. [VUE-SECURITY] [VUE-LINT]
- MUST await Vue Test Utils updates such as `trigger`, `setValue`, and `setProps`, then flush external promises when relevant. Why: Vue DOM batching and asynchronous services settle independently. [VUE-TEST]

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Prettier 3.9.10, inherited from TypeScript | [Root web `.prettierrc.json`](config/.prettierrc.json) | `npx prettier --check .` |
| Linter | ESLint 10.14.0 / @eslint/js 10.0.1; typescript-eslint 8.72.1; eslint-plugin-vue 10.12.0; vue-eslint-parser 10.4.1; eslint-config-prettier 10.1.8 | [Vue flat additions](config/eslint.config.js) over [TypeScript](config/typescript/eslint.config.js) | `npx eslint --max-warnings 0 .` |
| Build / type checks | vue-tsc 3.3.14 with TypeScript 6.0.3 and Vue 3.5.44 (3.5+ profile) | project `tsconfig.json` over the strict TypeScript base | `npx vue-tsc --noEmit` |
| Tests | Vitest 5.0.5 + @vue/test-utils 2.5.1; Playwright 1.64.1 | Consuming project's test configuration and lockfile; no component runner bundled | Consuming project's component/browser test command |

Mechanical formatting: the formatter handles this. Copy [the single web config](config/.prettierrc.json) to the consuming repository root as `.prettierrc.json`; do not add competing language configs. TypeScript/TSX and Vue scripts use `singleQuote: true`; standalone `*.css` uses `false`. Vue `<style>` uses the SFC's `true` setting too. Only `*.html` disables embedded-language formatting; Vue scripts/styles remain formatted. [PRETTIER]

Run these commands from the project root after adopting the configs and installing the pinned development dependencies. Not yet run against ESLint 10.14.0, its listed plugins and parsers, Vue 3.5.44, or vue-tsc 3.3.14 with TypeScript 6.0.3. Prettier 3.9.10 was validated on a sample.

Adoption keeps the sibling TypeScript import or adjusts it to the copied base. Tool dependencies belong at a common project root so imports in both config modules resolve. The consuming ESM `eslint.config.js` imports `createVueConfig` and calls it with `tsconfigRootDir: import.meta.dirname` and its source globs. A CommonJS project uses an `.mjs` config. `plainStyleFiles` defaults to `['**/App.vue']`; explicit layout/library paths may be added for intentional global or class-scoped CSS. This exception changes only style-block admission, not script or template checks. [VUE-LINT-CONFIG] [VUE-LINT]

The leaf selects `ESNext`/`Bundler`, browser libraries, `jsx: preserve`, `jsxImportSource: vue`, and both `.ts`/`.vue` includes. It deliberately extends the existing house base instead of adding a competing `@vue/tsconfig` baseline. Build/test/SSR environments need their own leaf projects and matching resolver aliases. No wildcard `*.vue` declaration returning `any` is supplied. [VUE-TS]

Imported-SFC compatibility: `createVueConfig` supplies `sfcInteropFiles`, defaulting to `['**/main.ts', '**/router/**/*.{ts,mts,cts}']`. Only those paths disable `@typescript-eslint/no-unsafe-argument`, `no-unsafe-assignment`, `no-unsafe-return`, `no-unsafe-call`, and `no-unsafe-member-access`; ordinary TypeScript and SFCs retain all five. Add exact async-component or exposed-ref integration paths through this option when they consume incomplete `.vue` import types. Keep non-interop logic outside those files. `vue-tsc --noEmit` with `strictTemplates` is the type authority for these operations; explicit `any` remains banned. [Vue helper source](https://github.com/vuejs/eslint-config-typescript/blob/main/src/internals.ts) [VUE-LINT-CONFIG]

SFC `<style>` contents are explicitly **review-only** in this distribution: ESLint checks style-block admission, not CSS declarations. Apply the [CSS guide](related/css.md) by review; automated SFC style checking requires a separately configured `postcss-html` Stylelint profile and project validation. Vue styles use single quotes under the root SFC formatting setting; standalone CSS uses double quotes. [STYLELINT] [PRETTIER]

`[VUE-TS]` compiler-option evidence uses [language-tools 3.3.14](https://github.com/vuejs/language-tools/blob/v3.3.14/packages/language-core/lib/types.ts), rather than the older 3.1.1 API. ESLint 10's inherited rules and Node engine floor follow [TypeScript Tooling](related/typescript.md#tooling).

- MUST run `vue-tsc --noEmit` with `vueCompilerOptions.strictTemplates: true` over Vue SFCs and their TypeScript dependencies. Why: bundler transpilation and script linting do not check template contracts. [VUE-TS]
- MUST parse SFCs with `vue-eslint-parser`, delegate scripts to the TypeScript parser, and include `.vue` in both lint globs and `extraFileExtensions`. Why: replacing the outer parser loses Vue syntax and template analysis. [VUE-LINT-CONFIG]
- MUST keep project-service settings and `extraFileExtensions` consistent across Vue and TypeScript files, with a discoverable leaf tsconfig. Why: typed rules need the right project without repeatedly reloading it. [VUE-LINT-CONFIG]
- MUST apply the TypeScript core-rule compatibility map to `.vue` files and put `eslint-config-prettier` after the Vue presets. Why: SFCs need the same core replacements and formatter conflict resolution as TypeScript. [VUE-LINT-CONFIG] [PRETTIER]

### Enforcement inventory

The configuration combines Vue's `flat/recommended` with the TypeScript strict and stylistic type-checked presets. The following inventories list every enabled ID for an SFC under the pinned versions, including inherited rules. Preset warnings also fail the command because it uses `--max-warnings 0`; explicitly added checks are errors. Ordinary `.ts` modules receive the inherited TypeScript checks plus Vue's recommended script checks and the three reactivity/ref additions. SFC-only checks do not run on plain TypeScript. [VUE-LINT] [TS-ESLINT]

#### Inherited TypeScript rules

These script checks retain the settings described in [TypeScript Tooling](related/typescript.md#tooling), including the scoped `*.type-test.ts` exception. The 150 enabled inherited IDs are listed here for ordinary SFCs. The five unsafe checks marked below are disabled only on `sfcInteropFiles`, leaving 145 inherited checks there; all 126 Vue additions remain configured for SFCs. [TS-ESLINT] [ESLINT]

| Rule ID | Inherited behavior |
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
| `@typescript-eslint/no-unsafe-argument` | Off only on `sfcInteropFiles`; otherwise: Do not feed an any-typed argument into a typed parameter unchecked. |
| `@typescript-eslint/no-unsafe-assignment` | Off only on `sfcInteropFiles`; otherwise: Do not propagate any into typed variable/property assignments unchecked. |
| `@typescript-eslint/no-unsafe-call` | Off only on `sfcInteropFiles`; otherwise: Do not call an any-typed value without a safe callable contract. |
| `@typescript-eslint/no-unsafe-declaration-merging` | Do not merge declarations in a way that promises members absent from their runtime implementation. |
| `@typescript-eslint/no-unsafe-enum-assignment` | Assign enum-typed locations from the corresponding enum rather than unrelated raw values. |
| `@typescript-eslint/no-unsafe-enum-comparison` | Compare an enum to values belonging to that enum rather than unrelated raw values. |
| `@typescript-eslint/no-unsafe-function-type` | Use a specific callable signature rather than the unsafe broad Function type. |
| `@typescript-eslint/no-unsafe-member-access` | Off only on `sfcInteropFiles`; otherwise: Do not access arbitrary members through any. |
| `@typescript-eslint/no-unsafe-return` | Off only on `sfcInteropFiles`; otherwise: Do not return any through a typed result contract unchecked. |
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

#### Vue additions

| Rule ID | Enforced behavior / limit |
| --- | --- |
| `vue/attribute-hyphenation` | Component attributes use kebab-case. |
| `vue/attributes-order` | Preset semantic groups; object-spread ordering can affect runtime behavior. |
| `vue/block-lang` | Requires a script block with lang="ts". |
| `vue/block-order` | Script, template, then style blocks. |
| `vue/comment-directive` | Recognize ESLint control comments inside template markup. |
| `vue/component-api-style` | Only script-setup API forms in SFCs; recognized component options are checked. |
| `vue/component-definition-name-casing` | Apply the selected casing to declared component names. |
| `vue/component-name-in-template-casing` | PascalCase for registered/imported component tags; filenames remain a review check. |
| `vue/custom-event-name-casing` | CamelCase custom events in script; update:model events have built-in exceptions. |
| `vue/define-emits-declaration` | Type-literal event maps for defineEmits. |
| `vue/define-props-declaration` | Type-based defineProps declarations. |
| `vue/define-props-destructuring` | destructure: always; requires reactive props destructuring, with meaningful defaults. |
| `vue/enforce-style-attribute` | scoped or module; plain only in explicit plainStyleFiles. |
| `vue/eqeqeq` | Template equality uses strict operators, allowing null comparisons. |
| `vue/html-button-has-type` | Give buttons an explicit type. |
| `vue/jsx-uses-vars` | Count JSX component references as uses of their JavaScript bindings. |
| `vue/multi-word-component-names` | Use component names containing more than one word. |
| `vue/no-arrow-functions-in-watch` | Use ordinary functions rather than arrows for Options API watchers. |
| `vue/no-async-in-computed-properties` | Keep computed-value evaluation synchronous. |
| `vue/no-child-content` | Do not supply children that a content-replacing directive would overwrite. |
| `vue/no-computed-properties-in-data` | Do not read computed values while initializing data. |
| `vue/no-define-model-default` | No defineModel defaults that can diverge from the parent. |
| `vue/no-deprecated-data-object-declaration` | For Vue 3, replace the old object form of component data. |
| `vue/no-deprecated-delete-set` | For Vue 3, stop calling the obsolete $delete and $set APIs. |
| `vue/no-deprecated-destroyed-lifecycle` | For Vue 3, replace beforeDestroy and destroyed with supported lifecycle hooks. |
| `vue/no-deprecated-dollar-listeners-api` | For Vue 3, stop reading the removed $listeners API. |
| `vue/no-deprecated-dollar-scopedslots-api` | For Vue 3, replace the former $scopedSlots API. |
| `vue/no-deprecated-events-api` | For Vue 3, replace the obsolete instance event-bus APIs. |
| `vue/no-deprecated-filter` | For Vue 3, remove the former filter expression syntax. |
| `vue/no-deprecated-functional-template` | For Vue 3, remove the old functional attribute on component templates. |
| `vue/no-deprecated-html-element-is` | For Vue 3, avoid the former component-replacement use of is on native elements. |
| `vue/no-deprecated-inline-template` | For Vue 3, remove the old inline-template facility. |
| `vue/no-deprecated-model-definition` | For Vue 3, replace component model option declarations with supported model interfaces. |
| `vue/no-deprecated-props-default-this` | For Vue 3, do not rely on a component instance through this inside a prop-default factory. |
| `vue/no-deprecated-router-link-tag-prop` | Stop using RouterLink's obsolete tag prop. |
| `vue/no-deprecated-scope-attribute` | Replace the deprecated scope attribute used before Vue 2.5. |
| `vue/no-deprecated-slot-attribute` | Replace the slot attribute superseded in Vue 2.6. |
| `vue/no-deprecated-slot-scope-attribute` | Replace the slot-scope attribute superseded in Vue 2.6. |
| `vue/no-deprecated-v-bind-sync` | For Vue 3, replace v-bind's old sync modifier. |
| `vue/no-deprecated-v-is` | Remove the v-is directive deprecated in Vue 3.1. |
| `vue/no-deprecated-v-on-native-modifier` | For Vue 3, remove the former native event modifier. |
| `vue/no-deprecated-v-on-number-modifiers` | For Vue 3, use supported key names instead of numeric keycode modifiers. |
| `vue/no-deprecated-vue-config-keycodes` | For Vue 3, stop configuring Vue.config.keyCodes. |
| `vue/no-dupe-keys` | Give component fields distinct names rather than defining a name repeatedly. |
| `vue/no-dupe-v-else-if` | Do not repeat a condition already handled in the same conditional chain. |
| `vue/no-duplicate-attr-inheritance` | Disable implicit attribute inheritance when manually forwarding $attrs. |
| `vue/no-duplicate-attributes` | Do not declare the same attribute repeatedly on one element. |
| `vue/no-export-in-script-setup` | Do not put module export statements in script setup. |
| `vue/no-expose-after-await` | Register the exposed component interface before asynchronous suspension. |
| `vue/no-import-compiler-macros` | Do not import macros supplied directly by the Vue compiler. |
| `vue/no-lifecycle-after-await` | Register lifecycle hooks synchronously before await. |
| `vue/no-lone-template` | Remove template wrappers that serve no purpose. |
| `vue/no-multiple-slot-args` | Pass only one argument object to a scoped slot. |
| `vue/no-mutating-props` | Direct and statically recognized nested prop mutation prohibited. |
| `vue/no-parsing-error` | Correct template parse errors. |
| `vue/no-ref-as-operand` | Operate on a ref's contained value rather than the ref wrapper. |
| `vue/no-ref-object-reactivity-loss` | Avoid extracting ref-wrapper state in ways that stop subsequent changes from being tracked. |
| `vue/no-required-prop-with-default` | Mark a prop optional when its default makes omission valid. |
| `vue/no-reserved-component-names` | Do not name components with names reserved by the framework or platform. |
| `vue/no-reserved-keys` | Leave reserved instance keys intact. |
| `vue/no-reserved-props` | Avoid framework-reserved names for props. |
| `vue/no-setup-props-reactivity-loss` | Keep setup props reactive rather than taking root-scope destructured or extracted snapshots. |
| `vue/no-shared-component-data` | Return each component instance's data from a factory function. |
| `vue/no-side-effects-in-computed-properties` | Keep computed getters free of observable mutations and other side effects. |
| `vue/no-template-key` | Do not assign keys to plain template wrappers; the detailed rule expressly allows Vue 3 template v-for keys. |
| `vue/no-template-shadow` | Do not hide an outer template binding with a same-named inner declaration. |
| `vue/no-textarea-mustache` | Do not use interpolation text to control a textarea's value. |
| `vue/no-undef-components` | Use only components that can be resolved in the template's context. |
| `vue/no-undef-directives` | Use only custom directives that can be resolved in the template's context. |
| `vue/no-unused-components` | Remove component registrations that the template never uses. |
| `vue/no-unused-vars` | Remove unused loop and scoped-slot bindings. |
| `vue/no-use-computed-property-like-method` | Read a computed property as a value rather than invoking it as a method. |
| `vue/no-use-v-else-with-v-for` | Keep v-else and v-else-if off elements that also carry v-for. |
| `vue/no-use-v-if-with-v-for` | No same-element combination; allowUsingIterationVar: false. |
| `vue/no-useless-template-attributes` | Remove template-wrapper attributes that have no effect. |
| `vue/no-v-for-template-key-on-child` | For Vue 3 repeated template groups, put the group's key on the template instead of its children. |
| `vue/no-v-html` | Avoid raw HTML insertion through v-html because it can introduce cross-site scripting. |
| `vue/no-v-text-v-html-on-component` | Do not apply native content-replacement directives to component tags. |
| `vue/no-watch-after-await` | Create watchers before asynchronous suspension. |
| `vue/one-component-per-file` | Give each component its own file. |
| `vue/order-in-components` | Preset order for recognized component option objects. |
| `vue/prefer-define-options` | Put script-setup component options in defineOptions rather than a separate default export. |
| `vue/prefer-import-from-vue` | Import public Vue APIs through vue rather than internal @vue packages. |
| `vue/prefer-use-template-ref` | Static string refs use useTemplateRef; callback refs are exempt. |
| `vue/prop-name-casing` | Use one selected casing convention for declared props. |
| `vue/require-component-is` | Give dynamic component elements their bound is selector. |
| `vue/require-explicit-emits` | Declare the events that a component emits. |
| `vue/require-explicit-slots` | Slot outlets need declarations; slot prop types are checked by vue-tsc. |
| `vue/require-prop-type-constructor` | Express runtime prop types as constructor values. |
| `vue/require-prop-types` | Specify types for component props. |
| `vue/require-render-return` | Make every render function produce a return value. |
| `vue/require-slots-as-functions` | Invoke Vue 3 slot entries as functions. |
| `vue/require-toggle-inside-transition` | Ensure transition content has a mechanism controlling its visibility. |
| `vue/require-typed-ref` | Give ref and shallowRef values a strong inferred or explicit type. |
| `vue/require-v-for-key` | Key presence on repeated items; stable/unique values still need review. |
| `vue/require-valid-default-prop` | Make each prop's default value appropriate for its declared type. |
| `vue/return-in-computed-property` | Return a value from computed getters. |
| `vue/return-in-emits-validator` | Return a validation result from emit validators. |
| `vue/this-in-template` | Avoid explicit this qualifiers in template bindings under the default policy. |
| `vue/use-v-on-exact` | Apply exact event-modifier handling where needed to distinguish modifier combinations. |
| `vue/v-bind-style` | Shorthand; same-name shorthand follows the preset default (not required). |
| `vue/v-on-event-hyphenation` | Kebab-case listeners; autofix enabled. |
| `vue/v-on-style` | Choose a consistent spelling of event directives. |
| `vue/v-slot-style` | Shorthand for component default, template default, and named slots. |
| `vue/valid-attribute-name` | Use syntactically valid attribute names. |
| `vue/valid-define-emits` | Keep defineEmits calls within the compiler macro's permitted forms. |
| `vue/valid-define-options` | Keep defineOptions calls within the compiler macro's permitted forms. |
| `vue/valid-define-props` | Keep defineProps calls within the compiler macro's permitted forms. |
| `vue/valid-next-tick` | Use supported nextTick invocation patterns. |
| `vue/valid-template-root` | Give the template a root structure valid for the target Vue version. |
| `vue/valid-v-bind` | Use v-bind with valid arguments, values and modifiers. |
| `vue/valid-v-cloak` | Use v-cloak only in its permitted directive form. |
| `vue/valid-v-else` | Place v-else as a valid final branch of a condition chain. |
| `vue/valid-v-else-if` | Place and express v-else-if as a valid continuation of a condition chain. |
| `vue/valid-v-for` | Use valid loop bindings and expressions for v-for. |
| `vue/valid-v-html` | Use v-html with its required expression and permitted placement. |
| `vue/valid-v-if` | Use v-if with a valid condition and directive form. |
| `vue/valid-v-is` | Keep legacy v-is use syntactically valid where that directive exists. |
| `vue/valid-v-memo` | Use v-memo only with supported values and placement. |
| `vue/valid-v-model` | Use v-model on supported writable targets with valid arguments and modifiers. |
| `vue/valid-v-on` | Supply valid event binding expressions and modifiers. |
| `vue/valid-v-once` | Use v-once only in its supported directive form. |
| `vue/valid-v-pre` | Use v-pre only in its supported directive form. |
| `vue/valid-v-show` | Supply a valid expression and placement for v-show. |
| `vue/valid-v-slot` | Declare slots with valid placement, arguments and scope bindings. |
| `vue/valid-v-text` | Supply v-text with a valid value and directive form. |

`reportUnusedDisableDirectives: error` is inherited. Prettier's inherited option IDs are `printWidth`, `tabWidth`, `useTabs`, `semi`, `singleQuote`, `trailingComma`, `arrowParens`, and `endOfLine`; there are no Vue-specific formatter overrides. The TypeScript guide maps the inherited compiler option IDs. The Vue leaf adds `vueCompilerOptions.target: 3.5` and `vueCompilerOptions.strictTemplates: true`; these are compiler options, not ESLint rules. [VUE-LINT-CONFIG] [PRETTIER] [VUE-TS]

The final Prettier layer disables Vue's layout checks: `vue/html-closing-bracket-newline`, `vue/html-closing-bracket-spacing`, `vue/html-end-tags`, `vue/html-indent`, `vue/html-quotes`, `vue/html-self-closing`, `vue/max-attributes-per-line`, `vue/multiline-html-element-content-newline`, `vue/mustache-interpolation-spacing`, `vue/no-multi-spaces`, `vue/no-spaces-around-equal-signs-in-attribute`, and `vue/singleline-html-element-content-newline`. The released Prettier compatibility config does not disable `vue/first-attribute-linebreak`, so this addition disables it explicitly. `vue/require-default-prop` is also off: an optional prop may intentionally remain absent. Removed `vue/script-setup-uses-vars` is not configured; the parser tracks template uses. [VUE-LINT] [PRETTIER]

Review still checks key stability/uniqueness, PascalCase filenames/import aliases, actual script-setup-only organization, deep mutation through aliases, class-scoped CSS boundaries, watch cancellation, required injection handling, error fallback behavior, public contract documentation, and DOM accessibility. Lint cannot prove them. Type-aware script rules do not automatically analyze every template expression; `vue/eqeqeq` explicitly covers template equality, while vue-tsc checks template types. [VUE-LINT-CONFIG] [VUE-LINT] [VUE-TS]

## Naming

- MUST use PascalCase filenames and component bindings with multi-word names, except the root `App.vue`. Why: component identities remain distinct from native elements. [VUE-STYLE] [VUE-LINT]
- MUST use PascalCase tags for locally imported components in SFC templates. Why: component references stand out from HTML tags. [VUE-STYLE] [VUE-LINT]
- MUST declare props in camelCase and pass component prop attributes in kebab-case. Why: one declaration/use convention removes SFC casing choices. [VUE-STYLE] [VUE-LINT]
- MUST emit ordinary custom events in camelCase and listen with kebab-case attributes, preserving Vue model events such as `update:modelValue`. Why: event conventions must retain framework contracts. [VUE-LINT] [VUE-MODEL]
- PREFER `Base` prefixes for application primitives and parent-name prefixes for tightly coupled child components. Why: names expose reuse and ownership boundaries. [VUE-STYLE]
- MUST name composables `useX` and keep them in TypeScript modules. Why: callers can recognize functions that own reactive behavior. [VUE-COMPOSABLES]

## Files and layout

- MUST write each component as one `.vue` SFC using `<script setup lang="ts">` and Composition API. Why: one component model gives templates direct typed bindings. [VUE-SFC] [VUE-LINT]
- MUST order SFC blocks as script, template, then styles. Why: contracts and state appear before their rendering and styling. [VUE-STYLE] [VUE-LINT]
- MUST import child components directly in script setup and register custom directives explicitly. Why: template dependencies remain resolvable by tooling. [VUE-SFC] [VUE-LINT]
- MUST use compiler macros without importing them and put component options in `defineOptions`. Why: macros are compiler syntax, not runtime Vue exports. [VUE-SFC] [VUE-LINT]
- MUST keep module exports in separate `.ts` modules rather than script setup. Why: script setup executes per instance and does not support module exports. [VUE-SFC] [VUE-LINT]
- MUST use `scoped` styles or CSS Modules for ordinary application SFC styles, with plain CSS limited to explicitly configured App/layout/library paths. Why: ordinary component styles must not leak globally. [VUE-STYLE] [VUE-LINT]
- PREFER distinctive class-based scoping for reusable library CSS and class selectors inside scoped styles. Why: consumers can override library styles and selectors stay tied to component intent. [VUE-STYLE]
- PREFER composables over mixins for reusable reactive logic, returning a plain object of refs when callers destructure results. Why: explicit bindings preserve dependencies and reactive connections. [VUE-COMPOSABLES]

## Types and data

- MUST declare props with `defineProps<Props>()` and emitted payloads with a typed `defineEmits` event-to-tuple map. Why: consumers get checked component inputs and outputs. [VUE-TS] [VUE-LINT]
- MUST destructure declared props with `const { value = fallback } = defineProps<Props>()`, using defaults only when meaningful. Why: Vue 3.5 preserves reactive reads and supports per-instance defaults in this syntax. [VUE-PROPS] [VUE-TS] [VUE-LINT]
- MUST leave incoming props and their nested objects/arrays unmodified; request owner updates through declared events. Why: child writes otherwise bypass the parent's state ownership. [VUE-PROPS] [VUE-LINT]
- MUST preserve meaningful absence in optional props; destructured object/array defaults need no factory, while legacy `withDefaults` defaults do. Why: the compiler creates destructured defaults per instance without inventing absent values. [VUE-SFC] [VUE-TS]
- PREFER `ref` for component state and read or write `.value` in script; top-level template refs unwrap automatically. Why: ref identity survives value replacement. [VUE-REACTIVITY]
- MUST give `ref` and `shallowRef` an inferable initial type or an explicit generic, including nullability where needed. Why: empty initialization must not create untyped mutable state. [VUE-TS] [VUE-LINT]
- MUST keep computed getters synchronous, side-effect-free, and value-returning. Why: cached derivation must not start asynchronous work or mutate its inputs. [VUE-REACTIVITY] [VUE-LINT]
- MUST pass a ref or getter such as `() => id` for a destructured prop to watchers and reactive composables, not its current value `id`. Why: later prop changes must remain observable. [VUE-WATCH] [VUE-COMPOSABLES]
- MUST use `useTemplateRef` for static template refs and handle null before accessing their value. Why: elements can be absent before mount or after conditional removal. [VUE-TEMPLATE-REFS] [VUE-LINT]
- MUST declare the component's slot outlets with `defineSlots` and type their slot props. Why: callers need a checked slot interface as well as checked ordinary props. [VUE-SFC] [VUE-LINT]
- MUST use shared `InjectionKey<T>` symbols for typed injection and check an absent required provider explicitly. Why: a type parameter cannot guarantee a provider exists. [VUE-TS]
- MUST avoid child-only defaults in `defineModel`; initialize defaults in the owning parent. Why: otherwise parent and child model values can start out different. [VUE-MODEL] [VUE-LINT]

## Errors

- MUST render an error boundary's fallback without the failing descendant, and return `false` from `onErrorCaptured` only after deliberately handling/reporting that failure. Why: rendering the same failing subtree can loop and `false` stops further propagation. [VUE-LIFECYCLE]
- PREFER `app.config.errorHandler` for reporting unhandled Vue lifecycle/render failures and explicit loading/error state for expected request failures. Why: Vue's runtime boundary and user-visible recovery serve different failure paths. [VUE-LIFECYCLE] [VUE-COMPOSABLES]
- MUST cancel or invalidate stale asynchronous watcher work and register `onWatcherCleanup` before the first await. Why: a superseded request must not overwrite current component state. [VUE-WATCH]

## Comments and docs

- PREFER JSDoc on public prop interfaces and composable signatures explaining prop defaults, event payload meaning, slot props, and reactive input expectations. Why: those Vue contracts are not apparent from the rendered DOM. [VUE-TS] [VUE-COMPOSABLES]
- MUST describe any imperative component interface exposed by `defineExpose`, including mount/unmount limits. Why: parent template refs otherwise create an undocumented dependency on child internals. [VUE-TEMPLATE-REFS]

## Testing

- PREFER Vitest with @vue/test-utils for component/composable tests and Playwright for browser checks. Why: the Vue-supported stack covers public component behavior and real browser interactions. [VUE-TEST]

Starting pins: [Vitest 5.0.5](https://github.com/vitest-dev/vitest/releases/tag/v5.0.5), [@vue/test-utils 2.5.1](https://github.com/vuejs/test-utils/releases/tag/v2.5.1), and [Playwright 1.64.1](https://github.com/microsoft/playwright/releases/tag/v1.64.1). Resolve compatible Vite/Vue-plugin/DOM-environment packages in the application lockfile; no installation or component-test pass is claimed here.

- MUST test Vue components through rendered DOM, supplied props/slots, and emitted events instead of private `wrapper.vm` state. Why: the component's public behavior should survive refactoring. [VUE-TEST]
- MUST await Vue Test Utils updates such as `trigger`, `setValue`, and `setProps`, then flush external promises when relevant. Why: Vue DOM batching and asynchronous services settle independently. [VUE-TEST]
- PREFER focused cases for prop replacement, list reordering, conditional ref removal, and stale async results when changing those behaviors. Why: these transitions expose Vue identity and lifecycle defects. [VUE-PROPS] [VUE-WATCH] [VUE-TEMPLATE-REFS]
- MUST verify rendered component accessibility and native interaction in the application's browser tests where DOM simulation is insufficient. Why: template lint cannot establish focus, layout, or assistive-technology behavior. [VUE-TEST] [WCAG22]

## Performance

- PREFER computed derivation over watchers that merely copy one reactive value into another. Why: computed values track dependencies without synchronization bookkeeping. [VUE-REACTIVITY]
- PREFER stable child props, lazy loading of noninitial component trees, and virtualization for genuinely large lists. Why: these reduce update work, initial downloads, and mounted nodes. [VUE-PERFORMANCE]
- MUST treat shallow reactive structures' nested data as immutable; replace a `shallowRef`'s `.value` or a `shallowReactive` object's top-level property to trigger updates. Why: shallow tracking deliberately omits nested mutation notifications. [VUE-PERFORMANCE]

## Security

- MUST render text through interpolation and keep `v-html` out of ordinary components; never compile untrusted strings as Vue templates. Why: raw markup and executable templates bypass Vue's safe text rendering. [VUE-SECURITY] [VUE-LINT]
- MUST mount Vue only into application-controlled DOM and constrain URL/style bindings before rendering untrusted values. Why: escaping does not make existing templates, dangerous URL schemes, or arbitrary CSS safe. [VUE-SECURITY]

## Language-specific pitfalls

- MUST give each `v-for` item a unique, stable primitive key, placing the key on the `template v-for` wrapper for grouped siblings. Why: identity must follow the item when the list changes. [VUE-STYLE] [VUE-LINT]
- MUST keep `v-if`, `v-else-if`, and `v-else` off elements carrying `v-for`; filter with computed data or use a separate wrapper. Why: Vue 3 evaluates `v-if` before the iteration scope exists. [VUE-STYLE] [VUE-LINT]
- PREFER simple template expressions, moving branching or repeated computation into named computed values or functions. Why: templates should make rendering relationships easy to inspect. [VUE-STYLE]
- MUST use `:`, `@`, and `#` directive shorthands consistently, including `#default` for explicit default-slot bindings. Why: one supported spelling keeps template conventions predictable. [VUE-STYLE] [VUE-LINT]
- MUST register lifecycle hooks and component-owned watchers synchronously during setup; call lifecycle-dependent composables there too. Why: Vue needs the active component to own and dispose of them. [VUE-LIFECYCLE] [VUE-WATCH] [VUE-COMPOSABLES]
- MUST dispose of manually created subscriptions, timers, listeners, and asynchronously created watchers through their owning composable's cleanup. Why: Vue only automatically stops effects it owns. [VUE-COMPOSABLES] [VUE-WATCH]
- MUST read all dependencies needed by an async `watchEffect` before its first await, or use `watch` with explicit sources. Why: later reads are outside automatic dependency collection. [VUE-WATCH]
- MUST await `nextTick` or use a post-flush watcher before observing DOM changes caused by reactive writes. Why: Vue batches DOM updates instead of applying them synchronously. [VUE-REACTIVITY] [VUE-WATCH]
- MUST set `inheritAttrs: false` when deliberately forwarding `$attrs` and choose the receiving element explicitly for multi-root components. Why: automatic fallthrough can duplicate attributes or lack a single target. [VUE-LINT]
- MUST give template buttons an explicit `type`. Why: an embedded component must not accidentally submit its enclosing form. [VUE-LINT]
- MUST use Vue 3 APIs and keyed fragment loops rather than Vue 2 filters, `.sync`, `.native`, instance event buses, or single-root restrictions. Why: the older syntax and lifecycle assumptions do not describe this baseline. [VUE-LINT]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- PREFER class-scoped library CSS with explicit `plainStyleFiles` paths when the style guide's library recommendation conflicts with `enforce-style-attribute`'s scoped-only default; ordinary app SFCs use scoped styles or CSS Modules. Why: the selected override preserves consumer theming and application isolation. [VUE-STYLE] [VUE-LINT]
- MUST use kebab-case prop attributes in SFCs although the style guide also accepts consistent camelCase and the lint default selects hyphenation. Why: the enforced default gives agents one spelling. [VUE-STYLE] [VUE-LINT]
- MUST let the inherited Prettier config decide script/attribute quoting instead of applying the style guide's opposing-quote rule or `vue/html-quotes` separately. Why: one formatter owns mechanical output; the current single-quoted-script default already avoids the cited combination. [VUE-STYLE] [VUE-LINT] [PRETTIER]
- MUST choose directive shorthand although the style guide permits consistent long forms and the lint defaults choose shorthand. Why: the explicit `:`, `@`, and `#` settings remove a needless alternative. [VUE-STYLE] [VUE-LINT]
- MUST prohibit nested and direct prop mutation despite the style guide's tightly coupled component exception and the optional `shallowOnly` relaxation. Why: events preserve a single state owner and allow consistent enforcement. [VUE-STYLE] [VUE-LINT]
- MUST key native-element loops as well as component loops despite the style guide's rare performance exception and the essential rule's unconditional key requirement. Why: predictable identity is the baseline and key presence is checkable. [VUE-STYLE] [VUE-LINT]
- MUST reject same-element `v-if`/`v-for` even where `allowUsingIterationVar` could relax the lint check. Why: the style guide's prohibition matches Vue 3 precedence and the relaxed check does not change runtime semantics. [VUE-STYLE] [VUE-LINT]
- MUST choose TypeScript script setup and Composition API although the style/typing guides also support Options API and the lint option permits several API families. Why: one authoring model keeps components, types, and lint rules uniform. [VUE-STYLE] [VUE-TS] [VUE-LINT]
- MUST choose type-based props for typed SFCs over the style guide's runtime-constructor examples and the lint rule's selectable runtime mode. Why: TypeScript defines the component contract once; runtime trust-boundary validation remains separate. [VUE-STYLE] [VUE-TS] [VUE-LINT]
- MUST use reactive props destructuring with `destructure: always`, following Vue 3.5's documented defaults; the plugin default `only-when-assigned` requires destructuring only when assigning the result. Why: this selected 3.5+ profile uses supported compiler behavior consistently. [VUE-TS] [VUE-LINT]
- MUST use PascalCase component tags in compiled SFCs although the style guide accepts consistent kebab-case and the lint rule supports either. Why: the default separates imported components from platform elements. [VUE-STYLE] [VUE-LINT]

Version and context notes: Vue 3 permits fragments, `v-model` arguments, and keyed `template v-for`; `no-template-key` exempts that wrapper. Compiler-transformed `defineProps` destructuring is reactive in Vue 3.5+, unlike ordinary `setup(props)` snapshots; getters still preserve tracking across watcher/composable call boundaries. Template quotation and JSX preservation concern different layers. The legacy option-order categories are not a new conflict and are mostly irrelevant to script setup. The current style-guide snapshot has no due-for-review banner; older warning text is not adopted as current evidence. [VUE-SFC] [VUE-PROPS] [VUE-TS] [VUE-STYLE] [VUE-LINT]
