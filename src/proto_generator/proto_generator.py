import json
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from modules.enum_map_replacer import resolve_enum_types
from modules.resolve_references import resolve_references

decoder_maps: Path = Path(__file__).parent.parent.parent / './resources/decoder_maps'
model_maps: Path = Path(__file__).parent.parent.parent / './resources/model_maps'

if not decoder_maps.is_dir():
    raise FileNotFoundError(f"Decoder maps directory not found at {decoder_maps}")

model_map_files = []

# Walk through the directory
for root, dirs, files in os.walk(model_maps):

    # Check each file in the current directory
    for file in files:
        # Check if the file ends with '.json'
        if not file.endswith('.json'):
            continue

        model_map_files.append(os.path.join(root, file))

environment = Environment(loader=FileSystemLoader(searchpath=Path(__file__).parent))
proto_template = environment.get_template("proto_template.jinja2")
enum_template = environment.get_template("enum_template.jinja2")

root_messages = []


def de_nest_message(_root_message):
    """Move all messages more than 1 level deep to the 1st level of nested_messages, recursively,
    and prevent adding duplicate messages based on their names."""

    unique_nested_messages = []
    used_nested_message_names = set()

    def traverse(message):
        if 'nested_messages' in message:
            for nested_message in message['nested_messages']:

                if nested_message['name'] in used_nested_message_names:
                    continue

                traverse(nested_message)
                unique_nested_messages.append(nested_message)
                used_nested_message_names.add(nested_message['name'])
            message['nested_messages'] = []

    traverse(_root_message)
    _root_message['nested_messages'] = unique_nested_messages
    return _root_message


for model_map_file in model_map_files:
    model_map = json.loads(Path(model_map_file).read_text())
    references = resolve_references(model_map, decoder_maps)
    references = de_nest_message(references)
    root_messages.append(references)


def replace_event_names(_root_messages):
    """
    If the message has got an 'alias', replace ALL references to the message with the alias, including the message name,
    and updates the types in fields to use the alias if available.
    """

    def build_alias_map(messages, alias_map):
        """Recursively build a map of original names to aliases."""
        for message in messages:
            if 'alias' in message and message['alias']:
                alias_map[message['name']] = message['alias']
                message['name'] = message['alias']  # Update the message name to its alias immediately

            if 'nested_messages' in message:
                build_alias_map(message['nested_messages'], alias_map)

    alias_map = {}
    # Build the alias map for all messages, including nested ones
    build_alias_map(_root_messages, alias_map)

    def replace_aliases_recursive(message, alias_map):
        """Recursively replace all occurrences of the original name with the alias in message types."""
        if message.get('type') in alias_map:
            message['type'] = alias_map[message['type']]

        if 'fields' in message:
            for field in message['fields']:
                if field['type'] in alias_map:
                    field['type'] = alias_map[field['type']]

        if 'nested_messages' in message:
            for nested_message in message['nested_messages']:
                replace_aliases_recursive(nested_message, alias_map)

    # Replace aliases in all messages
    for root_message in _root_messages:
        replace_aliases_recursive(root_message, alias_map)

    return _root_messages


def snake_case_field_names(_root_messages):
    """Convert all field names to snake_case wheras they are currently camelCase."""
    for root_message in _root_messages:

        def snake_case_fields(message):
            for field in message['fields']:
                # convert camelCase to snake_case
                field['name'] = ''.join(['_' + c.lower() if c.isupper() else c for c in field['name']]).lstrip('_')
            for nested_message in message['nested_messages']:
                snake_case_fields(nested_message)

        snake_case_fields(root_message)

    return _root_messages


def split_root_messages(_root_messages):
    """
    Split into event messages (messages starting with Webcast) and data messages, which are part OF
    event messages vis a vis their references.

    """

    event_messages = []
    _data_messages = []

    for message in _root_messages:
        if message['name'].startswith('Webcast'):
            event_messages.append(message)
        # if any fields start with Webcast
        elif any(field['type'].startswith('Webcast') for field in message['fields']):
            event_messages.append(message)
        else:
            _data_messages.append(message)

    return event_messages, _data_messages


root_messages = replace_event_names(root_messages)
top_level_enums = resolve_enum_types(root_messages)

webcast_file_context = {
    "imports": NotImplemented,
    "root_messages": root_messages,
}

data_file_context = {
    "imports": NotImplemented,
    "root_messages": root_messages,
}

enums_file_context = {
    "enums": top_level_enums
}

proto_output = Path(__file__).parent.parent.parent / './resources/proto_output'

if not proto_output.is_dir():
    proto_output.mkdir()

with open(proto_output / 'enums.proto', 'w') as f:
    output = enum_template.render(enums_file_context)
    f.write(output)

with open(proto_output / 'webcast.proto', 'w') as f:
    webcast_file_context['imports'] = ["enums.proto", "data.proto"]
    output = proto_template.render(webcast_file_context)
    f.write(output)

with open(proto_output / 'webcast-snake_case.proto', 'w') as f:
    webcast_file_context['imports'] = ["enums.proto", "data-snake_case.proto"]
    webcast_file_context['root_messages'] = snake_case_field_names(root_messages)
    output = proto_template.render(webcast_file_context)
    f.write(output)

print("Generated proto files in", proto_output)
