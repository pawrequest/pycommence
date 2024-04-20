using namespace Vovin.CmcLibNet.Database;
using namespace Newtonsoft.Json.Schema;
using namespace Newtonsoft.Json.Schema.Generation;
using namespace System;
using namespace System.Reflection;

Add-Type -Path "C:\Program Files\Vovin\Vovin.CmcLibNet\Vovin.CmcLibNet.dll"
Add-Type -Path "./Newtonsoft.Json.dll"
Add-Type -Path "./JsonSchema30r15/Bin/net45/Newtonsoft.Json.Schema.dll"

$generator = New-Object Newtonsoft.Json.Schema.Generation.JSchemaGenerator

$schemaMap = New-Object 'System.Collections.Generic.Dictionary[String,Newtonsoft.Json.Schema.JSchema]'

# Fetch all classes in the Vovin.CmcLibNet.Database namespace and generate schemas
$namespace = "Vovin.CmcLibNet.Database"
$types = [System.AppDomain]::CurrentDomain.GetAssemblies() |
        Where-Object { $_.FullName -like "*Vovin.CmcLibNet*" } |
        ForEach-Object {
            $_.GetTypes() |
                    Where-Object { $_.Namespace -eq $namespace -and $_.IsClass }
        }

foreach ($type in $types)
{
    $schema = $generator.Generate($type)
    $schemaMap.Add($type.Name, $schema)
}
# Now, save each individual schema to a separate file
foreach ($key in $schemaMap.Keys) {
    $individualSchema = $schemaMap[$key]
    $individualSchemaString = $individualSchema.ToString()

    # Sanitize the type name to ensure it is a valid filename
    $safeTypeName = $key -replace '[\\\/:*?"<>|]', '_'
    $individualFileName = "C:\Users\RYZEN\prdev\rsrc\" + $safeTypeName + ".json"

    Write-Output "Saving $key Schema to File"
    $individualSchemaString | Out-File -FilePath $individualFileName
}