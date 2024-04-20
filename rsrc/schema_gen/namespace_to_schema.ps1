using namespace Vovin.CmcLibNet.Database;
using namespace Newtonsoft.Json.Schema;
using namespace Newtonsoft.Json.Schema.Generation;
using namespace System;
using namespace System.Reflection;

Add-Type -Path "C:\Program Files\Vovin\Vovin.CmcLibNet\Vovin.CmcLibNet.dll"
Add-Type -Path "./Newtonsoft.Json.dll"
Add-Type -Path "./JsonSchema30r15/Bin/net45/Newtonsoft.Json.Schema.dll"

$generator = New-Object Newtonsoft.Json.Schema.Generation.JSchemaGenerator

# Fetch all classes in the Vovin.CmcLibNet.Database namespace
$namespace = "Vovin.CmcLibNet.Database"
$types = [System.AppDomain]::CurrentDomain.GetAssemblies() |
         Where-Object { $_.FullName -like "*Vovin.CmcLibNet*" } |
         ForEach-Object {
             $_.GetTypes() |
             Where-Object { $_.Namespace -eq $namespace -and $_.IsClass }
         }

foreach ($type in $types) {
    $schema = $generator.Generate($type)
    $schemaString = $schema.ToString()

    # Sanitize the type name to ensure it is a valid filename
    $safeTypeName = $type.Name -replace '[\\\/:*?"<>|]', '_'
    $fileName = "C:\Users\RYZEN\prdev\rsrc\" + $safeTypeName + ".json"

    Write-Output "Generated Schema for $type.Name: "
    Write-Output $schemaString

    # Save each schema to a separate file
    try {
        $schemaString | Out-File -FilePath $fileName
    } catch {
        Write-Error "Failed to write file for $type.Name. Error: $_"
    }
}
