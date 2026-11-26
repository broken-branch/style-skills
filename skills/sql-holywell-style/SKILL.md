---
name: sql-holywell-style
description: "Write or review SQL using Simon Holywell's guide only when explicitly requested; replaces house SQL style for this task."
license: CC-BY-SA-4.0
disable-model-invocation: true
metadata:
  kind: source
  language: sql
  version: "1.0.0"
  source-url: "https://www.sqlstyle.guide/"
  treatment: share-alike
---

# SQL style: Simon Holywell (condensed)

Use this skill only when the user explicitly requests Simon Holywell's SQL style. It replaces the house `sql-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing SQL, reading the relevant topic sections before changing code. Each rule names and links its original section; cite that section when explaining a review finding.

Scope: the SQL Style Guide at commit `d1c856a7d5303773adf66468f51529a7ded786a1` (2024-02-27), checked against the published guide on 2026-10-31. Every rule in the guide is covered. Examples and the keyword glossary are omitted.

The keyword appendix lists older engine versions and is not a current compatibility reference. Check the target dialect's documentation for supported syntax, types, and reserved names; preserve the guide's preferences where supported.

Keep the source's exceptions and recommendation strength. When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins; explain the conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original section, state the limitation and use the project's existing convention for that point.

License: this adaptation is [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/); the original notice is in [LICENSE](LICENSE). Changes: independently restated and shortened rules, grouped by topic; examples omitted.

Credit: SQL style guide by Simon Holywell is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License. Based on a work at https://www.sqlstyle.guide/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Simon Holywell.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [aligned joins and ranges](references/examples/low_stock.sql), [aligned aggregation](references/examples/stock_totals.sql), [aligned subqueries](references/examples/empty_depots.sql).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
