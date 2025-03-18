import json
from pathlib import Path

enum_map: Path = Path(__file__).parent.parent.parent.parent / './resources/enum_maps/enum_map.json'
enum_map_data: dict = json.load(open(enum_map, 'r'))

alias_map: dict = {
    "Common": "CommonMessageData",
    "Emote": "EmoteModel",
    "BattleTeamResult": "TeamBattleResult"
}


def recursively_resolve_path(path: list[str], root_messages: list[dict]) -> dict | None:
    """
    Recursively resolves the path to the root message

    """

    for root_message in root_messages:
        if path[0] in alias_map:
            path[0] = alias_map[path[0]]

        if root_message['name'] == path[0]:
            if len(path) == 1:
                return root_message
            else:
                return recursively_resolve_path(path[1:], [*root_message['nested_messages'], *root_messages])

    return None


def clean_enum_values(enum: dict):
    # Top level enum name
    top_level_enum_name = enum['identifier'].split(".")[-1]

    # create an upper case snake case of it
    top_level_enum_name = ''.join(['_' + c.upper() if c.isupper() else c for c in top_level_enum_name]).lstrip('_').upper()

    for key, value in enum['data'].copy().items():
        # if the name doesn't start with the top level enum name, add it to the front

        if not key.startswith(top_level_enum_name):
            new_key = f"{top_level_enum_name}_{key}"
            enum['data'][new_key] = value
            del enum['data'][key]


def resolve_enum_types(root_messages: list[dict]) -> list[dict]:
    """"
    Resolves enum types & returns a list of root enums

    """

    unresolved_enums = []
    resolved_enums = []

    for enum in enum_map_data.values():

        # Clean the enum values
        clean_enum_values(enum)

        for reference, referenced_fields in enum['references'].items():
            reference_path: list[str] = reference.split('.')
            root_message: dict = recursively_resolve_path(reference_path, root_messages)

            if root_message is None:
                print(f"Could not resolve reference {reference} for {enum['identifier']}")
                identifier = enum['identifier']

                if identifier in [e['identifier'] for e in unresolved_enums]:
                    duplicates = [e for e in unresolved_enums if e['identifier'] == identifier]
                    all_duplicates_equal = all(d['data'] == duplicates[0]['data'] for d in [*duplicates, enum])

                    if not all_duplicates_equal:
                        print(f"Duplicate enums with identifier {identifier} have different data")

                    continue

                if "." in identifier:
                    print("Skipping nested enum in unresolved enum list", identifier)
                    continue

                unresolved_enums.append(
                    {
                        'identifier': enum['identifier'],
                        'data': enum['data'],
                        'root_message': None,
                    }
                )
            else:

                if 'enums' not in root_message:
                    root_message['enums'] = []

                enum_data = {
                    'identifier': enum['identifier'].split(".")[-1],
                    'data': enum['data'],
                    'num_references': len(enum['references']),
                }

                root_message['enums'].append(enum_data)
                resolved_enums.append(enum_data)

                for field_number in referenced_fields:
                    for field in root_message['fields']:
                        if field['position'] == field_number:
                            field['type'] = enum_data['identifier']

    # Pick only the resolved enum with the most references
    top_level_enums = []

    for enum in [*resolved_enums, *unresolved_enums]:
        if enum['identifier'] in [e['identifier'] for e in top_level_enums]:
            duplicates = [e for e in top_level_enums if e['identifier'] == enum['identifier']]
            all_duplicates_equal = all(d['data'] == duplicates[0]['data'] for d in [*duplicates, enum])

            if not all_duplicates_equal:
                print(f"Duplicate enums with identifier {enum['identifier']} have different data")

            continue

        top_level_enums.append(enum)

    return top_level_enums
