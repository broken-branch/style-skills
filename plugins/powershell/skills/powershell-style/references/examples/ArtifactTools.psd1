# House rules: explicit module exports and metadata [PSSA];
# declare the supported PowerShell baseline [PS-LIFECYCLE].
@{
    RootModule = 'ArtifactTools.psm1'
    ModuleVersion = '1.0.0'
    GUID = 'c761099c-9ed0-481f-9362-bc8095211d4d'
    Author = 'Example contributors'
    Description = 'Read literal file paths as pipeline objects.'
    PowerShellVersion = '7.6'
    RequiredModules = @()
    FunctionsToExport = @('Get-ArtifactFile')
    CmdletsToExport = @()
    AliasesToExport = @()
    VariablesToExport = @()
}
