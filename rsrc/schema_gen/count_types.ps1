using namespace System;
using namespace System.Reflection;

# Load the assembly
$assemblyPath = "C:\Program Files\Vovin\Vovin.CmcLibNet\Vovin.CmcLibNet.dll"
$assembly = [Reflection.Assembly]::LoadFrom($assemblyPath)

# Create a dictionary to hold namespaces and their types
$namespaceMap = @{ }

# Iterate over all types in the assembly
foreach ($type in $assembly.GetTypes())
{
    if ($type.Namespace -ne $null)
    {
        # Initialize the namespace key if it doesn't already exist
        if (-not $namespaceMap.ContainsKey($type.Namespace))
        {
            $namespaceMap[$type.Namespace] = New-Object System.Collections.ArrayList
        }
        # Add the type to the namespace in the map
        $namespaceMap[$type.Namespace].Add($type)
    }
}

# Output the namespaces and their types
foreach ($namespace in $namespaceMap.Keys)
{
    Write-Output "Namespace: $namespace"
    foreach ($type in $namespaceMap[$namespace])
    {
        Write-Output "  Type: $( $type.Name )"
    }
}

# write dictionary to file
$namespaceMap | ConvertTo-Json | Out-File -FilePath "./namespaceMap.json" -Encoding utf8
#$namespaceMap | ConvertTo-Json -Depth 100 | Out-File -FilePath "./namespaceMap.json" -Encoding utf8
