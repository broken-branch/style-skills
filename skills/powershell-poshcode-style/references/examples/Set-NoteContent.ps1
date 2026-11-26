# [POSH-STYLE] ShouldProcess, READ-02 splatting and DOC-01 help.
# Rules: You should support -WhatIf; Using [switch]; full parameter names.
#requires -Version 5.0
<#
    .SYNOPSIS
    Replaces a note's text with explicit WhatIf and Confirm support.

    .EXAMPLE
    $script = Join-Path -Path $PSScriptRoot -ChildPath 'Set-NoteContent.ps1'
    $note = Join-Path -Path $PSScriptRoot -ChildPath 'note.txt'
    & $script -LiteralPath $note -Text 'ready' -WhatIf

    Previews the write without creating or replacing the file.

    .NOTES
    Existing contents are replaced. Encoding follows the target runtime's UTF8
    behavior, which differs in BOM handling between Windows PowerShell and pwsh.
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium')]
[OutputType([void])]
param (
    # The destination path; its parent directory must already exist.
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$LiteralPath,

    # Complete replacement text; an empty string is accepted.
    [Parameter(Mandatory)]
    [AllowEmptyString()]
    [string]$Text,

    # Suppresses the otherwise appended newline when enabled.
    [switch]$NoNewline
)

end {
    if ($PSCmdlet.ShouldProcess($LiteralPath, 'Replace note content')) {
        $writeParameters = @{
            LiteralPath = $LiteralPath
            Value = $Text
            Encoding = 'UTF8'
            NoNewline = $NoNewline
            ErrorAction = 'Stop'
        }
        Set-Content @writeParameters
    }
}

