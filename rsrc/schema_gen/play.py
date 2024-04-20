import json
import re
from pprint import pprint

COM_DEFINITION = r'C:\Users\RYZEN\prdev\workbench\pycommence\src\pycommence\wrapper\_icommence.py'
REFLECTION = r'C:\Users\RYZEN\prdev\workbench\pycommence\rsrc\schema_gen\namespaceMap.json'


def load_reflection_data(file_path=REFLECTION):
    with open('namespaceMap.json', encoding='utf-8-sig') as json_file:
        namespaces = json.load(json_file)
        return namespaces


def parse_python_com_code(file_path=COM_DEFINITION):
    methods = {}
    pattern = r'def (\w+)\(self(, [^)]+)?\):'
    with open(file_path) as file:
        content = file.read()
    matches = re.finditer(pattern, content)
    for match in matches:
        method_name = match.group(1)
        parameters = match.group(2)
        if parameters:
            params = [param.strip().split('=')[0].strip() for param in parameters.split(',') if
                      param.strip()]
        else:
            params = []
        methods[method_name] = params
    return methods


def generate_json_schema(reflection_data, com_methods):
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'title': 'COM Library API',
        'type': 'object',
        'properties': {}
    }
    for method_name, params in com_methods.items():
        method_info = reflection_data.get(method_name, {})
        param_details = {param: {'type': 'string'} for param in params}  # Simplistic assumption
        schema['properties'][method_name] = {
            'type': 'object',
            'properties': param_details,
            'required': params,
            'return': {
                'type': 'string',
                'description': f'Returns a result from {method_name}'  # Simplistic assumption
            }
        }
    return schema


# Assuming the file paths are defined
reflection_data = load_reflection_data()
com_methods = parse_python_com_code()
json_schema = generate_json_schema(reflection_data, com_methods)

# Save the schema to a file
with open('api_schema.json', 'w') as file:
    json.dump(json_schema, file, indent=4)


# # pprint(parse_python_com_code(), indent=4)
# pprint(load_reflection_data(), indent=4)