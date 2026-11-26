---
name: vue-style
description: "Write, edit, or review .vue and Vue .ts files using house Vue style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: vue
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# Vue style (house)

Our blend of the best Vue guides, in our own words. Every rule in the full guide names its source.

Scope: owned Vue 3.5+ applications and component libraries using compiled Single-File Components (SFCs), Composition API, and TypeScript 6.0.3. Build/test tools use Node 24 LTS or a newer supported release. Vue 2, in-DOM templates, and existing Options API migrations need separate profiles; this guide does not authorize a migration.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

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

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [button states](references/examples/ButtonStates.vue), [field and switch](references/examples/PreferenceForm.vue), [modal focus](references/examples/ViewDialog.vue).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
