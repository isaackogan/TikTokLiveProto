import json
import re
from pathlib import Path

from utilities import ModelMap


def find_class_body(text, start_index):
    """Find and extract the class body by counting braces properly."""
    brace_count = 0
    class_start = -1

    for index in range(start_index, len(text)):
        if text[index] == '{':
            if brace_count == 0:
                class_start = index
            brace_count += 1
        elif text[index] == '}':
            brace_count -= 1
            if brace_count == 0 and class_start != -1:
                return text[class_start + 1:index]
    return None  # Return None if no matching braces are found


field_pattern = r'@(\w+)\((?:\"([^"]+)\"|([\w\.]+))\)\s*\n*\s*(?:private|protected|public)?\s+(\w+(?:\s*<[^<>]+>)?(?:\[\])?)\s+(\w+)(?:\s*=\s*[^;]+)?;'
event_name_pattern = re.compile(r'this\.type\s*=\s*\w+\.(\w+)')

def parse_class(class_body, class_name):
    """Parses fields, methods, and nested classes."""
    # field_pattern = r'@(\w+)\((?:\"([^"]+)\"|([\w\.]+))\)\s*\n*\s*(?:private|protected|public)?\s+(\w+(?:\s*<[^<>]+>)?)\s+(\w+);?'

    fields = []
    for field in re.finditer(field_pattern, class_body, re.DOTALL):
        annotation_value = field.group(2) if field.group(2) else field.group(3)
        fields.append({
            "name": field.group(5),  # Variable name
            "annotation": annotation_value,  # String or constant reference
            "type": field.group(4),  # Field type
        })

    nested_class_pattern = r'\bclass\s+(\w+)(?:\s+extends\s+\w+(?:\s*,\s*\w+)*)?(?:\s+implements\s+\w+(?:\s*,\s*\w+)*)?\s*\{'
    nested_classes = {}

    for nested in re.finditer(nested_class_pattern, class_body, re.DOTALL):
        nested_name = nested.group(1)
        nested_start_index = nested.end() - 1  # Position after class declaration
        nested_body = find_class_body(class_body, nested_start_index)
        if nested_body:
            nested_classes[nested_name] = parse_class(nested_body, nested_name)

    extracted_enum_type = event_name_pattern.search(class_body)
    enum_field = None
    if extracted_enum_type:
        enum_field = extracted_enum_type.group(1)

    class_data = {
        "class_name": class_name,
        "fields": fields,
        "nested_classes": nested_classes,
        "event_name": enum_map.get(enum_field, None) or enum_map_data.get(class_name, None)
    }

    if class_data['event_name']:
        class_data['fields'].insert(
            0,
            {
                "name": "baseMessage",
                "annotation": None,
                "type": "CommonMessageData"
            }
        )

    return class_data


def parse_java_class(java_text):
    """Finds the outer class and initiates parsing."""
    outer_class_match = re.search(r'(?:public\s+|static\s+|final\s+)?class\s+(\w+)', java_text)
    if outer_class_match:
        outer_class_name = outer_class_match.group(1)
        class_start_index = outer_class_match.end() - 1
        outer_class_body = find_class_body(java_text, class_start_index)
        if outer_class_body:
            return parse_class(outer_class_body, outer_class_name)
    return None


models: Path = Path(__file__).parent.parent.parent / './resources/models'
model_maps: Path = Path(__file__).parent.parent.parent / './resources/model_maps'
model_files = [file for file in models.iterdir() if file.suffix == '.java']
enum_map = json.load(open(Path(__file__).parent.parent.parent / './resources/enum_maps/event_map.json', 'r'))
enum_map_data = {v[len('Webcast'):]: v for k, v in enum_map.items()}


def de_duplicate_fields(model_map_data):
    """Remove fields from the parent class if they exist in a nested class."""
    for nested in model_map_data.get('nested_classes', {}).values():
        nested_field_names = {field['name'] for field in nested.get('fields', [])}
        model_map_data['fields'] = [field for field in model_map_data['fields'] if field['name'] not in nested_field_names]
        de_duplicate_fields(nested)
    return model_map_data


skipped = 0

for idx, file in enumerate(model_files):
    model_map = model_maps / f"{file.stem}.json"

    if model_map.exists():
        skipped += 1
        continue

    print(f'Parsing Model {idx + 1}/{len(model_files)}: {file.stem}')
    model_map_data: ModelMap = parse_java_class(file.read_text())

    if model_map_data:
        model_map_data = de_duplicate_fields(model_map_data)
        with open(model_map, 'w') as f:
            f.write(json.dumps(model_map_data, indent=4))

print(f'Skipped {skipped} files')
