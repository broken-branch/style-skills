# House rules: execution-phase fixtures and isolated TestDrive data [PESTER];
# zero/one/many outputs [PS-OUTPUT], literal paths, and error behavior [MS-CMDLET].
#requires -Version 7.6
<#
.SYNOPSIS
Test the artifact module with Pester 5.9.1.
.DESCRIPTION
Creates temporary files in Pester's TestDrive; no existing files are changed.
Run through Invoke-Pester rather than dot-sourcing this test file.
.INPUTS
None.
.OUTPUTS
None. Pester owns the test report and failure results.
.EXAMPLE
Invoke-Pester -Path ./ArtifactTools.Tests.ps1
Run the pipeline, literal-path, and error-contract checks.
#>

BeforeAll -Scriptblock {
    $modulePath = Join-Path -Path $PSScriptRoot -ChildPath 'ArtifactTools.psd1'
    Import-Module -Name $modulePath -ErrorAction Stop
}

Describe -Name 'Get-ArtifactFile' -Fixture {
    BeforeEach -Scriptblock {
        $filePath = Join-Path -Path $TestDrive -ChildPath 'report[1].txt'
        $otherPath = Join-Path -Path $TestDrive -ChildPath 'other.txt'
        $missingPath = Join-Path -Path $TestDrive -ChildPath 'missing.txt'
        Set-Content -LiteralPath $filePath -Value 'first' -ErrorAction Stop
        Set-Content -LiteralPath $otherPath -Value 'second' -ErrorAction Stop
    }

    It -Name 'emits nothing for an empty pipeline' -Test {
        $items = @(@() | Get-ArtifactFile)
        $items.Count | Should -Be 0
    }

    It -Name 'returns one file with literal brackets in its name' -Test {
        $items = @(Get-ArtifactFile -LiteralPath $filePath)
        $items.Count | Should -Be 1
        $items[0] | Should -BeOfType ([System.IO.FileInfo])
        $items[0].Name | Should -Be 'report[1].txt'
    }

    It -Name 'returns one object for each pipeline input' -Test {
        $items = @($filePath, $otherPath | Get-ArtifactFile)
        $items.Count | Should -Be 2
        $items[0].Name | Should -Be 'report[1].txt'
        $items[1].Name | Should -Be 'other.txt'
        $items[1] | Should -BeOfType ([System.IO.FileInfo])
    }

    It -Name 'binds an exact LiteralPath property' -Test {
        $items = @([pscustomobject]@{ LiteralPath = $filePath } | Get-ArtifactFile)
        $items.Count | Should -Be 1
        $items[0].Name | Should -Be 'report[1].txt'
    }

    It -Name 'reports a missing path and continues to the next file' -Test {
        $items = @(
            $missingPath, $filePath |
                Get-ArtifactFile -ErrorAction SilentlyContinue -ErrorVariable failures
        )
        $items.Count | Should -Be 1
        $items[0].Name | Should -Be 'report[1].txt'
        $failures.Count | Should -Be 1
    }

    It -Name 'honors terminating errors requested by the caller' -Test {
        { Get-ArtifactFile -LiteralPath $missingPath -ErrorAction Stop } |
            Should -Throw
    }

    It -Name 'rejects directories without adding success output' -Test {
        $items = @(
            Get-ArtifactFile -LiteralPath $TestDrive -ErrorAction SilentlyContinue -ErrorVariable failures
        )
        $items.Count | Should -Be 0
        $failures.Count | Should -Be 1
        $failures[0].FullyQualifiedErrorId | Should -Match '^ArtifactPathIsNotFile,'
    }

    It -Name 'rejects an empty path during parameter binding' -Test {
        { Get-ArtifactFile -LiteralPath '' -ErrorAction Stop } |
            Should -Throw
    }
}
