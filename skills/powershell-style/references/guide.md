# PowerShell style guide

Scope: PowerShell 7.6 LTS scripts and script modules on supported Windows, Linux, and macOS hosts in FullLanguage mode; reference runtime 7.6.6. Windows PowerShell 5.1, binary cmdlet implementation, DSC resources, and constrained endpoints require separate profiles.
Baseline: [shared rules](shared.md), including dependencies, commits, versioning, review, and AI agent workflow.
MUST means required; PREFER means the default, with a reason recorded for departures.
Source tags resolve in [source credits](sources.md#source-tags).

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

## Tooling

| Purpose | Tool and version | Config file | Repository command |
| --- | --- | --- | --- |
| Formatter | Invoke-Formatter, PSScriptAnalyzer 1.25.0 | [PSScriptAnalyzerSettings.psd1](config/PSScriptAnalyzerSettings.psd1) | `Invoke-Formatter -ScriptDefinition (Get-Content -Raw <script.ps1>) -Settings ./PSScriptAnalyzerSettings.psd1` |
| Linter | PSScriptAnalyzer 1.25.0; explicit 60-rule selection | Same settings file | `Invoke-ScriptAnalyzer -Path . -Recurse -Settings ./PSScriptAnalyzerSettings.psd1` |
| Build / type checks | PowerShell parser and Test-ModuleManifest, reference 7.6.6; no static type checker | Project module manifest | `Test-ModuleManifest -Path <module.psd1>` |
| Tests | Pester 5.9.1, deliberately pinned v5 baseline | Project's Pester tests | `Invoke-Pester -Path ./tests` |

Mechanical formatting: the formatter handles this.

- MUST run PSScriptAnalyzer with the supplied explicit rule selection and retain Information and parser diagnostics. Why: a severity filter can hide help, output-contract, and syntax failures. [PSSA-CONFIG]
- MUST use the supplied Invoke-Formatter settings for PowerShell source. Why: formatter-owned layout and spelling corrections stay consistent with lint. [PSSA-CONFIG]
- MUST declare the script minimum with `#requires -Version 7.6` and the module minimum with manifest `PowerShellVersion = '7.6'` for this baseline. Why: incompatible hosts fail before the workload starts. [POSH-STYLE] [PS-LIFECYCLE]

Run the commands in PowerShell from the project root after copying the settings and installing PSScriptAnalyzer 1.25.0 and Pester 5.9.1. Check formatter output by comparison before replacing files, and fail lint on every returned diagnostic, including Information and ParseError records. Retain Pester v5 until the project validates a v6 migration.

Not yet run against PowerShell 7.6.6, PSScriptAnalyzer 1.25.0, or Pester 5.9.1. Loading the config, comparing formatter output, linting, parsing modules and scripts, and running tests remain validation work before adoption.

### Configured diagnostic IDs

Every selected rule appears below. Descriptions summarize detection, not complete semantic guarantees. The released 1.25.0 manuals and formatter source control this inventory. [PSSA] [PSSA-CONFIG]

| Rule ID | Configured coverage / limit |
| --- | --- |
| `PSAvoidAssignmentToAutomaticVariable` | Assignments or parameters that overwrite automatic variables. |
| `PSAvoidDefaultValueForMandatoryParameter` | Defaults on mandatory parameters. |
| `PSAvoidDefaultValueSwitchParameter` | A switch whose default is true. |
| `PSAvoidExclaimOperator` | Formatter-owned logical-negation spelling. |
| `PSAvoidGlobalAliases` | Aliases created with global scope. |
| `PSAvoidGlobalFunctions` | Functions explicitly declared in global scope. |
| `PSAvoidGlobalVars` | Explicit global variables; automatic/preference variables have exceptions. |
| `PSAvoidInvokingEmptyMembers` | Empty or dynamically unresolved member-invocation names. |
| `PSAvoidLongLines` | Configured 120-character diagnostic threshold; no automatic line wrapping. |
| `PSAvoidMultipleTypeAttributes` | Multiple type constraints on one parameter. |
| `PSAvoidNullOrEmptyHelpMessageAttribute` | Empty declared HelpMessage attributes; not missing help prose. |
| `PSAvoidReservedWordsAsFunctionNames` | Reserved words used for function names. |
| `PSAvoidSemicolonsAsLineTerminators` | Formatter-owned redundant statement terminators. |
| `PSAvoidShouldContinueWithoutForce` | ShouldContinue calls without a Force parameter; control flow still needs review. |
| `PSAvoidTrailingWhitespace` | Formatter-owned trailing whitespace. |
| `PSAvoidUsingAllowUnencryptedAuthentication` | Use of AllowUnencryptedAuthentication. |
| `PSAvoidUsingBrokenHashAlgorithms` | Known MD5/SHA-1 hash APIs; not a cryptographic proof. |
| `PSAvoidUsingCmdletAliases` | Resolvable command aliases, with no allowed aliases. |
| `PSAvoidUsingComputerNameHardcoded` | Literal ComputerName arguments. |
| `PSAvoidUsingConvertToSecureStringWithPlainText` | Known plaintext-to-SecureString patterns. |
| `PSAvoidUsingDeprecatedManifestFields` | Deprecated ModuleToProcess in module manifests. |
| `PSAvoidUsingDoubleQuotesForConstantString` | Formatter-owned constant-string quoting, with semantic exceptions. |
| `PSAvoidUsingEmptyCatchBlock` | Empty catches; ineffective recovery remains a review duty. |
| `PSAvoidUsingInvokeExpression` | Invoke-Expression calls. |
| `PSAvoidUsingPlainTextForPassword` | Recognized password/passphrase parameters with plaintext types. |
| `PSAvoidUsingPositionalParameters` | Calls with three or more positional arguments; shorter calls still need review. |
| `PSAvoidUsingUsernameAndPasswordParams` | Separate username/password parameter interfaces. |
| `PSAvoidUsingWMICmdlet` | Legacy WMI cmdlets. |
| `PSAvoidUsingWriteHost` | Write-Host outside functions using the Show verb. |
| `PSMisleadingBacktick` | Whitespace after a continuation backtick. |
| `PSMissingModuleManifestField` | Missing required module manifest fields, including ModuleVersion. |
| `PSPlaceCloseBrace` | Formatter-owned closing-brace placement. |
| `PSPlaceOpenBrace` | Formatter-owned opening-brace placement. |
| `PSPossibleIncorrectComparisonWithNull` | Null on the right of a comparison. |
| `PSPossibleIncorrectUsageOfAssignmentOperator` | Suspicious assignments/equality tokens in conditions; intentional cases can escape. |
| `PSPossibleIncorrectUsageOfRedirectionOperator` | Redirection tokens used as comparison operators. |
| `PSProvideCommentHelp` | Help presence only for functions named in `Export-ModuleMember`; manifest-only exports need review. Generated help starts inside the body. |
| `PSReservedCmdletChar` | Reserved characters in command names. |
| `PSReservedParams` | Redeclaration of reserved/common parameters. |
| `PSReviewUnusedParameter` | Apparently unused parameters; cross-scope uses have inference limits. |
| `PSShouldProcess` | SupportsShouldProcess declaration/call mismatch; not proof of complete guarding. |
| `PSUseApprovedVerbs` | Verbs outside the approved verb list. |
| `PSUseCmdletCorrectly` | Resolvable invocation errors and missing mandatory arguments. |
| `PSUseConsistentIndentation` | Formatter-owned indentation. |
| `PSUseConsistentParameterSetName` | Missing default, inconsistent set spelling, duplicate declarations, and multiline names. |
| `PSUseConsistentParametersKind` | Inline function parameters where ParamBlock is selected. |
| `PSUseConsistentWhitespace` | Formatter-owned token spacing. |
| `PSUseCorrectCasing` | Canonical resolvable command/parameter/type spelling and keyword/operator casing. |
| `PSUseDeclaredVarsMoreThanAssignments` | Assigned variables not read in the analyzed scriptblock; cross-scope limits apply. |
| `PSUseLiteralInitializerForHashtable` | Hashtable constructor forms with unintended case-sensitive key behavior. |
| `PSUseOutputTypeCorrectly` | Statically inferred output inconsistent with OutputType; dynamic output needs tests. |
| `PSUseProcessBlockForPipelineCommand` | Pipeline parameters used without a process block. |
| `PSUsePSCredentialType` | Credential parameters not typed PSCredential. |
| `PSUseShouldProcessForStateChangingFunctions` | Missing SupportsShouldProcess for recognized state-changing verbs. |
| `PSUseSingleValueFromPipelineParameter` | Multiple by-value pipeline declarations grouped by parameter-set name. |
| `PSUseSingularNouns` | Plural command nouns, except the configured Data and Windows exemptions. |
| `PSUseSupportsShouldProcess` | Handwritten WhatIf/Confirm parameters. |
| `PSUseToExportFieldsInManifest` | Missing, null, or wildcard export fields. |
| `PSUseUsingScopeModifierInNewRunspaces` | Unqualified outer variables in recognized remote/job/parallel scriptblocks. |
| `PSUseUTF8EncodingForHelpFile` | Detected encoding of about_*.help.txt files; no general BOM-free-source guarantee. |

### Deliberate gaps and overrides

`PSProvideCommentHelp` has `ExportedOnly = true` and `Placement = 'begin'`; its [released rule manual](https://github.com/PowerShell/PSScriptAnalyzer/blob/1.25.0/docs/Rules/ProvideCommentHelp.md) limits presence checking to functions exported with `Export-ModuleMember`. Manifest-only exports still require full help, checked in review. Help quality and existing placement also need review. Positional-argument and alias allowlists are empty. The formatter's supported rules also have entries under `Rules`, including the otherwise nonconfigurable `PSAvoidTrailingWhitespace`; Invoke-Formatter selects from those entries. The 120-character lint limit reports long lines but does not reflow strings or comments. [PSSA] [PSSA-CONFIG]

`PSAlignAssignmentStatement` is not selected; the configured whitespace rule owns assignment spacing. `PSUseBOMForUnicodeEncodedFile` is omitted for the modern UTF-8 profile. `PSAvoidOverwritingBuiltInCmdlets` and `PSUseCompatibleCmdlets`, `PSUseCompatibleCommands`, `PSUseCompatibleSyntax`, and `PSUseCompatibleTypes` are omitted rather than presenting old bundled profiles as a verified 7.6 platform matrix. Parsing on the declared runtime, command-collision review, and tests on supported hosts remain necessary. [PSSA]

`PSUseConstrainedLanguageMode` and the seven `PSDSC*` rules are outside this scope. Newer PSScriptAnalyzer releases add `PSAvoidDynamicallyCreatingVariableNames`, `PSAvoidUsingArrayList`, `PSInvalidMultiDotValue`, and `PSMissingTryBlock`; version 1.25.0 lacks them, so they are not enabled. [PSSA]

Manual review covers public identifier casing and domain prefixes, named/fully spelled parameters missed by static binding, CmdletBinding presence, complete mutation guards, stream purity, native exit contracts, help usefulness, general source encoding, and compatibility. Runtime tests cover binding, validation, output cardinality, provider behavior, and error propagation. The single-pipeline-parameter check groups declarations by set name; interactions with all-sets parameters and nested scopes still need review. [PSSA] [PS-OUTPUT]

## Naming

- MUST name commands with an approved PascalCase verb and a singular PascalCase noun, adding a domain prefix to generic nouns. Why: `Get-Verb` conventions make commands discoverable and reduce collisions. [MS-CMDLET] [PSSA]
- MUST use canonical full command names and full named parameters in committed PowerShell calls; hashtable splatting also counts as named binding. Why: aliases, abbreviations, and positional binding obscure intent and can change meaning. [POSH-STYLE] [PSSA]
- MUST use PascalCase for public parameters, properties, classes, enums, and module names, preserving names imposed by external contracts. Why: PowerShell's public surface follows consistent casing despite case-insensitive lookup. [POSH-STYLE] [MS-CMDLET]
- PREFER camelCase for private local variables. Why: locals stay distinct from the discoverable command interface. [POSH-STYLE]
- PREFER standard singular PascalCase parameter names such as `Name`, `LiteralPath`, and `ComputerName`. Why: callers can reuse familiar PowerShell parameter vocabulary. [MS-CMDLET]
- MUST keep automatic variable names such as `$input`, `$args`, and `$Error` out of user-defined parameter and local declarations. Why: shadowing runtime state changes PowerShell behavior. [PSSA]

## Files and layout

- PREFER reusable commands in `.psm1` modules with `.psd1` manifests and thin `.ps1` workflow entry points. Why: module scope separates reusable operations from orchestration. [POSH-STYLE]
- MUST list module exports explicitly in `FunctionsToExport`, `CmdletsToExport`, `AliasesToExport`, and `VariablesToExport`, using `@()` for none. Why: wildcard or implicit exports expose unintended commands and state. [PSSA]
- MUST use `RootModule` and `ModuleVersion` in module manifests and declare module dependencies in `RequiredModules`. Why: loading and command discovery depend on accurate manifest metadata. [PSSA] [POSH-STYLE]
- MUST keep module initialization from changing global aliases, global functions, or caller preferences. Why: importing a module must not alter unrelated commands in the session. [PSSA] [PS-ERRORS]
- MUST resolve bundled assets from `$PSScriptRoot` with `Join-Path`, and resolve filesystem paths before passing them to native or .NET APIs. Why: PowerShell provider location and process working directory can differ. [POSH-STYLE] [MS-CMDLET]
- MUST use `-LiteralPath` for exact caller-supplied filenames and implement wildcard expansion only in a documented `Path` interface. Why: brackets and wildcard characters can otherwise select unintended targets. [MS-CMDLET]
- MUST save PowerShell 7 source and `about_*.help.txt` files as UTF-8 without a BOM in this profile. Why: modern PowerShell and Unix tooling share this encoding without the Windows PowerShell 5.1 ambiguity. [PS-ENCODING] [PSSA]

## Types and data

- MUST define reusable script commands with `[CmdletBinding()]` and a `param` block. Why: common parameters and advanced binding provide a predictable command interface. [POSH-STYLE] [PSSA]
- MUST give public parameters one specific type and applicable validation attributes, with explicit null or empty allowances where those values are meaningful. Why: PowerShell coercion alone does not express the input contract. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST use `[switch]` for optional flags, leave absent switches false, and forward their values with splatting or `-Flag:$Flag`. Why: presence-only forwarding changes an explicitly false switch to true. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST omit default values on mandatory parameters and avoid redeclaring common parameters such as `Verbose` or `ErrorAction`. Why: advanced binding owns prompting and common-parameter behavior. [PSSA]
- MUST select `DefaultParameterSetName` whenever named parameter sets exist, keep set spelling consistent, and use at most one by-value pipeline parameter per set. Why: binding needs an unambiguous default and input route. [POSH-STYLE] [MS-CMDLET] [PSSA]
- MUST process pipeline-bound parameters in `process`, handling each input record there. Why: an implicit end block sees only the final pipeline-bound values. [POSH-STYLE] [PSSA]
- MUST emit raw result objects on the success stream and put diagnostics on verbose, debug, warning, or information streams. Why: callers must be able to pipe results into other commands without parsing status text. [MS-CMDLET] [POSH-STYLE] [PS-OUTPUT]
- MUST declare `[OutputType(...)]` for commands that emit results and keep emitted objects consistent with that declaration. Why: output metadata describes a contract but does not cast or validate runtime results. [POSH-STYLE] [PSSA] [PS-OUTPUT]
- MUST capture or discard incidental success output with an assignment or `[void]` in reusable functions. Why: every uncaptured expression contributes to the result, even before `return`. [PS-OUTPUT]
- MUST put `$null` on the left of equality comparisons. Why: a collection on the left makes PowerShell filter elements instead of perform a scalar null test. [PSSA]
- PREFER `@(...)` when collecting command results that callers will count or index, and document intentionally returning a collection as one object. Why: pipeline enumeration changes zero, one, and many-result shapes. [PS-OUTPUT]
- PREFER literal `@{}` dictionaries for ordinary PowerShell keys and `[pscustomobject]` for records with named output properties. Why: these forms fit PowerShell's case-insensitive lookup and object pipeline. [PSSA] [POSH-STYLE]

## Errors

- MUST NOT rely on `$PSNativeCommandUseErrorActionPreference` for native failure handling in this profile; set it to `$false` in a child scriptblock around native calls, then immediately inspect `$LASTEXITCODE` and raise or return the appropriate error. Why: scoped explicit handling respects program-specific success codes without changing the caller's preference. [PS-ERRORS]

- MUST use `-ErrorAction Stop` on fallible cmdlet calls when subsequent work depends on success or a `catch` must handle the failure. Why: ordinary nonterminating errors otherwise let the dependent statements continue. [POSH-STYLE] [PS-ERRORS]
- MUST check a native command's exit code immediately and interpret it using that program's success-code contract. Why: the house uses explicit `$LASTEXITCODE` handling rather than relying on `$PSNativeCommandUseErrorActionPreference`, and success codes vary by program. [PS-ERRORS]
- MUST scope preference changes locally and restore any temporary change in the same scope with `finally`. Why: assigning a guessed default afterward can overwrite the caller's policy. [PS-ERRORS]
- MUST rethrow with bare `throw` when a catch cannot recover, and use `finally` for disposal of resources acquired by that operation. Why: the original error record and cleanup survive exceptional exits. [PS-ERRORS]
- PREFER `$PSCmdlet.WriteError()` with an identified `ErrorRecord` for recoverable per-item failures and `$PSCmdlet.ThrowTerminatingError()` for command-level failure. Why: advanced commands can expose categories and target objects through PowerShell's error contract. [PS-ADVANCED]

## Comments and docs

- PREFER a concise `.SYNOPSIS` and useful parameter help for private functions, adding `.EXAMPLE` only when usage needs explanation. Why: private helpers need context rather than mandatory boilerplate. [POSH-STYLE] [PSSA]

- MUST give runnable scripts and exported functions useful comment-based help with `.SYNOPSIS`, parameter descriptions, input/output contracts, and a runnable `.EXAMPLE`. Why: `Get-Help` must explain actual use rather than just confirm a help block exists. [POSH-STYLE] [PSSA]
- PREFER function help inside the opening function body before `[CmdletBinding()]` and `param`. Why: help remains attached to the implementation, matching the configured `Placement = 'begin'` correction. [POSH-STYLE] [PSSA]
- MUST describe wildcard behavior, emitted types, failure behavior, and mutation or confirmation semantics in a command's help. Why: those PowerShell contracts cannot be inferred from parameter names alone. [POSH-STYLE] [MS-CMDLET]
- PREFER external format/type data for custom object presentation and terminal formatting at the workflow boundary. Why: embedding `Format-*` in reusable tools replaces domain objects with formatting records. [POSH-STYLE] [MS-CMDLET]

## Testing

- MUST put Pester tests in `*.Tests.ps1`, with imports and fixture creation in `BeforeAll` or `BeforeEach` and assertions inside `It`. Why: Pester discovery and execution have distinct scopes and phases. [PESTER]
- MUST test zero, one, and many pipeline inputs, direct array input when supported, and the type and count of success-stream output. Why: binding and automatic enumeration can silently drop or add results. [PS-OUTPUT] [POSH-STYLE] [PESTER]
- MUST test that `-WhatIf` leaves state unchanged for state-changing commands, including calls through wrappers. Why: a ShouldProcess declaration does not prove that every effect is guarded. [PS-SHOULDPROCESS] [PESTER]
- MUST exercise terminating and nonterminating error paths, native failure codes where used, and literal paths containing wildcard characters. Why: PowerShell's separate error and provider semantics need observable regression checks. [PS-ERRORS] [MS-CMDLET] [PESTER]
- PREFER Pester `TestDrive:` for filesystem tests, recreating modified fixtures per test. Why: TestDrive removes temporary files but does not undo changes to inherited fixtures. [PESTER]

## Performance

- PREFER producing each result in `process` as soon as it is ready and avoid materializing entire upstream pipelines without an algorithmic need. Why: streaming bounds intermediate memory and starts downstream work earlier. [MS-CMDLET] [POSH-STYLE]
- MUST treat `$using:` input to thread jobs or parallel runspaces as shared data unless copied or protected for concurrent access. Why: runspace separation does not make mutable referenced objects thread-safe. [PS-REMOTE]

## Security

- MUST add `SupportsShouldProcess` to state-changing commands and guard every mutation with `$PSCmdlet.ShouldProcess(target, action)`. Why: `-WhatIf` and `-Confirm` require a real decision at the effect boundary. [POSH-STYLE] [PS-SHOULDPROCESS] [PSSA]
- MUST implement `WhatIf` and `Confirm` through `SupportsShouldProcess`, and keep a `Force` bypass for `ShouldContinue` separate from the ShouldProcess decision. Why: Force must not silently bypass a caller's dry run. [PSSA] [PS-SHOULDPROCESS]
- MUST accept `[pscredential]$Credential` for username/password authentication and let the caller obtain the credential. Why: reusable automation must not unexpectedly prompt or expose a password parameter. [POSH-STYLE] [PS-CREDENTIAL] [PSSA]
- PREFER omitting `[System.Management.Automation.Credential()]` in unattended APIs and adding it only in an explicitly interactive adapter that accepts usernames. Why: credential transformation can invoke a host prompt and does not promise a Windows dialog. [PS-CREDENTIAL]
- MUST treat credential `Export-Clixml` protection as Windows-only and avoid using it as encrypted secret storage on Linux or macOS. Why: non-Windows credential exports are reversible text, not encrypted credentials. [PS-CLIXML]
- MUST invoke commands directly or with `&` and separate arguments instead of `Invoke-Expression`. Why: constructed PowerShell text is executable syntax rather than an argument value. [PSSA]
- MUST avoid `ConvertTo-SecureString -AsPlainText` on password literals, plaintext password parameters, and `-AllowUnencryptedAuthentication`. Why: those APIs can expose credentials before their apparent protection applies. [PSSA]
- MUST use CIM commands rather than removed WMI cmdlets and accept remote targets through parameters. Why: PowerShell 7 automation cannot depend on the legacy WMI command set or a hardcoded host. [PSSA]
- MUST validate CLM-targeted code under its actual application-control policy and avoid unsupported dynamic compilation, types, or classes there. Why: FullLanguage examples and signature-text detection cannot establish constrained-runtime permission. [PSSA]

## Language-specific pitfalls

- MUST restrict `Write-Host` to deliberately interactive `Show-*` functions. Why: its display output is not reusable success-stream data, and the analyzer's exception is limited to the Show verb. [PSSA] [POSH-STYLE]
- MUST use PowerShell comparison operators such as `-eq` and `-gt`, keeping assignment and redirection out of conditions unless assignment is deliberate and explicit. Why: `=`, `==`, and `>` do not mean C-style comparison. [PSSA]
- PREFER hashtable splatting and natural syntax continuation over backtick line continuation. Why: trailing characters after a backtick can change parsing. [POSH-STYLE] [PSSA]
- MUST pass outside values into remote commands and jobs through explicit parameters or `$using:` as supported by the execution mechanism. Why: a new runspace does not inherit ordinary local-variable binding. [PSSA]
- MUST use native argument passing that matches the target executable and test spaces, embedded quotes, and empty arguments on each supported OS. Why: PowerShell's Windows legacy fallbacks differ from Standard argument passing. [PS-ERRORS]
- MUST preserve filesystem path case and use explicit case-sensitive comparisons when the external protocol requires them. Why: PowerShell's usual case-insensitivity does not define filesystem or protocol semantics. [MS-CMDLET]
- MUST keep `Format-Table`, `Format-List`, and similar formatting commands out of reusable result-producing pipelines. Why: later commands would receive formatting instructions instead of domain data. [POSH-STYLE]

## Where the sources disagree

Where the sources disagree, the following house choices apply. Each choice states the adopted behavior and its reason.

- MUST choose the analyzer's Show-only `Write-Host` exception over PoshCode's rough-draft Format-command, Formatted-switch, and general interactive exceptions. Why: one narrow display boundary matches the default diagnostic and protects reusable output. [POSH-STYLE] [PSSA]
- PREFER the configured `PSAvoidLongLines` threshold of 120 over PoshCode's flexible 115-character target. Why: a single machine-checked setting avoids a second handwritten wrapping policy; Invoke-Formatter does not wrap long lines. [POSH-STYLE] [PSSA]
- PREFER help inside the function before its parameter block, choosing PoshCode's location and `PSProvideCommentHelp.Placement = 'begin'` over the analyzer's generated `before` default. Why: generated help stays close to the function it describes. [POSH-STYLE] [PSSA]
- MUST require full help for exported functions and runnable scripts, departing from PoshCode's every-function requirement with `ExportedOnly = true`; prefer concise help for private helpers. Why: public contracts need examples, while private implementation details should not require narration. [POSH-STYLE] [PSSA]
- MUST use full named parameters in committed PowerShell calls even where the analyzer tolerates one or two positional arguments. Why: the stricter published naming policy is clearer and the three-argument lint threshold is only partial coverage. [POSH-STYLE] [PSSA]
- MUST use full command names, choosing published PoshCode naming and the analyzer over PoshCode's unpublished internal-alias proposal. Why: a TODO proposal does not justify hidden command vocabulary in maintained code. [POSH-STYLE] [PSSA]
- PREFER a caller-supplied PSCredential without implicit prompting for automation; use an explicit Credential() attribute only for intentional interactive conversion. Why: PoshCode's Security and Parameter Blocks chapters disagree, while Microsoft documents the attribute's conversion purpose and the analyzer checks only typing. [POSH-STYLE] [PS-CREDENTIAL] [PSSA]
- MUST choose UTF-8 without BOM for this PowerShell 7 profile and leave `PSUseBOMForUnicodeEncodedFile` unselected. Why: modern encoding guidance and the UTF-8 help rule permit it, whereas the general BOM rule reflects a different compatibility need; Windows PowerShell 5.1 needs its own profile. [PSSA] [PS-ENCODING]
- MUST apply CLM restrictions only to explicitly CLM-targeted deployment profiles, leaving `PSUseConstrainedLanguageMode` unselected in this FullLanguage baseline. Why: PoshCode's draft Add-Type advice assumes capabilities that a constrained host may deny; adding the CLM checker with `Enable = true` and `IgnoreSignatures = true` still does not replace runtime policy testing. [POSH-STYLE] [PSSA]
