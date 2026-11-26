# React style guide

Scope: React/React DOM 19.3 browser applications and reusable components, using TypeScript 6.0.3 and the automatic JSX runtime. React Compiler adoption is optional; compiler-aware linting is included. Client form Actions are included. React Native, framework routing, Server Components, and Server Functions need additional project profiles. Build/test tools use Node 24 LTS or a newer supported release.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

## Quick rules

- MUST write new ordinary React components as named function declarations in `.tsx`; reserve classes for capabilities such as Error Boundaries. Why: Hooks support stateful functions and explicit names aid tooling. [REACT-COMPONENT] [REACT-LINT]
- PREFER PascalCase component names and matching `ComponentName.tsx` filenames, with `useThing.ts` for non-JSX Hooks. Why: imports identify components and Hooks consistently. [AIRBNB-REACT] [REACT-RULES]
- MUST declare typed component props, including accepted children, and use parameter defaults when a function prop needs a fallback; do not rely on `propTypes` or function `defaultProps`. Why: React 19 removed those runtime mechanisms for functions. [REACT19] [BULLETPROOF]
- MUST render components through JSX instead of calling component functions directly. Why: React owns their identity, state, and scheduling. [REACT-RULES]
- MUST call ordinary Hooks unconditionally at the top level of function components or custom Hooks, before early returns. Why: React associates state with stable call order. [REACT-RULES]
- MUST keep `use` inside a component or Hook and outside `try/catch`; any promise passed to it must come from a cache, loader, or parent with stable identity across rerenders, never be created during render. Why: new promises repeatedly suspend; `use` permits conditions and loops. [REACT-HOOKS]
- MUST keep repeated render calculations idempotent and free of observable side effects, including time/random generation and global writes. Why: React may restart or discard rendering. [REACT-RULES]
- MUST treat React props, state, Hook arguments/results, and values already passed into JSX as immutable snapshots. Why: React relies on those snapshots for consistent rendering and caching. [REACT-RULES]
- MUST define components and Hooks at module scope; pass changing data as props instead of creating component types during render. Why: changing type identity resets state. [REACT-HOOKS] [REACT-LINT]
- PREFER deriving display values from current props/state during render instead of storing synchronized copies in state. Why: duplicate state creates stale passes and Effect chains. [REACT-EFFECTS]
- MUST put interaction-triggered submissions and parent notifications in the relevant event handler or form Action. Why: an Effect cannot reliably identify which interaction caused a render. [REACT-EFFECTS]
- MUST use Effects for external synchronization and return cleanup that reverses subscriptions, timers, or other acquired resources. Why: dependencies, unmounts, and Strict Mode can repeat setup. [REACT-EFFECT-API]
- MUST include every reactive value used by an Effect, memo, or callback in its dependency list; restructure logic rather than omitting dependencies. Why: missing dependencies capture stale values. [REACT-HOOKS]
- MUST prevent outdated asynchronous Effect results from committing after cleanup or a newer request. Why: responses can arrive out of order. [REACT-EFFECTS]
- MUST access `ref.current` outside render except for guarded, predictable one-time initialization; keep display-driving values in state. Why: ref writes do not request a render. [REACT-HOOKS]
- PREFER keeping component state with its consumers and lifting shared state to their lowest common owner. Why: one owner avoids synchronization between duplicate stores. [BULLETPROOF] [REACT-EFFECTS]
- MUST use stable data-derived keys unique among siblings; never use array indexes, render-generated randomness, or `useId` for list keys. Why: keys preserve each item's state across updates. [REACT-LISTS] [REACT-ID] [REACT-LINT]
- MUST keep each input controlled or uncontrolled for its lifetime; controlled text/checked values need synchronous `onChange` updates unless read-only. Why: switching ownership or delaying the update breaks input behavior. [REACT-DOM]
- MUST preserve native semantics and accessible names through JSX wrappers, including forwarding label, ARIA, and focus-related props to the intended DOM element. Why: a component name alone conveys no browser semantics. [JSX-A11Y] [REACT-DOM]
- MUST use Error Boundaries for descendant rendering failures and handle event/request failures in their own handlers. Why: `try/catch` around JSX does not catch later child renders. [REACT-COMPONENT] [REACT-HOOKS]
- MUST keep `dangerouslySetInnerHTML` out of ordinary components; isolate any necessary sanitized rich HTML in a reviewed adapter. Why: that API bypasses React's text escaping. [REACT-DOM] [REACT-LINT]
- MUST exercise Effect setup, cleanup, and remounting under Strict Mode when testing synchronization. Why: repeated development lifecycles reveal leaked subscriptions and nonrepeatable work. [REACT-EFFECT-API]
- PREFER purpose-specific custom Hooks over wrappers exposing generic callback/dependency-array scheduling. Why: domain APIs keep synchronization details inside one implementation. [REACT-HOOKS-SOURCE] [REACT-EFFECTS]
- MUST make component correctness independent of `useMemo`, `useCallback`, and `memo`; memo calculations must be pure and return their computed value. Why: memoization is an optimization, not a lifecycle or state guarantee. [REACT-MEMO] [REACT-HOOKS]
- MUST accept a forwarded `ref` as an ordinary typed prop in new function components and pass it to the intended DOM element; do not add `forwardRef`. Why: React 19 supports ref props directly. [React: forwardRef](https://react.dev/reference/react/forwardRef)

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Prettier 3.9.10, inherited | [Root web `.prettierrc.json`](config/.prettierrc.json) | `npx prettier --check .` |
| Linter | ESLint / @eslint/js 9.39.5; typescript-eslint 8.72.1; eslint-config-prettier 10.1.8; eslint-plugin-react 7.37.5; eslint-plugin-react-hooks 7.1.1; eslint-plugin-jsx-a11y 6.10.2 | [React additions](config/eslint.config.js) over [TypeScript base](config/typescript/eslint.config.js) | `npx eslint --max-warnings 0 .` |
| Build / type checks | TypeScript 6.0.3; @types/react and @types/react-dom 19.3.0 | project `tsconfig.json` extends the strict base | `npx tsc --noEmit` |
| Tests | Vitest 5.0.5 + React Testing Library + MSW; Playwright 1.64.1 for browsers | Project's test configuration and lockfile | Project's component, integration, and browser test commands |

Mechanical formatting: the formatter handles this. Copy [the single web config](config/.prettierrc.json) to the consuming repository root as `.prettierrc.json`; do not add competing language configs. TypeScript/TSX and Vue scripts use `singleQuote: true`; standalone `*.css` uses `false`. Vue `<style>` uses the SFC's `true` setting too. Only `*.html` disables embedded-language formatting; Vue scripts/styles remain formatted. [PRETTIER]

Run these commands from the project root after adopting the configs and resolving the exact tool and React/React DOM versions in the project's manifests and lockfile. The JSX accessibility plugin supplies checks missing from the two React plugins. [REACT-LINT] [JSX-A11Y]

Dated exception (2026-10-31): **EOL since 2026-08-06; revisit when eslint-plugin-react and jsx-a11y declare ESLint 10.** Pin ESLint and @eslint/js to 9.39.5 for React, including the shared TypeScript factory's dependencies at the common project root. The React 7.37.5 and jsx-a11y 6.10.2 peer ranges stop at ESLint 9; this is the house compatibility exception, not a maintained ESLint baseline. See [version support](https://eslint.org/version-support/) and [9.39.5 recommended source](https://github.com/eslint/eslint/blob/v9.39.5/packages/js/src/configs/eslint-recommended.js).

The config exports `createReactConfig({ files, tsconfigRootDir, additionalEffectHooks })`. Copy both the React and TypeScript config modules, preserve or adjust their relative import, and call the factory with the consuming root, usually `import.meta.dirname`. Its default root is the config module directory; pass the consuming project root explicitly. ESM `.js` needs `"type": "module"`; `.mjs` is an alternative, with imports adjusted. Typed files, including tests and Hooks without JSX, need a discoverable leaf `tsconfig.json`. JS tooling files are outside this profile. The full inherited rule-ID and compiler-option inventory is in [TypeScript Tooling](related/typescript.md#eslint-enforcement-inventory); the React 9 preset retains 147 TypeScript/core rules. The ESLint 10-only recommended additions `no-unassigned-vars`, `no-useless-assignment`, and `preserve-caught-error` in that table are absent here. [ESLINT] [TS-ESLINT-COMPAT]

For this browser profile, set the project tsconfig to `module: ESNext`, `moduleResolution: Bundler`, `lib: [ES2022, DOM, DOM.Iterable]`, `jsx: react-jsx`, and React type packages. `jsx` selects the automatic runtime; the other options define resolution and browser types, not extra lint checks. Framework builds may require `jsx: preserve` while performing the automatic transform themselves. Browser globals are checked by TypeScript's DOM library; the typed base disables core `no-undef`, so a separate globals package is unnecessary here. The root web Prettier options apply, including its CSS and HTML overrides. [TS-CONFIG] [REACT19]

- MUST use the automatic JSX transform with this React 19 profile; import React APIs/types only when referenced. Why: the runtime transform no longer needs a React namespace import solely for JSX. [REACT19] [REACT-LINT]
- MUST lint custom Hooks in `.ts` as well as components in `.tsx`. Why: Hook order and dependency bugs do not require JSX syntax. [REACT-HOOKS]
- MUST register actual custom Effect wrappers through shared `settings['react-hooks'].additionalEffectHooks`, using a precise expression such as `^(useDebouncedEffect)$`. Why: order and dependency checks need the same wrapper names. [REACT-HOOKS]
- MUST map custom DOM wrappers in `settings['jsx-a11y'].components` and link/form wrappers in the React plugin settings when adopting them. Why: static checks otherwise cannot see the DOM semantics or destinations behind wrappers. [JSX-A11Y] [REACT-LINT]
- MUST use the [rendered HTML profile](related/html.md#rendered-output-validation) for framework-generated `useId` values while retaining uniqueness and reference checks. Why: generated identifiers do not follow authored-ID naming conventions. [REACT-ID] [HTML-VALIDATE]

No custom Effect names or wrapper mappings are invented by the supplied config. The factory's optional `additionalEffectHooks` argument supplies the shared setting; legacy rule-level `additionalHooks` takes precedence, so it is absent. A custom Hook that owns its dependencies internally needs no registration. [REACT-HOOKS]

### Inherited TypeScript rule IDs

These 147 errors remain enabled for the React ESLint 9 typed file scope, including the TypeScript tool-config default-export exception. Their options and individual meanings are documented in [TypeScript Tooling](related/typescript.md#eslint-enforcement-inventory); the list here makes the complete combined lint inventory explicit. `reportUnusedDisableDirectives: error` also detects unused suppressions. [ESLINT] [TS-ESLINT]

```text
@typescript-eslint/adjacent-overload-signatures
@typescript-eslint/array-type
@typescript-eslint/await-thenable
@typescript-eslint/ban-ts-comment
@typescript-eslint/ban-tslint-comment
@typescript-eslint/class-literal-property-style
@typescript-eslint/consistent-generic-constructors
@typescript-eslint/consistent-indexed-object-style
@typescript-eslint/consistent-type-assertions
@typescript-eslint/consistent-type-definitions
@typescript-eslint/consistent-type-exports
@typescript-eslint/dot-notation
@typescript-eslint/explicit-member-accessibility
@typescript-eslint/explicit-module-boundary-types
@typescript-eslint/no-array-constructor
@typescript-eslint/no-array-delete
@typescript-eslint/no-base-to-string
@typescript-eslint/no-confusing-non-null-assertion
@typescript-eslint/no-confusing-void-expression
@typescript-eslint/no-deprecated
@typescript-eslint/no-duplicate-enum-values
@typescript-eslint/no-duplicate-type-constituents
@typescript-eslint/no-dynamic-delete
@typescript-eslint/no-empty-function
@typescript-eslint/no-empty-object-type
@typescript-eslint/no-explicit-any
@typescript-eslint/no-extra-non-null-assertion
@typescript-eslint/no-extraneous-class
@typescript-eslint/no-floating-promises
@typescript-eslint/no-for-in-array
@typescript-eslint/no-generated-empty-object-type
@typescript-eslint/no-implied-eval
@typescript-eslint/no-import-type-side-effects
@typescript-eslint/no-inferrable-types
@typescript-eslint/no-invalid-void-type
@typescript-eslint/no-meaningless-void-operator
@typescript-eslint/no-misused-new
@typescript-eslint/no-misused-promises
@typescript-eslint/no-misused-spread
@typescript-eslint/no-mixed-enums
@typescript-eslint/no-namespace
@typescript-eslint/no-non-null-asserted-nullish-coalescing
@typescript-eslint/no-non-null-asserted-optional-chain
@typescript-eslint/no-non-null-assertion
@typescript-eslint/no-redundant-type-constituents
@typescript-eslint/no-require-imports
@typescript-eslint/no-this-alias
@typescript-eslint/no-unnecessary-boolean-literal-compare
@typescript-eslint/no-unnecessary-condition
@typescript-eslint/no-unnecessary-template-expression
@typescript-eslint/no-unnecessary-type-arguments
@typescript-eslint/no-unnecessary-type-assertion
@typescript-eslint/no-unnecessary-type-constraint
@typescript-eslint/no-unnecessary-type-conversion
@typescript-eslint/no-unnecessary-type-parameters
@typescript-eslint/no-unsafe-argument
@typescript-eslint/no-unsafe-assignment
@typescript-eslint/no-unsafe-call
@typescript-eslint/no-unsafe-declaration-merging
@typescript-eslint/no-unsafe-enum-assignment
@typescript-eslint/no-unsafe-enum-comparison
@typescript-eslint/no-unsafe-function-type
@typescript-eslint/no-unsafe-member-access
@typescript-eslint/no-unsafe-return
@typescript-eslint/no-unsafe-unary-minus
@typescript-eslint/no-unused-expressions
@typescript-eslint/no-unused-vars
@typescript-eslint/no-useless-constructor
@typescript-eslint/no-useless-default-assignment
@typescript-eslint/no-wrapper-object-types
@typescript-eslint/only-throw-error
@typescript-eslint/prefer-as-const
@typescript-eslint/prefer-find
@typescript-eslint/prefer-for-of
@typescript-eslint/prefer-function-type
@typescript-eslint/prefer-includes
@typescript-eslint/prefer-literal-enum-member
@typescript-eslint/prefer-namespace-keyword
@typescript-eslint/prefer-nullish-coalescing
@typescript-eslint/prefer-optional-chain
@typescript-eslint/prefer-promise-reject-errors
@typescript-eslint/prefer-readonly
@typescript-eslint/prefer-reduce-type-parameter
@typescript-eslint/prefer-regexp-exec
@typescript-eslint/prefer-return-this-type
@typescript-eslint/prefer-string-starts-ends-with
@typescript-eslint/related-getter-setter-pairs
@typescript-eslint/require-await
@typescript-eslint/restrict-plus-operands
@typescript-eslint/restrict-template-expressions
@typescript-eslint/return-await
@typescript-eslint/strict-boolean-expressions
@typescript-eslint/switch-exhaustiveness-check
@typescript-eslint/triple-slash-reference
@typescript-eslint/unbound-method
@typescript-eslint/unified-signatures
@typescript-eslint/use-unknown-in-catch-callback-variable
eqeqeq
for-direction
no-async-promise-executor
no-case-declarations
no-compare-neg-zero
no-cond-assign
no-constant-binary-expression
no-constant-condition
no-control-regex
no-debugger
no-delete-var
no-dupe-else-if
no-duplicate-case
no-empty
no-empty-character-class
no-empty-pattern
no-empty-static-block
no-eval
no-ex-assign
no-extend-native
no-extra-boolean-cast
no-fallthrough
no-global-assign
no-invalid-regexp
no-irregular-whitespace
no-loss-of-precision
no-misleading-character-class
no-new-func
no-nonoctal-decimal-escape
no-octal
no-prototype-builtins
no-regex-spaces
no-restricted-syntax
no-self-assign
no-shadow-restricted-names
no-sparse-arrays
no-unsafe-finally
no-unsafe-optional-chaining
no-unused-labels
no-unused-private-class-members
no-useless-backreference
no-useless-catch
no-useless-escape
no-var
prefer-const
prefer-rest-params
prefer-spread
require-yield
use-isnan
valid-typeof
```

### React rule IDs

These 33 checks are enabled at error severity after `react.configs.flat.recommended`, `jsx-runtime`, and house overrides. Descriptions summarize coverage, not complete static proofs. [REACT-LINT]

| Rule ID | Check / configured scope |
| --- | --- |
| `react/button-has-type` | Explicit valid type on native buttons. |
| `react/display-name` | Discoverable names for recognized component definitions. |
| `react/function-component-definition` | Named components use declarations; anonymous component expressions use arrows. |
| `react/jsx-filename-extension` | JSX is allowed only in `.tsx` within the typed file scope. |
| `react/jsx-key` | Keys on lists, including shorthand fragments; statically visible duplicate keys. |
| `react/jsx-no-comment-textnodes` | Accidental comment syntax rendered as text. |
| `react/jsx-no-duplicate-props` | Duplicate explicit JSX props. |
| `react/jsx-no-script-url` | Detectable `javascript:` URLs. |
| `react/jsx-no-target-blank` | External/dynamic link destinations opening a new tab require `noreferrer` by the preset; form/spread checks are not enabled by default. |
| `react/jsx-no-undef` | Undeclared JSX identifiers. |
| `react/jsx-pascal-case` | PascalCase component references; not filename casing. |
| `react/jsx-uses-vars` | Marks JSX component variables as used. |
| `react/no-access-state-in-setstate` | Stale `this.state` reads in class `setState` arguments. |
| `react/no-array-index-key` | Recognizable array indexes used as keys. |
| `react/no-children-prop` | Explicit `children` attributes instead of nested JSX. |
| `react/no-danger` | `dangerouslySetInnerHTML` outside a reviewed, narrowly overridden adapter. |
| `react/no-danger-with-children` | Supplying both children and raw inner HTML. |
| `react/no-deprecated` | Known deprecated React APIs; not an exhaustive React 19 migration check. |
| `react/no-direct-mutation-state` | Direct class-state mutation; Hooks mutation has separate checks. |
| `react/no-find-dom-node` | Removed `findDOMNode` use. |
| `react/no-is-mounted` | Obsolete `isMounted` calls. |
| `react/no-object-type-as-default-prop` | Fresh array/object/function defaults created in component parameter lists. |
| `react/no-render-return-value` | Reliance on legacy `ReactDOM.render` return values. |
| `react/no-string-refs` | Legacy string refs. |
| `react/no-this-in-sfc` | `this` inside function components. |
| `react/no-unescaped-entities` | Ambiguous JSX text characters; express intended text as JSX strings/entities. |
| `react/no-unknown-property` | Unknown or misspelled native DOM props. |
| `react/no-unsafe` | Recognized unsafe class lifecycles. |
| `react/no-unstable-nested-components` | Nested component definitions; `allowAsProps: false` retains the default `render*` callback exception, with detection limits. |
| `react/prefer-stateless-function` | Classes without class-only needs; does not ban every new stateful class. |
| `react/require-render-return` | A class `render` method returns a result. |
| `react/style-prop-object` | An object for the DOM `style` prop. |
| `react/void-dom-elements-no-children` | Children/raw HTML on void DOM elements. |

`react/prop-types` and `react/require-default-props` are off for typed React 19 functions. `react/react-in-jsx-scope` and `react/jsx-uses-react` are off through `jsx-runtime`. There is no `no-multi-comp`, class-ordering, prop-spread ban, or blanket inline-handler ban. `react/jsx-no-leaked-render` is omitted because inherited `@typescript-eslint/strict-boolean-expressions` already checks JSX condition operands with real types; the untyped React rule can flag valid Boolean variables. [REACT-LINT] [REACT19]

### Hooks and compiler rule IDs

The stable `reactHooks.configs.flat.recommended` profile supplies 16 active checks for the selected 7.1.1 line. `exhaustive-deps`, `incompatible-library`, and `unsupported-syntax` are promoted from warnings to errors; all listed checks block this new-code profile. This does not turn on React Compiler in the application build. Existing applications can stage adoption in their own explicitly scoped migration profile. [REACT-HOOKS] [REACT-HOOKS-SOURCE]

| Rule ID | Check / configured scope |
| --- | --- |
| `react-hooks/config` | Compiler options supplied to lint analysis. |
| `react-hooks/error-boundaries` | Invalid attempts to catch child rendering with `try/catch`. |
| `react-hooks/exhaustive-deps` | Dependencies and supported custom Effect wrappers. |
| `react-hooks/gating` | Compiler gate configuration when supplied. |
| `react-hooks/globals` | Recognized global mutation during render. |
| `react-hooks/immutability` | Recognized mutation of React snapshots and immutable values. |
| `react-hooks/incompatible-library` | Known memoization-incompatible APIs; does not detect all libraries, including some MobX observer use. |
| `react-hooks/preserve-manual-memoization` | Existing manual cache dependencies/dataflow that compilation cannot preserve. |
| `react-hooks/purity` | Known impure operations in rendering. |
| `react-hooks/refs` | Inferred ref reads/writes during render, with the lazy-initialization exception. |
| `react-hooks/rules-of-hooks` | Hook placement and order, including the distinct `use` restrictions. |
| `react-hooks/set-state-in-effect` | Synchronous derived-state updates in Effects; ref-based DOM measurement is an allowed case. |
| `react-hooks/set-state-in-render` | Unconditional render updates; not every guarded same-component adjustment. |
| `react-hooks/static-components` | Recognized component types recreated during render. |
| `react-hooks/unsupported-syntax` | Syntax unsupported by compiler analysis. |
| `react-hooks/use-memo` | Incorrect memo calculations, including missing return values. |

The current overview lists `react-hooks/component-hook-factories`, but the 7.1.1 changelog/source identify it as a deprecated no-op after removal in 7.1.0. It is not counted or enabled here. Stable definitions remain a house requirement, partially checked by `static-components` and `react/no-unstable-nested-components`; dynamic Hook factories still need review. The experimental `recommended-latest` profile is not used. Build compiler options/gates remain outside the linter's independent configuration. [REACT-HOOKS-SOURCE]

### JSX accessibility rule IDs

The recommended JSX accessibility profile plus two additions enables these 33 errors. This is static JSX coverage; the rendered result still follows the [HTML guide](related/html.md) and WCAG 2.2 A/AA requirements. It does not establish WCAG conformance. [JSX-A11Y] [WCAG22]

| Rule ID | Check / configured scope |
| --- | --- |
| `jsx-a11y/alt-text` | Text alternatives on supported elements. |
| `jsx-a11y/anchor-has-content` | Content/accessible name for anchors. |
| `jsx-a11y/anchor-is-valid` | Detectable valid link destinations versus action controls. |
| `jsx-a11y/aria-activedescendant-has-tabindex` | Focusability when using `aria-activedescendant`. |
| `jsx-a11y/aria-props` | Known ARIA attribute names. |
| `jsx-a11y/aria-proptypes` | Statically checkable ARIA value types. |
| `jsx-a11y/aria-role` | Valid concrete roles. |
| `jsx-a11y/aria-unsupported-elements` | ARIA on supported elements. |
| `jsx-a11y/autocomplete-valid` | Recognized autocomplete tokens. |
| `jsx-a11y/click-events-have-key-events` | Keyboard handlers on relevant nonnative click targets. |
| `jsx-a11y/control-has-associated-label` | Control text/name; enabled with recommended exclusions for input/textarea and listed composite roles, whose labels still need review. |
| `jsx-a11y/heading-has-content` | Nonempty heading content. |
| `jsx-a11y/html-has-lang` | Language on a rendered document's `html` element. |
| `jsx-a11y/iframe-has-title` | Iframe titles. |
| `jsx-a11y/img-redundant-alt` | Redundant image terminology in alternatives. |
| `jsx-a11y/interactive-supports-focus` | Focusability/tabbability of configured interactive roles. |
| `jsx-a11y/label-has-associated-control` | Labels associated with controls; does not prove every input has a label. |
| `jsx-a11y/media-has-caption` | Caption tracks on supported media; not caption quality or every WCAG media alternative. |
| `jsx-a11y/mouse-events-have-key-events` | Focus equivalents for mouse-over/out handlers. |
| `jsx-a11y/no-access-key` | Avoid accessKey conflicts with browser/assistive shortcuts. |
| `jsx-a11y/no-aria-hidden-on-focusable` | Detectable focusable elements marked aria-hidden; descendant behavior needs rendered tests. |
| `jsx-a11y/no-autofocus` | Automatic focus; a stronger default, not a universal WCAG ban. |
| `jsx-a11y/no-distracting-elements` | Obsolete distracting elements. |
| `jsx-a11y/no-interactive-element-to-noninteractive-role` | Loss of native interactive semantics, subject to preset exceptions. |
| `jsx-a11y/no-noninteractive-element-interactions` | Interaction handlers on noninteractive elements, with preset handler/element exceptions. |
| `jsx-a11y/no-noninteractive-element-to-interactive-role` | Invalid role conversions, retaining the preset's permitted composite mappings. |
| `jsx-a11y/no-noninteractive-tabindex` | Noninteractive tab stops, retaining the tabpanel/dynamic-expression allowances. |
| `jsx-a11y/no-redundant-roles` | Roles duplicating native semantics. |
| `jsx-a11y/no-static-element-interactions` | Event handlers requiring explicit semantics; dynamic-role expressions remain an analysis limit. |
| `jsx-a11y/role-has-required-aria-props` | Required properties for known roles. |
| `jsx-a11y/role-supports-aria-props` | Properties supported by the element's role. |
| `jsx-a11y/scope` | Table-header scope placement. |
| `jsx-a11y/tabindex-no-positive` | Positive tab-order overrides. |

### Checks that still need review

Filename casing, feature dependencies, complete key stability/uniqueness, correct state ownership, direct component calls, Hook injection, cleanup completeness, request races, hydration, useful fallback behavior, sanitization, and memoization benefits are not fully enforced. Rendered accessible names, keyboard behavior, focus, contrast, and all applicable WCAG processes need browser/assistive-technology checks. An Error Boundary does not establish request recovery, and compiler diagnostics do not prove purity. [REACT-RULES] [REACT-EFFECTS] [JSX-A11Y]

Not yet run against TypeScript 6.0.3 or ESLint 9.39.5 with the listed React plugins. Prettier 3.9.10 was validated on a sample; the rule inventory is based on configuration review, not runtime `--print-config` output.

## Naming

- PREFER PascalCase component names and matching `ComponentName.tsx` filenames, with `useThing.ts` for non-JSX Hooks. Why: imports identify components and Hooks consistently. [AIRBNB-REACT] [REACT-RULES]
- MUST prefix custom Hook names with `use` followed by a capitalized word, and reserve that prefix for functions that obey Hook rules. Why: React tooling recognizes Hook boundaries by convention. [REACT-RULES]
- PREFER `onThing` for callback props and `handleThing` for local event handlers, keeping native prop names faithful to their DOM meaning. Why: component call sites reveal event contracts. [React: responding to events](https://react.dev/learn/responding-to-events)
- MUST retain a useful component name through wrappers such as `memo`, using a named implementation and a display name where tooling needs one. Why: component trees and error traces need identifiable owners. [AIRBNB-REACT] [REACT-LINT]

## Files and layout

- MUST write new ordinary React components as named function declarations in `.tsx`; reserve classes for capabilities such as Error Boundaries. Why: Hooks support stateful functions and explicit names aid tooling. [REACT-COMPONENT] [REACT-LINT]
- PREFER a feature folder containing its UI, Hooks, requests, and tests, creating only folders actually needed. Why: feature changes stay together without imposing a demo application's entire layout. [BULLETPROOF]
- PREFER dependency flow from application composition to features to shared code; compose independent features in the application layer. Why: shared UI remains reusable and feature dependencies avoid cycles. [BULLETPROOF]
- PREFER one principal exported component per file while keeping small related private components together, including stateful wrappers. Why: responsibility determines a useful file boundary better than component count. [AIRBNB-REACT] [REACT-EFFECTS]
- MUST define components and Hooks at module scope; pass changing data as props instead of creating component types during render. Why: changing type identity resets state. [REACT-HOOKS] [REACT-LINT]
- PREFER explicit props at ordinary call sites; use typed, filtered spreads for deliberate DOM/library forwarding. Why: wrappers need flexible forwarding without leaking component-only props onto DOM nodes. [AIRBNB-REACT]

The TypeScript baseline's named-export rule applies. Framework-required defaults need a file-pattern override that removes only its `ExportDefaultDeclaration` selector and preserves the other `no-restricted-syntax` selectors; there is no broad React default-export exemption. [GOOGLE-TS] [ESLINT]

## Types and data

- MUST accept a forwarded `ref` as an ordinary typed prop in new function components and pass it to the intended DOM element; do not add `forwardRef`. Why: React 19 supports ref props directly. [React: forwardRef](https://react.dev/reference/react/forwardRef)
- MUST render new context providers as `<Context value={value}>` instead of `<Context.Provider>`. Why: React 19 supports the context object as the provider. [React 19 release](https://react.dev/blog/2024/12/05/react-19)
- MUST declare typed component props, including accepted children, and use parameter defaults when a function prop needs a fallback; do not rely on `propTypes` or function `defaultProps`. Why: React 19 removed those runtime mechanisms for functions. [REACT19] [BULLETPROOF]
- PREFER explicit `children?: ReactNode` for arbitrary renderable children, narrowing to `ReactElement` when the contract requires an element. Why: children types describe the accepted renderable values. [REACT-TS]
- PREFER imported `JSX.Element` or `JSX.Element | null` for exported components returning elements. Why: the house boundary-type rule requires a return contract and React 19 scopes JSX types to React. [TS-ESLINT] [REACT19]
- MUST treat React props, state, Hook arguments/results, and values already passed into JSX as immutable snapshots. Why: React relies on those snapshots for consistent rendering and caching. [REACT-RULES]
- MUST replace each changed level of a state object/array through its setter or reducer; do not mutate received arrays with `sort` or `push`. Why: React needs a new observable snapshot. [REACT-HOOKS]
- PREFER keeping component state with its consumers and lifting shared state to their lowest common owner. Why: one owner avoids synchronization between duplicate stores. [BULLETPROOF] [REACT-EFFECTS]
- PREFER deriving display values from current props/state during render instead of storing synchronized copies in state. Why: duplicate state creates stale passes and Effect chains. [REACT-EFFECTS]
- PREFER `useState` for independent values and `useReducer` for coupled state transitions; keep server-cache and navigable URL state in their respective data/router layers. Why: each kind of state has distinct update and lifetime semantics. [BULLETPROOF]
- MUST use the previous-state updater form when a queued update depends on pending state, including class `setState`. Why: multiple batched updates can otherwise reuse one stale snapshot. [REACT-EFFECT-API] [REACT-LINT]
- MUST keep each input controlled or uncontrolled for its lifetime; controlled text/checked values need synchronous `onChange` updates unless read-only. Why: switching ownership or delaying the update breaks input behavior. [REACT-DOM]
- MUST use stable data-derived keys unique among siblings; never use array indexes, render-generated randomness, or `useId` for list keys. Why: keys preserve each item's state across updates. [REACT-LISTS] [REACT-ID] [REACT-LINT]
- PREFER `useRef` objects for persistent handles and callback refs when attachment/cleanup needs custom work; never use string refs. Why: both current ref forms support different lifecycles. [REACT-HOOKS] [REACT19]
- MUST access `ref.current` outside render except for guarded, predictable one-time initialization; keep display-driving values in state. Why: ref writes do not request a render. [REACT-HOOKS]

## Errors

- MUST use Error Boundaries for descendant rendering failures and handle event/request failures in their own handlers. Why: `try/catch` around JSX does not catch later child renders. [REACT-COMPONENT] [REACT-HOOKS]
- PREFER boundaries around independently recoverable routes or UI regions with a useful fallback and deliberate retry/reset behavior. Why: one failed region need not remove the whole application. [BULLETPROOF]
- MUST let Suspense handle `use` suspension and an Error Boundary handle its rejected resource; never catch `use` locally. Why: React's suspension mechanism must reach its owning boundary. [REACT-HOOKS]
- MUST handle a promise's rejection inside a synchronous event callback when its React prop expects `void`, rather than passing an unhandled async handler. Why: such event callbacks do not consume returned promises; typed linting checks this boundary. [TS-ESLINT] [REACT-COMPONENT]

Error Boundaries do not generally catch ordinary event handlers, timer callbacks, server rendering failures, or errors in the boundary itself. Client Actions have React-managed error propagation; they are not ordinary void event callbacks. Server Functions additionally need the framework's transport/security profile. [REACT-COMPONENT] [React form Actions](https://react.dev/reference/react-dom/components/form)

- PREFER `useActionState` with client form Actions for submissions needing pending and result/error state. Why: React manages the submission transition and state together. [React useActionState](https://react.dev/reference/react/useActionState)
- MUST return expected validation failures as Action state and provide an Error Boundary for unexpected thrown/rejected Action failures. Why: users need actionable errors and React propagates unhandled Action failures to the boundary. [React useActionState](https://react.dev/reference/react/useActionState)
- MUST call `useFormStatus` inside a descendant of the owning form and keep `useOptimistic` updates inside an Action/transition with a confirmed result or rollback path. Why: status follows the parent form and optimistic state must settle with the operation. [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus) [useOptimistic](https://react.dev/reference/react/useOptimistic)

## Comments and docs

- PREFER component examples showing controlled versus uncontrolled usage, permitted children, accessible labeling, and failure/loading states. Why: callers need to see the behavioral prop contract. [BULLETPROOF] [REACT-DOM]
- PREFER documenting the external system and ownership lifetime beside a nontrivial Effect or custom Hook. Why: future edits need to preserve the setup/cleanup relationship. [REACT-EFFECT-API]

## Testing

- PREFER Vitest with React Testing Library and MSW for component/feature tests, and Playwright for browser accessibility and keyboard checks. Why: user-facing assertions and request interception exercise real integration boundaries. [BULLETPROOF]

Use [Bulletproof's testing structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md) for this choice, not its older React/ESLint package versions. Pin compatible Testing Library/MSW/environment packages in the consuming lockfile; Vitest 5.0.5 and Playwright 1.64.1 are the selected starting versions.

- MUST exercise Effect setup, cleanup, and remounting under Strict Mode when testing synchronization. Why: repeated development lifecycles reveal leaked subscriptions and nonrepeatable work. [REACT-EFFECT-API]
- PREFER DOM-level feature tests through user interactions and accessible roles/names, with network interception rather than replacing Hooks dynamically. Why: React-controlled behavior and request integration stay in the test. [BULLETPROOF] [REACT-RULES]
- MUST cover reordered/removed list items, controlled-input changes, and stale asynchronous responses when those behaviors change. Why: identity and scheduling bugs often survive a static rendering test. [AIRBNB-REACT] [REACT-DOM] [REACT-EFFECTS]
- MUST check boundary fallback/retry behavior and keyboard/focus behavior for changed interactive components. Why: successful initial rendering misses recovery and accessibility failures. [REACT-COMPONENT] [JSX-A11Y]

## Performance

- MUST make component correctness independent of `useMemo`, `useCallback`, and `memo`; memo calculations must be pure and return their computed value. Why: memoization is an optimization, not a lifecycle or state guarantee. [REACT-MEMO] [REACT-HOOKS]
- PREFER direct render calculations before manual caches, and use lazy state initialization for expensive initial state. Why: caches add dependencies and initializers need not rerun on every update. [REACT-EFFECTS] [BULLETPROOF]
- MUST use stable immutable module-level values for object/array/function prop defaults instead of fresh parameter-default literals. Why: new default identities can retrigger synchronization and defeat memoization. [REACT-LINT]
- PREFER the framework's data loader or an existing query/cache layer over ad hoc request Effects. Why: caching, server loading, and parallel requests need coordinated ownership. [REACT-EFFECTS] [BULLETPROOF]
- PREFER route-level code splitting and state/context boundaries based on which UI actually consumes updates. Why: unrelated routes and consumers need not load or rerender together. [BULLETPROOF]
- MUST check memoization compatibility before introducing observed mutable library APIs into compiler-optimized or manually memoized UI. Why: an unchanged reference can hide changed data from React. [REACT-HOOKS]

For named route exports, adapt the import at module scope without changing the module's public exports:

```tsx
const Settings = lazy(() =>
  import('./Settings').then((module) => ({ default: module.Settings })),
);
```

Import `lazy` from React, render this under Suspense and an Error Boundary, and keep the declaration outside rendering. This satisfies [React.lazy's default-member contract](https://react.dev/reference/react/lazy) and the named-export rule.

## Security

- MUST keep `dangerouslySetInnerHTML` out of ordinary components; isolate any necessary sanitized rich HTML in a reviewed adapter. Why: that API bypasses React's text escaping. [REACT-DOM] [REACT-LINT]
- MUST validate allowed destinations before putting untrusted URLs in `href`, `src`, or navigation APIs; never use `javascript:` links. Why: escaping JSX text does not validate URL schemes or navigation targets. [REACT-LINT] [OWASP]
- MUST make external or dynamic JSX links with `target="_blank"` use `rel="noreferrer"` under this preset, and audit equivalent custom wrappers. Why: this explicit house policy prevents opener access and referrer disclosure without relying on implicit browser behavior. [REACT-LINT]

The HTML adapter's file-scoped `react/no-danger` exception does not relax `no-danger-with-children` or supply a sanitizer. The guide chooses no sanitizer package. Client route guards remain UI behavior under shared authorization policy. [REACT-DOM] [BULLETPROOF]

## Language-specific pitfalls

### Rendering and Hooks

- MUST render components through JSX instead of calling component functions directly. Why: React owns their identity, state, and scheduling. [REACT-RULES]
- MUST call ordinary Hooks unconditionally at the top level of function components or custom Hooks, before early returns. Why: React associates state with stable call order. [REACT-RULES]
- MUST keep `use` inside a component or Hook and outside `try/catch`; any promise passed to it must come from a cache, loader, or parent with stable identity across rerenders, never be created during render. Why: new promises repeatedly suspend; `use` permits conditions and loops. [REACT-HOOKS]
- MUST call Hooks statically instead of injecting a Hook through props or constructing higher-order Hooks at runtime. Why: React needs a locally visible, stable Hook structure. [REACT-RULES]
- MUST keep repeated render calculations idempotent and free of observable side effects, including time/random generation and global writes. Why: React may restart or discard rendering. [REACT-RULES]
- MUST confine render-local mutation to freshly created values before passing them to Hooks or JSX. Why: local calculations may build data without changing another render's snapshot. [REACT-RULES]
- PREFER resetting a conceptual subtree with a changed data-identity key before synchronizing its old state in an Effect. Why: React can discard the old subtree's state in one transition. [REACT-EFFECTS]
- MUST keep any unavoidable render-time state adjustment in the same component behind a terminating previous-render comparison; never update another component during render. Why: the documented narrow exception avoids stale commits without an infinite render loop. [REACT-EFFECTS] [REACT-HOOKS]

### Effects

- MUST put interaction-triggered submissions and parent notifications in the relevant event handler or form Action. Why: an Effect cannot reliably identify which interaction caused a render. [REACT-EFFECTS]
- MUST use Effects for external synchronization and return cleanup that reverses subscriptions, timers, or other acquired resources. Why: dependencies, unmounts, and Strict Mode can repeat setup. [REACT-EFFECT-API]
- MUST include every reactive value used by an Effect, memo, or callback in its dependency list; restructure logic rather than omitting dependencies. Why: missing dependencies capture stale values. [REACT-HOOKS]
- MUST prevent outdated asynchronous Effect results from committing after cleanup or a newer request. Why: responses can arrive out of order. [REACT-EFFECTS]
- MUST keep an Effect's setup callback synchronous and run asynchronous work inside it with explicit completion/error handling and cleanup. Why: React expects an optional cleanup function, not a promise. [REACT-EFFECT-API]
- PREFER `useSyncExternalStore` for an external store subscription instead of a handwritten Effect/state mirror. Why: React provides a dedicated subscription and snapshot contract. [REACT-EFFECTS]
- PREFER purpose-specific custom Hooks over wrappers exposing generic callback/dependency-array scheduling. Why: domain APIs keep synchronization details inside one implementation. [REACT-HOOKS-SOURCE] [REACT-EFFECTS]
- MUST limit synchronous Effect-driven state changes to actual synchronization needs such as ref-derived DOM measurement, rather than copying props or calculating display data. Why: derivable state causes an unnecessary second render. [REACT-HOOKS] [REACT-EFFECTS]

### JSX, DOM, and remaining classes

- MUST preserve native semantics and accessible names through JSX wrappers, including forwarding label, ARIA, and focus-related props to the intended DOM element. Why: a component name alone conveys no browser semantics. [JSX-A11Y] [REACT-DOM]
- MUST specify native button types and connect visible labels with nesting or `htmlFor`; use `useId` for reusable DOM relationships when no stable caller-provided ID exists. Why: accidental form submissions and duplicate DOM IDs break reusable controls. [REACT-LINT] [REACT-ID] [REACT-DOM]
- MUST use `className`, `htmlFor`, and object-valued `style` in JSX while retaining hyphens in `aria-*` and `data-*`. Why: React's DOM prop names and value contracts differ from HTML syntax. [REACT-DOM]
- MUST use explicit Boolean conditions for conditional JSX, such as `items.length > 0`, rather than relying on a numeric `&&` operand. Why: React renders `0` as text. [REACT-LINT] [TS-ESLINT]
- MUST put list keys on the outer returned element or explicit `Fragment` and pass any needed identifier separately as a prop. Why: keys belong to React's sibling reconciliation rather than the child prop contract. [REACT-LISTS] [REACT-LINT]
- MUST keep new code free of removed legacy context, string refs, `findDOMNode`, `isMounted`, and unsafe will-lifecycles. Why: historical ordering lists do not make obsolete APIs valid. [REACT19] [REACT-COMPONENT]
- PREFER class-field arrow handlers in necessary classes when lexical `this` is needed; define lifecycle methods as prototype methods. Why: constructor binding is not required by modern React or class-field syntax. [REACT-COMPONENT]

## Where the sources disagree

- MUST use function components for new ordinary stateful UI when Airbnb prefers classes for state/refs and current React recommends functions with Hooks; retain needed Error Boundary classes. Why: this matches the current state model without losing class-only capabilities. [AIRBNB-REACT] [REACT-COMPONENT]
- MUST use parameter defaults only where a function prop needs a fallback when Airbnb requires `defaultProps` for optional props and React 19 removes function `defaultProps`; class defaults remain supported. Why: the current runtime determines valid behavior. [AIRBNB-REACT] [REACT19]
- MUST use typed prop contracts rather than React `propTypes` when Airbnb prescribes runtime prop shapes and Bulletproof favors TypeScript. Why: React 19 ignores `propTypes`; external data validation remains governed by shared policy. [AIRBNB-REACT] [BULLETPROOF] [REACT19]
- PREFER `useRef` objects for ordinary persistent handles and callback refs for attachment-specific behavior when Airbnb mandates callback-only refs and current React supports both. Why: each supported form has a useful lifecycle contract. [AIRBNB-REACT] [REACT-HOOKS]
- MUST use `.tsx` for typed JSX when Airbnb specifies `.jsx` and Bulletproof demonstrates TypeScript components. Why: this profile extends the strict TypeScript configuration. [AIRBNB-REACT] [BULLETPROOF]
- PREFER PascalCase component filenames when Airbnb specifies PascalCase and Bulletproof demonstrates optional kebab-case. Why: matching component and filename names makes the house default predictable; established filenames still follow shared migration scope. [AIRBNB-REACT] [BULLETPROOF]
- PREFER one principal exported component with related private components colocated when Airbnb's one-component rule would split React's stateful wrapper example. Why: cohesive implementation details need not become separate modules. [AIRBNB-REACT] [REACT-EFFECTS]
- PREFER class-field arrow handlers in necessary classes when Airbnb forbids them and current React uses them. Why: lexical binding is supported and avoids ceremonial constructor binding. [AIRBNB-REACT] [REACT-COMPONENT]
- MUST omit legacy context and unsafe lifecycles when Airbnb's ordering lists contain them and current React removes or discourages them. Why: source-era ordering is not a current API requirement. [AIRBNB-REACT] [REACT19] [REACT-COMPONENT]
- MUST assess MobX observer/memoization compatibility and isolate a documented compiler opt-out where needed when Bulletproof lists MobX and React warns about hidden mutable observations. Why: library availability does not prove memoization correctness, and the linter may miss this pattern. [BULLETPROOF] [REACT-HOOKS]
- MUST use React Hook Form's `useWatch` alternative for rendered field observation instead of the flagged `watch` pattern when Bulletproof recommends the library and React identifies that API's incompatibility. Why: the restriction concerns observable dataflow rather than banning the library. [BULLETPROOF] [REACT-HOOKS]
- MUST treat `component-hook-factories` as inactive in plugin 7.1.1 when the reference overview lists it but the release changelog/source declare a no-op. Why: documented intentions cannot supply an absent check; stable definitions retain other checks and review. [REACT-HOOKS] [REACT-HOOKS-SOURCE]
