# PowerShell style: Microsoft cmdlet development guidelines (condensed)

Use this skill only when the user explicitly requests Microsoft's strongly encouraged cmdlet development guidelines. It replaces the house `powershell-style` skill for this task.

Read the relevant sections of [references/rules.md](references/rules.md) before writing or reviewing cmdlets. Each rule names and links its original section; cite that section when explaining a review finding.

Scope: every guideline from the strongly encouraged design and code guidelines, source commit `46dd905eed71bbc671f1219d7dc11831026e6372` (2026-04-08), page date 2021-10-05, checked in the PowerShell 7.6 view on 2026-10-31. Linked required and advisory guideline collections are separate sources and are not included.

These are recommendations where applicable. Binary-cmdlet API members and assembly Help.xml files apply to compiled cmdlets; do not impose them as script syntax. Preserve the source's broad recommendations while distinguishing them from runtime requirements. The reference flags contradictory host wording, the command-casing typo, the dated Debug claim, and the clarification that compiled parameter properties are non-static.

When a rule conflicts with a formatter or linter already used by the project, the project's tooling wins; explain the conflict in one line. Preserve the source's optional choices and exceptions.

The bundled rules work offline. If an ambiguity needs an unavailable original section, state the limitation and use the project's existing convention for that point.

License: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/), with the upstream license in [LICENSE](LICENSE). Changes: rules independently restated, shortened, and grouped by topic; examples omitted; applicability and source ambiguities retained.

Credit: Strongly Encouraged Development Guidelines for PowerShell cmdlets, Microsoft Corporation, CC-BY-4.0, https://learn.microsoft.com/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Microsoft Corporation.
