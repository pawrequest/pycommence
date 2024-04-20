using namespace Newtonsoft.Json.Schema;
using namespace Newtonsoft.Json.Schema.Generation;
using namespace System;
using namespace System.Reflection;

Add-Type -Path "C:\Program Files\Vovin\Vovin.CmcLibNet\Vovin.CmcLibNet.dll"
Add-Type -Path "C:\Program Files (x86)\Commence\Commence RM\Newtonsoft.Json.dll"
Add-Type -Path "./JsonSchema30r15/Bin/net45/Newtonsoft.Json.Schema.dll"

$generator = New-Object Newtonsoft.Json.Schema.Generation.JSchemaGenerator

# Initialize the composite schema
$compositeSchema = New-Object Newtonsoft.Json.Schema.JSchema
$compositeSchema.Id = new-object Uri("http://example.com/vovin/composite")
$compositeSchema.Type = [Newtonsoft.Json.Schema.JSchemaType]::Object
$compositeSchema.Definitions = new-object Newtonsoft.Json.Schema.JSchemaDictionary

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
    $compositeSchema.Definitions.Add($type.Name, $schema)
}

# Convert the composite schema to JSON
$schemaString = $compositeSchema.ToString()

# Output and save the composite schema
Write-Output "Generated Composite Schema: "
Write-Output $schemaString
$schemaString | Out-File -FilePath "C:\Users\RYZEN\prdev\rsrc\compositeSchema.json"

# Now, split and save each individual schema to a separate file
foreach ($key in $compositeSchema.Definitions.Keys)
{
    $individualSchema = $compositeSchema.Definitions[$key]
    $individualSchemaString = $individualSchema.ToString()
    $individualFileName = "C:\Users\RYZEN\prdev\rsrc\" + $key + ".json"
    Write-Output "Saving $key Schema to File"
    $individualSchemaString | Out-File -FilePath $individualFileName
}
