---
name: powershell-style
description: "Write, edit, or review .ps1, .psm1, and .psd1 using house PowerShell style unless another guide is requested."
license: CC-BY-4.0
metadata:
  kind: house
  language: powershell
  version: "1.0.0"
  source-url: "references/sources.md"
  treatment: original-synthesis
---

# PowerShell style (house)

Our blend of the best PowerShell guides, in our own words. Every rule in the full guide names its source.

Scope: PowerShell 7.6 LTS scripts and script modules on supported Windows, Linux, and macOS hosts in FullLanguage mode; reference runtime 7.6.6. Windows PowerShell 5.1, binary cmdlet implementation, DSC resources, and constrained endpoints require separate profiles.

If the project declares older versions or its own formatter/linter settings, follow the project and say so.

## Quick rules

- MUST name commands with an approved PascalCase verb and a singular PascalCase noun, adding a domain prefix to generic nouns. Why: `Get-Verb` conventions make commands discoverable and reduce collisions. [MS-CMDLET] [PSSA]
- MUST use canonical full command names and full named parameters in committed PowerShell calls; hashtable splatting also counts as named binding. Why: aliases, abbreviations, and positional binding obscure intent and can change meaning. [POSH-STYLE] [PSSA]
- MUST list module exports explicitly in `FunctionsToExport`, `CmdletsToExport`, `AliasesToExport`, and `VariablesToExport`, using `@()` for none. Why: wildcard or implicit exports expose unintended commands and state. [PSSA]
- MUST resolve bundled assets from `$PSScriptRoot` with `Join-Path`, and resolve filesystem paths before passing them to native or .NET APIs. Why: PowerShell provider location and process working directory can differ. [POSH-STYLE] [MS-CMDLET]
- MUST use `-LiteralPath` for exact caller-supplied filenames and implement wildcard expansion only in a documented `Path` interface. Why: brackets and wildcard characters can otherwise select unintended targets. [MS-CMDLET]
- MUST define reusable script commands with `[CmdletBinding()]` and a `param` block. Why: common parameters and advanced binding provide a predictable command interface. [POSH-STYLE] [PSSA]
- MUST give public parameters one specific type and applicable validation attributes, with explicit null or empty allowances where those values are meaningful. Why: PowerShell coercion alone does not express the input contract. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST use `[switch]` for optional flags, leave absent switches false, and forward their values with splatting or `-Flag:$Flag`. Why: presence-only forwarding changes an explicitly false switch to true. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST select `DefaultParameterSetName` whenever named parameter sets exist, keep set spelling consistent, and use at most one by-value pipeline parameter per set. Why: binding needs an unambiguous default and input route. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST process pipeline-bound parameters in `process`, handling each input record there. Why: an implicit end block sees only the final pipeline-bound values. [POSH-STYLE] [PSSA]
- MUST emit raw result objects on the success stream and put diagnostics on verbose, debug, warning, or information streams. Why: callers must be able to pipe results into other commands without parsing status text. [MS-CMDLET] [POSH-STYLE] [PS-OUTPUT]
- MUST declare `[OutputType(...)]` for commands that emit results and keep emitted objects consistent with that declaration. Why: output metadata describes a contract but does not cast or validate runtime results. [POSH-STYLE] [PSSA] [PS-OUTPUT]
- MUST capture or discard incidental success output with an assignment or `[void]` in reusable functions. Why: every uncaptured expression contributes to the result, even before `return`. [PS-OUTPUT]
- MUST put `$null` on the left of equality comparisons. Why: a collection on the left makes PowerShell filter elements instead of perform a scalar null test. [PSSA]
- MUST use `-ErrorAction Stop` on fallible cmdlet calls when subsequent work depends on success or a `catch` must handle the failure. Why: ordinary nonterminating errors otherwise let the dependent statements continue. [POSH-STYLE] [PS-ERRORS]
- MUST check a native command's exit code immediately and interpret it using that program's success-code contract. Why: the house uses explicit `$LASTEXITCODE` handling rather than relying on `$PSNativeCommandUseErrorActionPreference`, and success codes vary by program. [PS-ERRORS]
- MUST scope preference changes locally and restore any temporary change in the same scope with `finally`. Why: assigning a guessed default afterward can overwrite the caller's policy. [PS-ERRORS]
- MUST add `SupportsShouldProcess` to state-changing commands and guard every mutation with `$PSCmdlet.ShouldProcess(target, action)`. Why: `-WhatIf` and `-Confirm` require a real decision at the effect boundary. [POSH-STYLE] [PS-SHOULDPROCESS] [PSSA]
- MUST accept `[pscredential]$Credential` for username/password authentication and let the caller obtain the credential. Why: reusable automation must not unexpectedly prompt or expose a password parameter. [POSH-STYLE] [PS-CREDENTIAL] [PSSA]
- MUST treat credential `Export-Clixml` protection as Windows-only and avoid using it as encrypted secret storage on Linux or macOS. Why: non-Windows credential exports are reversible text, not encrypted credentials. [PS-CLIXML]
- MUST invoke commands directly or with `&` and separate arguments instead of `Invoke-Expression`. Why: constructed PowerShell text is executable syntax rather than an argument value. [PSSA]
- MUST restrict `Write-Host` to deliberately interactive `Show-*` functions. Why: its display output is not reusable success-stream data, and the analyzer's exception is limited to the Show verb. [PSSA] [POSH-STYLE]
- MUST give runnable scripts and exported functions useful comment-based help with `.SYNOPSIS`, parameter descriptions, input/output contracts, and a runnable `.EXAMPLE`. Why: `Get-Help` must explain actual use rather than just confirm a help block exists. [POSH-STYLE] [PSSA]
- MUST put Pester tests in `*.Tests.ps1`, with imports and fixture creation in `BeforeAll` or `BeforeEach` and assertions inside `It`. Why: Pester discovery and execution have distinct scopes and phases. [PESTER]
- MUST test that `-WhatIf` leaves state unchanged for state-changing commands, including calls through wrappers. Why: a ShouldProcess declaration does not prove that every effect is guarded. [PS-SHOULDPROCESS] [PESTER]

## When to read more

- Before a change bigger than one function, read [references/guide.md](references/guide.md), the section for what you're doing.
- For naming basics, errors, tests, commits, secrets, and agent workflow, read [references/shared.md](references/shared.md).
- To set up tooling, copy or merge the files in [references/config/](references/config/) into your repository, then read the guide's Tooling section. Use the project's own source files and test fixtures.
- For worked controls, read [advanced pipeline function](references/examples/ArtifactTools.psm1), [explicit module manifest](references/examples/ArtifactTools.psd1), [pipeline and error tests](references/examples/ArtifactTools.Tests.ps1).

## Sources

See [references/sources.md](references/sources.md) for sources, licenses, source tags, and changes. Unofficial: not affiliated with or endorsed by any source's owner.
