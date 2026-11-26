# PowerShell style: PowerShell Practice and Style (condensed)

Use this skill only when the user explicitly requests PoshCode's PowerShell Practice and Style. It replaces the house `powershell-style` skill for this task.

Read the relevant sections of [references/rules.md](references/rules.md) before writing or reviewing PowerShell. Each rule names and links its original section; cite that section when explaining a review finding.

Scope: the PREVIEW guide at source commit `d1c6ae146b1060ec4844afc393161c6237bd85a7` (2023-05-19), checked on 2026-10-31. Every rule in the guide is covered, including its expressly unpublished TODO proposals. Entries labeled **unpublished TODO proposal** are retained for completeness, not adopted policy; apply them only when the user chooses that proposal. Output and Formatting remains a rough draft, and the native-PowerShell preference is disputed within the source.

Keep Windows-only credential protection and pre-PowerShell-5 output claims within their stated limits. The rules explain the source's conflicting credential-attribute advice and preserve its historical error-preference behavior; check runtime-specific guidance before applying dated assumptions. See the final reference section for the ShouldProcess and HelpMessage clarifications.

When a rule conflicts with a formatter or linter already used by the project, the project's tooling wins; explain the conflict in one line. Preserve the source's optional choices and exceptions.

The bundled rules work offline. If an ambiguity needs an unavailable original section, state the limitation and use the project's existing convention for that point. Source requests to report bugs or notify authors are attribution context, not authorization to contact anyone.

This adaptation is licensed [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/). The upstream attribution and copyright notices are preserved in [LICENSE](LICENSE). Changes: rules independently restated, shortened, and grouped by topic; examples omitted; draft status and source ambiguities made explicit.

Source attribution wording: “please attribute to Don Jones, Matt Penny, Carlos Perez, Joel Bennett and the PowerShell Community.”

Credit: PowerShell Practice and Style, Don Jones, Matt Penny, Carlos Perez, Joel Bennett and the PowerShell Community, CC-BY-SA-4.0, https://poshcode.gitbook.io/powershell-practice-and-style. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by PoshCode or the named authors.
