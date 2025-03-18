import json
import re
from pathlib import Path

import wordninja

# Adjust the base path to fit the actual location of the '__file__' or directly specify the directory path.
web_files: Path = Path(__file__).parent.parent.parent / 'resources' / 'web_js' / 'WebpageSave'
studio_files: Path = Path(__file__).parent.parent.parent / 'resources' / 'web_js' / 'LiveStudioSave'
enum_map: Path = Path(__file__).parent.parent.parent / 'resources' / 'enum_maps' / 'enum_map.json'
event_map: Path = Path(__file__).parent.parent.parent / 'resources' / 'enum_maps' / 'event_map.json'
event_map_data = {v[len('Webcast'):]: v for k, v in json.load(open(event_map, 'r')).items()}


def split_and_format(s: str) -> str:
    """
    >>> split_and_format('DISCORDEXPIREDSUBSCRIBERACTIONTYPEREMOVEROLE7DAYS')
    'DISCORD_EXPIRED_SUBSCRIBER_ACTION_TYPE_REMOVE_ROLE_7_DAYS'

    """

    split_words = wordninja.split(s.upper())
    return "_".join(split_words)


def extract_identifier(full_identifier: str) -> str:
    if 'webcast.im.' in full_identifier:
        identifier = full_identifier.split('im.')[-1]
    elif 'webcast.data.' in full_identifier:
        identifier = full_identifier.split('webcast.data.')[-1]
    else:
        identifier = full_identifier.split(".")[-1]

    return identifier


def find_live_studio_objects(js_content: str) -> list[dict]:
    pattern = r'proto\.(?:webcast|tikcast)\.\w+(?:\.\w+)*\s*=\s*\{[^}]*\};'
    matches = re.findall(pattern, js_content, re.DOTALL)
    match_dicts = []

    for match in matches:
        match = re.sub(r'\s+', '', match).rstrip(";")
        full_identifier, proto = match.split("=")

        proto = (proto.replace("{", '{"').replace(":", '":').replace(",", ',"'))
        last_quote = proto.rfind('"')
        proto = proto[:last_quote - 1] + "}"
        identifier_parts = extract_identifier(full_identifier).split(".")
        identifier_parts[0] = event_map_data.get(identifier_parts[0], identifier_parts[0])

        match_dicts.append(
            {
                full_identifier: {
                    'data': clean_object_literal(json.loads(proto)),
                    'identifier': '.'.join(identifier_parts)
                }
            }
        )

    return match_dicts


def clean_object_literal(dirty_object: dict):
    clean_object = {}

    for k, v in dirty_object.copy().items():
        clean_object[split_and_format(k)] = v

    return clean_object


def find_live_studio_deserializers(
        js_content: str,
) -> list[str]:
    pattern = r'\b(proto\.[\w\.]+?\.deserializeBinaryFromReader\s*=\s*function\s*\(.*?\)\s*\{[\s\S]*?\};)'
    return re.findall(pattern, js_content, re.DOTALL)


def add_references_to_enum(full_identifier: str, enum_object: dict, decoder_literal_list: list[str]):
    enum_object['references'] = {}

    for decoder_literal in decoder_literal_list:

        if full_identifier not in decoder_literal:
            continue

        decoder_name = decoder_literal[:decoder_literal.find("="):].strip()
        decoder_name = decoder_name[:decoder_name.find('.deserializeBinaryFromReader')].strip()
        decoder_lines = decoder_literal.split('\n')
        decoder_identifier = extract_identifier(decoder_name)

        for idx, line in enumerate(decoder_lines):

            if full_identifier not in line:
                continue

            # Move backwards in lines until we find the case line
            case_line = None
            for i, l in enumerate(reversed(decoder_lines[:idx])):
                if 'case' in l:
                    case_line = l
                    break

            case_num: int = int(case_line.split('case ')[-1].split(':')[0])
            decoder_identifier_parts = decoder_identifier.split('.')
            decoder_identifier_parts[0] = event_map_data.get(decoder_identifier_parts[0], decoder_identifier_parts[0])
            decoder_identifier = '.'.join(decoder_identifier_parts)

            if decoder_identifier not in enum_object['references']:
                enum_object['references'][decoder_identifier] = []

            enum_object['references'][decoder_identifier].append(case_num)


if __name__ == '__main__':
    """
    Unfortunately the Java app is not compiled with Enums, but the Web app is.
    So we extract enums from the web app.
    """

    # Iterate through all JS files in the web_files directory and subdirectories
    object_literals = []
    decoder_literals = []
    object_map = {}

    for file in studio_files.rglob('*.js'):  # Using rglob to recursively find .js files
        if file.is_file():  # Checking if it's a file
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                object_literals.extend(find_live_studio_objects(content))
                decoder_literals.extend(find_live_studio_deserializers(content))

    for obj in object_literals:
        name = list(obj.keys())[0]
        value = obj[name]
        add_references_to_enum(name, value, decoder_literals)

        if name in object_map:

            # If collision, check if the values are the same. If they are not, print a warning and skip
            if object_map[name] != value:
                print(f'Collision detected for {name}', object_map[name], 'VS', value)

            continue

        object_map[name] = value

    with open(enum_map, 'w') as f:
        json.dump(object_map, f, indent=4)
