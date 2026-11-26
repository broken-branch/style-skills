# [POSH-STYLE] ERR-01, ERR-03, ERR-06: catch per item and retain its error record.
# Rules: TOOL-06 raw data; full command and parameter names; DOC-01 help.
#requires -Version 3.0
<#
    .SYNOPSIS
    Reports each requested filesystem item's name and container status.

    .EXAMPLE
    .\Get-FileRecord.ps1 -LiteralPath $PSCommandPath

    Emits a record for the calling script's file, without formatting it.
#>
[CmdletBinding()]
[OutputType([pscustomobject])]
param (
    # A filesystem path; wildcard characters are treated literally.
    [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
    [ValidateNotNullOrEmpty()]
    [string]$LiteralPath
)

process {
    try {
        $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
        [pscustomobject]@{
            Name = $item.Name
            IsContainer = $item.PSIsContainer
        }
    } catch {
        $failure = $_
        Write-Error -ErrorRecord $failure
    }
}

