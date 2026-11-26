# [POSH-STYLE] TOOL-03, TOOL-06, DOC-01: pipeline objects and raw units.
# Rules: Advanced Functions; Prefer: param (), begin, process, end.
#requires -Version 3.0
<#
    .SYNOPSIS
    Turns named stock measurements into consistent pipeline records.

    .EXAMPLE
    [pscustomobject]@{ Name = 'spare'; Quantity = 12 } | .\ConvertTo-StockRecord.ps1

    Emits one object with the original name and integral quantity.
#>
[CmdletBinding()]
[OutputType([pscustomobject])]
param (
    # The descriptive stock name, supplied directly or by matching property.
    [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
    [ValidateNotNullOrEmpty()]
    [string]$Name,

    # The nonnegative number of units, without display conversion.
    [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
    [ValidateRange(0, 2147483647)]
    [int]$Quantity
)

process {
    [pscustomobject]@{
        Name = $Name
        Quantity = $Quantity
    }
}

