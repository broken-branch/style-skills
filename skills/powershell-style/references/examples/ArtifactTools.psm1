# House rules: validated advanced pipeline commands and help [POSH-STYLE];
# literal paths [MS-CMDLET], typed output [PS-OUTPUT], and per-item errors [PS-ADVANCED].
#requires -Version 7.6

function Get-ArtifactFile {
    <#
    .SYNOPSIS
    Read file metadata for one literal path at a time.
    .DESCRIPTION
    Emits file objects without changing files or requesting confirmation.
    Missing or unreadable paths and non-file items produce per-item errors.
    Processing continues unless the caller selects -ErrorAction Stop.
    .PARAMETER LiteralPath
    One exact file path, supplied directly or by pipeline value or property name.
    Wildcards are not expanded. Pipe multiple paths rather than passing an array.
    .INPUTS
    System.String. One path per pipeline record.
    .OUTPUTS
    System.IO.FileInfo. One object for each successfully inspected file.
    .EXAMPLE
    Get-ArtifactFile -LiteralPath './report[1].txt'
    Read an existing file whose name contains literal brackets.
    .EXAMPLE
    './first.txt', './second.txt' | Get-ArtifactFile
    Read metadata for two existing files without formatting the objects.
    #>
    [CmdletBinding()]
    [OutputType([System.IO.FileInfo])]
    param (
        [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
        [ValidateNotNullOrEmpty()]
        [string]$LiteralPath
    )

    process {
        try {
            $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
        } catch {
            $PSCmdlet.WriteError($_)
            return
        }

        if ($item -isnot [System.IO.FileInfo]) {
            $exception = [System.ArgumentException]::new('The path must identify a file.')
            $record = [System.Management.Automation.ErrorRecord]::new(
                $exception,
                'ArtifactPathIsNotFile',
                [System.Management.Automation.ErrorCategory]::InvalidArgument,
                $LiteralPath
            )
            $PSCmdlet.WriteError($record)
            return
        }

        $item
    }
}

Export-ModuleMember -Function Get-ArtifactFile -Cmdlet @() -Alias @() -Variable @()
