# Rules of React: condensed rules

Ordinary Hook placement rules do not prohibit conditional or looped calls to `use`. Call `use` only inside a component or Hook, and do not wrap a promise-reading `use` call in `try`/`catch`.

Source owner: Meta Platforms, Inc. and React documentation contributors. License: [CC-BY-4.0](../LICENSE). Changes: rules independently restated, shortened and grouped by topic; examples omitted. Unofficial; no endorsement is implied.

Copyright © Meta Platforms, Inc.

## Quick rules

- Keep rendering pure; run side effects in handlers or Effects.
- Call ordinary Hooks at the top level of components or custom Hooks; `use` has its own conditional-call rules.
- Treat props, state, and Hook arguments and results as immutable snapshots.

## Tooling

- Enable Strict Mode and the React ESLint checks to reveal rule violations. — [Rules of React: Rules of React](https://react.dev/reference/rules). <!-- rules-of-react:1 -->

## Types and data

- Regard received props and current state as read-only render snapshots. — [Rules of React: Props and state are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#props-and-state-are-immutable). <!-- rules-of-react:13 -->
- Supply replacement props instead of editing the values a component received. — [Rules of React: Props and state are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#props-and-state-are-immutable). <!-- rules-of-react:14 -->
- Use the state setter to request a new snapshot; do not mutate the current one. — [Rules of React: Props and state are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#props-and-state-are-immutable). <!-- rules-of-react:15 -->
- After supplying an argument to a Hook, leave that argument unchanged. — [Rules of React: Return values and arguments to Hooks are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#return-values-and-arguments-to-hooks-are-immutable). <!-- rules-of-react:16 -->
- Leave values obtained from a Hook unmodified. — [Rules of React: Return values and arguments to Hooks are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#return-values-and-arguments-to-hooks-are-immutable). <!-- rules-of-react:17 -->
- Rely on a Hook's public behavior without depending on hidden implementation details. — [Rules of React: Return values and arguments to Hooks are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#return-values-and-arguments-to-hooks-are-immutable). <!-- rules-of-react:18 -->
- Once a value is used in JSX, do not subsequently modify it. — [Rules of React: Values are immutable after being passed to JSX](https://react.dev/reference/rules/components-and-hooks-must-be-pure#values-are-immutable-after-being-passed-to-jsx). <!-- rules-of-react:19 -->
- Finish any permitted local mutation before creating JSX that uses the value. — [Rules of React: Values are immutable after being passed to JSX](https://react.dev/reference/rules/components-and-hooks-must-be-pure#values-are-immutable-after-being-passed-to-jsx). <!-- rules-of-react:20 -->

## Testing

- Prefer server mocks and, where practical, end-to-end coverage over injecting replacement Hooks for tests. — [Rules of React: Don’t dynamically use Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks#dont-dynamically-use-hooks). <!-- rules-of-react:26 -->

## Purity

- For identical props, state, context, and Hook inputs, produce an equivalent rendering result. — [Rules of React: Components and Hooks must be idempotent](https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent). <!-- rules-of-react:2 -->
- Ensure each calculation executed while rendering is repeatable for the same inputs. — [Rules of React: Components and Hooks must be idempotent](https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent). <!-- rules-of-react:3 -->
- Read clocks, generate randomness, and perform other nondeterministic work outside repeated render calculations. — [Rules of React: Components and Hooks must be idempotent](https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent). <!-- rules-of-react:4 -->
- Run externally observable actions outside component rendering. — [Rules of React: Side effects must run outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#side-effects-must-run-outside-of-render). <!-- rules-of-react:5 -->
- Handle interaction work in event handlers; use Effects when synchronization cannot be handled that way. — [Rules of React: Side effects must run outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#side-effects-must-run-outside-of-render). <!-- rules-of-react:6 -->
- During rendering, leave values originating outside that render unchanged. — [Rules of React: Side effects must run outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#side-effects-must-run-outside-of-render). <!-- rules-of-react:7 -->
- Mutation is acceptable for temporary values freshly created within the current calculation. — [Rules of React: Local mutation](https://react.dev/reference/rules/components-and-hooks-must-be-pure#local-mutation). <!-- rules-of-react:8 -->
- Recreate render output locally instead of accumulating entries in an array shared across renders. — [Rules of React: Local mutation](https://react.dev/reference/rules/components-and-hooks-must-be-pure#local-mutation). <!-- rules-of-react:9 -->
- Lazy initialization is permissible when repeated calls remain safe and cannot disturb other components' rendering. — [Rules of React: Lazy initialization](https://react.dev/reference/rules/components-and-hooks-must-be-pure#lazy-initialization). <!-- rules-of-react:10 -->
- Evaluating a component must not itself make visible DOM changes. — [Rules of React: Changing the DOM](https://react.dev/reference/rules/components-and-hooks-must-be-pure#changing-the-dom). <!-- rules-of-react:11 -->
- Synchronize external browser state after rendering rather than modifying it while calculating JSX. — [Rules of React: Changing the DOM](https://react.dev/reference/rules/components-and-hooks-must-be-pure#changing-the-dom). <!-- rules-of-react:12 -->

## React calls Components and Hooks

- Describe component instances in JSX so React controls invocation; do not invoke component functions yourself. — [Rules of React: Never call component functions directly](https://react.dev/reference/rules/react-calls-components-and-hooks#never-call-component-functions-directly). <!-- rules-of-react:21 -->
- Call Hooks within component or Hook logic instead of passing them around as interchangeable function values. — [Rules of React: Never pass around Hooks as regular values](https://react.dev/reference/rules/react-calls-components-and-hooks#never-pass-around-hooks-as-regular-values). <!-- rules-of-react:22 -->
- Declare a fixed Hook implementation rather than manufacturing or modifying Hooks dynamically. — [Rules of React: Don’t dynamically mutate a Hook](https://react.dev/reference/rules/react-calls-components-and-hooks#dont-dynamically-mutate-a-hook). <!-- rules-of-react:23 -->
- Do not provide a Hook through props or another runtime dependency-injection mechanism. — [Rules of React: Don’t dynamically use Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks#dont-dynamically-use-hooks). <!-- rules-of-react:24 -->
- Put the Hook invocation directly in its component or in a statically defined custom Hook. — [Rules of React: Don’t dynamically use Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks#dont-dynamically-use-hooks). <!-- rules-of-react:25 -->

## Rules of Hooks

- Place ordinary Hook calls at the top level, ahead of any return that depends on a condition. — [Rules of React: Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level). <!-- rules-of-react:27 -->
- Keep ordinary Hook calls out of branches, iteration bodies, and nested function bodies. — [Rules of React: Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level). <!-- rules-of-react:28 -->
- Keep Hook calls outside `try`, `catch`, and `finally` blocks. — [Rules of React: Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level). <!-- rules-of-react:29 -->
- Neither event handlers nor class components may call Hooks. — [Rules of React: Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level). <!-- rules-of-react:30 -->
- Do not invoke Hooks from functions supplied to `useMemo`, `useReducer`, or `useEffect`. — [Rules of React: Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level). <!-- rules-of-react:31 -->
- Invoke Hooks only as React renders a function component or evaluates a custom Hook, never from a regular JavaScript function. — [Rules of React: Only call Hooks from React functions](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-from-react-functions). <!-- rules-of-react:32 -->

Scope clarification: ordinary Hook placement rules do not prohibit conditional or looped calls to the separate [`use` API](https://react.dev/reference/react/use). Call `use` only inside a component or Hook, and do not wrap a promise-reading `use` call in `try`/`catch`.
