---
name: react-style
description: "Write, edit, or review React code (.tsx, .jsx, and Hook .ts files) using house style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: react
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# React style (house)

Our blend of the best React guides, in our own words. Every rule in the full guide names its source.

Scope: React/React DOM 19.3 browser applications and reusable components, using TypeScript 6.0.3 and the automatic JSX runtime. React Compiler adoption is optional; compiler-aware linting is included. Client form Actions are included. React Native, framework routing, Server Components, and Server Functions need additional project profiles. Build/test tools use Node 24 LTS or a newer supported release.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

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

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [button states](references/examples/ButtonStates.tsx), [field and switch](references/examples/PreferenceForm.tsx), [modal focus](references/examples/ViewDialog.tsx), [shared styles](references/examples/controls.css).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
