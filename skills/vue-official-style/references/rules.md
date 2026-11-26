# Vue project style (condensed)

Vue Style Guide rules, grouped by topic. Each rule keeps its source priority and section link; optional explanations are labeled separately.

Each rule keeps its original priority and section link. A means Essential, B means Strongly Recommended, C means Recommended, and D means Use with Caution. The quick rules explain these priorities without duplicating the topic rules. Examples are omitted.

## Quick rules

- Treat this guide as a starting point for Vue conventions, adjusting deliberately for the project; it does not prescribe a complete JavaScript style. — [Style Guide (Introduction)](https://vuejs.org/style-guide/).
- **A:** Apply the error-prevention requirements; only someone with deep Vue and JavaScript expertise should make an exceptional departure. — [Priority A Rules: Essential](https://vuejs.org/style-guide/rules-essential.html#priority-a-rules-essential).
- **B:** Normally adopt the readability recommendations, departing only occasionally and with a sound justification. — [Priority B Rules: Strongly Recommended](https://vuejs.org/style-guide/rules-strongly-recommended.html#priority-b-rules-strongly-recommended).
- **C:** Keep equivalent style choices uniform, using the community default unless there is a reason to choose another accepted form. — [Priority C Rules: Recommended](https://vuejs.org/style-guide/rules-recommended.html#priority-c-rules-recommended).
- **D:** Approach the identified risky features as exceptional tools, understanding their maintenance costs and why the particular case needs them. — [Priority D Rules: Use with Caution](https://vuejs.org/style-guide/rules-use-with-caution.html#priority-d-rules-use-with-caution).

## Naming

- **A:** Name components with at least two words; the application's root `App` is exempt. — [Use multi-word component names](https://vuejs.org/style-guide/rules-essential.html#use-multi-word-component-names).
- **A (optional explanation):** App- or component-specific class-name prefixes can provide extra isolation from third-party styles; scoping is the essential rule. — [Use component-scoped styling](https://vuejs.org/style-guide/rules-essential.html#use-component-scoped-styling).
- **B:** Pick PascalCase or kebab-case for SFC filenames and keep that choice uniform; weigh editor completion against case-insensitive filesystem compatibility. — [Single-file component filename casing](https://vuejs.org/style-guide/rules-strongly-recommended.html#single-file-component-filename-casing).
- **B:** Start the names of app-styled base components with the same recognizable prefix. — [Base component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#base-component-names).
- **B:** Usually name a base component after the HTML element it wraps, unless that element does not describe the component's purpose. — [Base component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#base-component-names).
- **B:** For a child usable only with one parent, begin its name with that parent's component name. — [Tightly coupled component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#tightly-coupled-component-names).
- **B:** Lead component names with the broadest concept in the app's context, then add the narrower descriptors. — [Order of words in component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#order-of-words-in-component-names).
- **B:** Favor PascalCase when referencing components from SFC markup or string templates. — [Component name casing in templates](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-name-casing-in-templates).
- **B:** Write component tags in kebab-case when the browser parses the template before Vue. — [Component name casing in templates](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-name-casing-in-templates).
- **B:** A uniform kebab-case convention is also valid when established usage or consistency across template formats outweighs PascalCase's benefits. — [Component name casing in templates](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-name-casing-in-templates).
- **B:** Spell JavaScript component identifiers and JSX component names in PascalCase. — [Component name casing in JS/JSX](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-name-casing-in-js-jsx).
- **B:** For simple apps that register every component globally through `app.component`, kebab-case registration strings are the recommended alternative. — [Component name casing in JS/JSX](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-name-casing-in-js-jsx).
- **B:** Spell out words in component names, especially where an abbreviation would be unfamiliar. — [Full-word component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#full-word-component-names).
- **B:** Use camelCase when declaring a prop's name. — [Prop name casing](https://vuejs.org/style-guide/rules-strongly-recommended.html#prop-name-casing).
- **B:** Spell prop attributes in kebab-case in browser-parsed DOM templates. — [Prop name casing](https://vuejs.org/style-guide/rules-strongly-recommended.html#prop-name-casing).
- **B:** In SFC markup and JSX, either prop-attribute casing is valid; consistently choose camelCase or kebab-case. — [Prop name casing](https://vuejs.org/style-guide/rules-strongly-recommended.html#prop-name-casing).

## Files and layout

- **B:** Keep each component in its own file when the build can combine the files. — [Component files](https://vuejs.org/style-guide/rules-strongly-recommended.html#component-files).
- **B:** Compose base components only from HTML elements, other base components, or UI components supplied by third parties. — [Base component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#base-component-names).
- **B:** Global registration is an option for heavily reused, consistently prefixed base components; this does not mandate Vite or a particular registration implementation. — [Base component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#base-component-names).
- **B:** Express tight parent-child relationships through name prefixes rather than deep directory trees containing indistinguishable child filenames. — [Tightly coupled component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#tightly-coupled-component-names).
- **B:** Reserve consideration of nested feature folders for very large applications, rather than using them routinely to organize components. — [Order of words in component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#order-of-words-in-component-names).
- **B:** Use self-closing syntax for components with no children in JSX, SFCs, and string templates. — [Self-closing components](https://vuejs.org/style-guide/rules-strongly-recommended.html#self-closing-components).
- **B:** When an element has several attributes, expand the markup so each attribute occupies its own line. — [Multi-attribute elements](https://vuejs.org/style-guide/rules-strongly-recommended.html#multi-attribute-elements).
- **B:** Surround nonempty HTML attribute values with quotes, even when HTML permits omitting them. — [Quoted attribute values](https://vuejs.org/style-guide/rules-strongly-recommended.html#quoted-attribute-values).
- **B:** Use the other quote style for attributes from the one chosen for JavaScript strings. — [Quoted attribute values](https://vuejs.org/style-guide/rules-strongly-recommended.html#quoted-attribute-values).
- **B:** Adopt directive abbreviations uniformly (`:` for binding, `@` for listeners, `#` for slots), or uniformly spell out the directives. — [Directive shorthands](https://vuejs.org/style-guide/rules-strongly-recommended.html#directive-shorthands).
- **C:** Apply one stable ordering convention to component and instance option declarations. — [Component/instance options order](https://vuejs.org/style-guide/rules-recommended.html#component-instance-options-order).
- **C:** Prefer this option sequence: identity (`name`); compilation (`compilerOptions`); template dependencies (`components`, `directives`); option composition (`extends`, `mixins`, `provide`/`inject`); public interface (`inheritAttrs`, `props`, `emits`, `expose`); Composition API entry (`setup`); reactive state (`data`, `computed`); reactive callbacks (`watch`, lifecycle hooks); nonreactive behavior (`methods`); output (`template`/`render`). — [Component/instance options order](https://vuejs.org/style-guide/rules-recommended.html#component-instance-options-order).
- **C:** Within lifecycle declarations, follow the guide's suggested sequence: creation (`beforeCreate`, `created`), mounting (`beforeMount`, `mounted`), updating (`beforeUpdate`, `updated`), activation (`activated`, `deactivated`), unmounting (`beforeUnmount`, `unmounted`), error handling (`errorCaptured`), render diagnostics (`renderTracked`, `renderTriggered`), then server-only prefetch (`serverPrefetch`). — [Component/instance options order](https://vuejs.org/style-guide/rules-recommended.html#component-instance-options-order).
- **C:** Maintain a uniform attribute order on both native elements and components. — [Element attribute order](https://vuejs.org/style-guide/rules-recommended.html#element-attribute-order).
- **C:** Prefer this attribute sequence: component definition (`is`); iteration (`v-for`); visibility conditions (`v-if`, `v-else-if`, `v-else`, `v-show`, `v-cloak`); rendering controls (`v-pre`, `v-once`); document identity (`id`); unique references (`ref`, `key`); two-way data (`v-model`); remaining bound and unbound attributes; event handlers (`v-on`); replacement content (`v-html`, `v-text`). — [Element attribute order](https://vuejs.org/style-guide/rules-recommended.html#element-attribute-order).
- **C:** A blank line between multiline option entries can improve scanning, especially once the component extends beyond a screen. — [Empty lines in component/instance options](https://vuejs.org/style-guide/rules-recommended.html#empty-lines-in-component-instance-options).
- **C:** Keep SFC block order uniform and place `<style>` last; either `<script>` or `<template>` can lead. — [Single-file component top-level element order](https://vuejs.org/style-guide/rules-recommended.html#single-file-component-top-level-element-order).

## Types and data

- **A:** Before committing a component, describe its props thoroughly and specify at least which types each accepts. — [Use detailed prop definitions](https://vuejs.org/style-guide/rules-essential.html#use-detailed-prop-definitions).
- **B:** Base components must not hold or depend on application-wide state. — [Base component names](https://vuejs.org/style-guide/rules-strongly-recommended.html#base-component-names).
- **B:** Leave only straightforward expressions in templates; extract complex calculations into methods or computed values. — [Simple expressions in templates](https://vuejs.org/style-guide/rules-strongly-recommended.html#simple-expressions-in-templates).
- **B:** Decompose complicated computed values into small, clearly named computed properties wherever feasible. — [Simple computed properties](https://vuejs.org/style-guide/rules-strongly-recommended.html#simple-computed-properties).

## Performance

- **A:** An unkeyed ordinary-element loop is an exceptional performance choice, acceptable only when retaining element identity is unnecessary; component loops still need keys. — [Use keyed v-for](https://vuejs.org/style-guide/rules-essential.html#use-keyed-v-for).
- **D:** In `scoped` CSS, favor selectors based on classes over selectors based on element names. — [Element selectors with scoped](https://vuejs.org/style-guide/rules-use-with-caution.html#element-selectors-with-scoped).

## Language-specific pitfalls

- **A:** Every component rendered by `v-for` needs a key that keeps its internal state attached to the corresponding item. — [Use keyed v-for](https://vuejs.org/style-guide/rules-essential.html#use-keyed-v-for).
- **A:** Ordinarily give native elements rendered in loops unique, stable keys too, so updates preserve each item's element identity. — [Use keyed v-for](https://vuejs.org/style-guide/rules-essential.html#use-keyed-v-for).
- **A:** Keep `v-if` off any element that also carries `v-for`. — [Avoid v-if with v-for](https://vuejs.org/style-guide/rules-essential.html#avoid-v-if-with-v-for).
- **A:** Perform list filtering in a computed value and iterate over that result, instead of pairing the loop with an item filter directive. — [Avoid v-if with v-for](https://vuejs.org/style-guide/rules-essential.html#avoid-v-if-with-v-for).
- **A:** Control whether an entire list appears by placing its condition on the surrounding container. — [Avoid v-if with v-for](https://vuejs.org/style-guide/rules-essential.html#avoid-v-if-with-v-for).
- **A:** When a condition needs the iteration variable, an outer `<template>` carrying `v-for` may wrap the separately conditional child. — [Avoid v-if with v-for](https://vuejs.org/style-guide/rules-essential.html#avoid-v-if-with-v-for).
- **A:** For SFC applications, contain styling within each component; root `App` and layout components may supply global styles. — [Use component-scoped styling](https://vuejs.org/style-guide/rules-essential.html#use-component-scoped-styling).
- **A:** SFC style isolation may use `scoped`, CSS Modules, BEM, or another suitable convention or library; the `scoped` attribute itself is optional. — [Use component-scoped styling](https://vuejs.org/style-guide/rules-essential.html#use-component-scoped-styling).
- **A:** For component libraries, favor class-based style isolation so consumers can override internals through readable selectors with manageable specificity. — [Use component-scoped styling](https://vuejs.org/style-guide/rules-essential.html#use-component-scoped-styling).
- **B:** Supply an explicit closing tag for custom components in templates the browser parses as DOM before Vue compiles them. — [Self-closing components](https://vuejs.org/style-guide/rules-strongly-recommended.html#self-closing-components).
- **D:** Prefer parent-to-child props and child-to-parent events for communication, rather than modifying received props or accessing `$parent`. — [Implicit parent-child communication](https://vuejs.org/style-guide/rules-use-with-caution.html#implicit-parent-child-communication).
- **D:** Consider prop mutation or parent access only for exceptional, already interdependent components, weighing understandable state flow against maintenance cost rather than merely reducing code. — [Implicit parent-child communication](https://vuejs.org/style-guide/rules-use-with-caution.html#implicit-parent-child-communication).

## Where the sources disagree

No unresolved source conflicts in this guide's scope. This is a single-source adaptation; its accepted alternatives and exceptional cases remain conditional rather than becoming house-policy choices. The styling rule retains the original's explicit SFC scope, as stated in the original. Lifecycle ordering describes declaration layout, not a promise about runtime hook execution.

Credit: Vue Style Guide, Yuxi (Evan) You and Vue documentation contributors, CC-BY-4.0, https://vuejs.org/style-guide/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Yuxi (Evan) You and Vue documentation contributors.
