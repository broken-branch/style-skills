# React style: Airbnb React/JSX (condensed)

Use this skill only when the user explicitly requests this source. It replaces the house `react-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing React code. Each rule names and links to its original section; cite the source title and section in review findings.

The source file last changed in 2021. Rules marked dated preserve historical class/state/ref advice, prop validation, function defaults, and legacy ordering. Prefer `react-official-style` wherever the guides clash; the rules file links current official guidance so this package also works on its own.

React 19 ignores `propTypes` and function `defaultProps`; use typing and parameter defaults where appropriate. Class `defaultProps` remains supported. Do not introduce removed context APIs, string refs, or unsafe lifecycles merely to follow the historical ordering lists.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State that conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original, state the limitation and use the project's existing convention for that point.

Source snapshot: Airbnb React/JSX Style Guide: React README last changed 2021-02-17, 7a6ef3e7.

License: [MIT](LICENSE). Changes: rules restated and shortened; examples omitted; dated guidance qualified.

Credit: Airbnb React/JSX Style Guide, Airbnb, MIT, https://github.com/airbnb/javascript/tree/master/react. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Airbnb.
