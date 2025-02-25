import json
import re
from pathlib import Path

from utilities import ModelMap


def parse_java_class(java_text):
    def find_class_body(text, start_index):
        """ Find and extract the class body by counting braces. """
        brace_count = 0
        inside_class = False
        class_start = 0

        for index in range(start_index, len(text)):
            if text[index] == '{':
                if not inside_class:
                    inside_class = True
                    class_start = index
                brace_count += 1
            elif text[index] == '}':
                brace_count -= 1
                if brace_count == 0 and inside_class:
                    return text[class_start + 1:index]
        return None  # Return None if no matching braces are found

    def parse_class(class_body, class_name):
        """ Parses fields, methods, and nested classes. """
        field_pattern = r'@(\w+)\((?:\"([^"]+)\"|([\w\.]+))\)\s*\n*\s*public\s+(\w+(?:\s*<[^<>]+>)?)\s+(\w+);?'
        event_name_pattern = r'this\.type\s*=\s*\w+\.(\w+)'

        # Only 1 event name, extract it, group 1 is the event name
        event_name = re.search(event_name_pattern, class_body)

        # Extract Fields
        fields = []
        for field in re.finditer(field_pattern, class_body, re.DOTALL):
            print('Found Field:', field.group(5))  # Variable name

            # Determine annotation value (string or constant reference)
            annotation_value = field.group(2) if field.group(2) else field.group(3)
            fields.append({
                "name": field.group(5),  # Variable name
                "annotation": annotation_value,  # String or constant reference
                "type": field.group(4),  # Field type
            })

        # Find and Parse Nested Classes
        nested_class_pattern = r'\bclass\s+(\w+)(\s+extends\s+\w+(\s*,\s*\w+)*)?(\s+implements\s+\w+(\s*,\s*\w+)*)?\s*\{'
        nested_classes = {}

        for nested in re.finditer(nested_class_pattern, class_body, re.DOTALL):
            nested_name = nested.group(1)
            nested_start_index = nested.end() - 1  # Position after class declaration
            nested_body = find_class_body(class_body, nested_start_index)
            if nested_body:
                print('Found Nested Class:', nested_name)
                nested_classes[nested_name] = parse_class(nested_body, nested_name)

        class_data = {
            "class_name": class_name,
            "fields": fields,
            "nested_classes": nested_classes,
            "event_name": enum_map.get(event_name.group(1) if event_name else None, None)
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

    # Find the Outer Class
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


def de_duplicate_fields(model_map_data):
    """
    If the field exists on a nested class, remove it from the parent class.
    Recursively

    """

    def remove_duplicates(fields, nested_classes):
        for nested_class in nested_classes:
            nested_fields = nested_classes[nested_class]['fields']
            for field in nested_fields:
                if field in fields:
                    fields.remove(field)
            remove_duplicates(fields, nested_classes[nested_class]['nested_classes'])

    remove_duplicates(model_map_data['fields'], model_map_data['nested_classes'])
    return model_map_data


skipped = 0

for idx, file in enumerate(model_files):
    model_map = model_maps / f"{file.stem}.json"

    if model_map.exists():
        skipped += 1
        continue
    else:
        print(f'Parsing Model {idx + 1}/{len(model_files)}: {file.stem}')

    model_map_data: ModelMap = parse_java_class(file.read_text())
    with open(model_map, 'w') as f:
        f.write(json.dumps(model_map_data, indent=4))

print(f'Skipped {skipped} files')
