<#
Microsoft cmdlet guidelines: [support-parameter-sets] alternative path inputs;
[support-input-from-the-pipeline] arrays and pipeline records;
[support-windows-powershell-paths] provider content and literal paths;
[write-single-records-to-the-pipeline-sc03] stream individual strings.
Script implementation: process and provider cmdlets replace binary APIs.
#>
function Get-TextLine {
    <#
    .SYNOPSIS
    Streams text from a content provider without changing letter case.
    .EXAMPLE
    './draft.txt', './notes.txt' | Get-TextLine
    .EXAMPLE
    Get-TextLine -LiteralPath './notes[1].txt'
    #>
    [CmdletBinding(DefaultParameterSetName = 'Path')]
    [OutputType([string])]
    param (
        [Parameter(Mandatory, Position = 0, ValueFromPipeline,
            ValueFromPipelineByPropertyName, ParameterSetName = 'Path')]
        [Alias('PSPath')]
        [ValidateNotNullOrEmpty()]
        [string[]] $Path,

        [Parameter(Mandatory, ValueFromPipeline,
            ValueFromPipelineByPropertyName, ParameterSetName = 'LiteralPath')]
        [ValidateNotNullOrEmpty()]
        [string[]] $LiteralPath
    )

    process {
        if ($PSCmdlet.ParameterSetName -eq 'LiteralPath') {
            $ContentParameter = @{ LiteralPath = $LiteralPath }
        }
        else {
            $ContentParameter = @{ Path = $Path }
        }

        Write-Verbose 'Reading provider content.'
        Get-Content @ContentParameter
    }
}
