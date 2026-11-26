<#
Microsoft cmdlet guidelines: [use-singular-parameter-names] array parameters;
[parameters-that-take-true-and-false] switch flag;
[make-cmdlets-case-insensitive-and-case-preserving-sc04] preserve spelling;
[support-wildcard-characters] wildcard filters; stream each matching record.
#>
function Select-TextLine {
    <#
    .SYNOPSIS
    Selects text using case-insensitive wildcard patterns.
    .EXAMPLE
    'Map.md', 'notes.txt' | Select-TextLine -Pattern '*.MD'
    .EXAMPLE
    'Map.md', 'notes.txt' | Select-TextLine -Pattern '*.MD' -NotMatch
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param (
        [Parameter(Mandatory, ValueFromPipeline)]
        [AllowEmptyString()]
        [string[]] $InputObject,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string[]] $Pattern,

        [switch] $NotMatch
    )

    process {
        foreach ($Line in $InputObject) {
            $MatchesPattern = $false
            foreach ($Candidate in $Pattern) {
                if ($Line -like $Candidate) {
                    $MatchesPattern = $true
                    break
                }
            }

            if ($MatchesPattern -ne $NotMatch.IsPresent) {
                $PSCmdlet.WriteObject($Line)
            }
        }
    }
}
