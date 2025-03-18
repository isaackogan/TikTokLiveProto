import copy
import json
import logging
from pathlib import Path

from model_map_extractor.utilities import ModelMap
from .decoder_resolver import resolve_decoder, resolve_decoder_from_file_name
from .type_resolver import BASIC_TYPE_MAP

ENUM_LIST = json.load(
    open(Path(__file__).parent.parent.parent.parent / './resources/enum_maps/enum_list.json')
)

type MessageField = {
    "type": str,
    "name": str,
    "annotation": str | None,
    "position": int,
}

type MessageStruct = {
    "name": str,
    "fields": list[MessageField],
    "nested_messages": list[MessageStruct],
}


def resolve_references(
        model_map: ModelMap,
        decoder_map_dir: Path,
        parent_message_type: str = None,
        decoder_file_name=None,
) -> MessageStruct:
    base_struct = {
        "name": model_map['class_name'],
        "alias": model_map.get('event_name'),
        "fields": [],
        "nested_messages": [],
    }

    if decoder_file_name:
        decoder_map, decoder_map_path = resolve_decoder_from_file_name(
            file_name=decoder_file_name,
            decoder_map_dir=decoder_map_dir,
        )
    else:
        decoder_map, decoder_map_path = resolve_decoder(
            message_type=model_map['class_name'],
            parent_message_type=parent_message_type,
            decoder_map_dir=decoder_map_dir,
        )

    for field in model_map['fields']:
        if field['name'] not in decoder_map:
            # replace the decoder_map_path file extension with .java
            if decoder_map_path is not None:
                decoder_map_path_str = str(decoder_map_path.with_suffix('.java').absolute()).replace("decoder_maps", "decoders")
                file_data = open(decoder_map_path_str, 'r').read()

                # Remove everything before the class declaration
                file_data = file_data[file_data.find("public class"):]

                if field['name'] in file_data:

                    if f"{field['name']} = new ArrayList();" in file_data:
                        logging.info('ArrayList with no decoder. Skipping, this is filled dynamically')
                        continue

                    logging.error(f"Field named \"{field['name']}\" NOT in decoder-map for {model_map['class_name']}, TikTok sucks")
                    continue

            logging.debug(f"Field {field['name']} not found in decoder map for {model_map['class_name']}")
            continue

        resolved_field, nested_messages = resolve_field(
            field,
            model_map,
            decoder_map_dir,
            copy.deepcopy(decoder_map),
            parent_message_type=parent_message_type,
        )

        for new_nested_message in nested_messages:
            base_struct['nested_messages'].append(new_nested_message)

        if resolved_field and resolved_field not in base_struct['fields']:
            base_struct['fields'].append(resolved_field)

    # Sort fields by position
    base_struct['fields'] = sorted(base_struct['fields'], key=lambda x: x['position'])

    return base_struct


def get_enum_type(field_name: str) -> str | None:
    field_name = field_name[0].capitalize() + field_name[1:]

    if field_name in ENUM_LIST:
        return ENUM_LIST[ENUM_LIST.index(field_name)]

    return None


def resolve_field(field, model_map, decoder_map_dir, decoder_map, parent_message_type) -> tuple[MessageField, list[MessageStruct]]:
    field_type = field['type']
    field_position = decoder_map[field['name']]['field']
    annotation = field.get('annotation', None)

    # Enum type
    enum_type = get_enum_type(field['name'])
    if enum_type:
        return {
            "type": enum_type,
            "name": field['name'],
            "annotation": annotation,
            "position": field_position,
        }, []

    # Basic type
    if field_type in BASIC_TYPE_MAP:
        return {
            "type": BASIC_TYPE_MAP[field_type],
            "name": field['name'],
            "annotation": annotation,
            "position": field_position,
        }, []

    # Nested class
    if field_type in model_map['nested_classes']:

        decoder_file_name = decoder_map[field['name']]['proto_decoder']
        if decoder_file_name:
            decoder_file_name = decoder_file_name.replace(".java", ".json")

        nested_struct = resolve_references(
            model_map={
                **model_map['nested_classes'][field_type],
                "nested_classes": {
                    **model_map['nested_classes'][field_type]['nested_classes'],
                    **model_map['nested_classes'],
                },
            },
            decoder_map_dir=decoder_map_dir,
            parent_message_type=(parent_message_type or "") + f"_{model_map['class_name']}",
            decoder_file_name=decoder_file_name,
        )

        return {
            "type": nested_struct["name"],  # Reference the message name
            "name": field['name'],
            "annotation": annotation,
            "position": field_position,
        }, [nested_struct]

    if field_type.startswith("ArrayList<"):
        field_type = field_type.replace("ArrayList<", "List<")
        field['type'] = field_type

    if field_type.startswith("ArrayMap<"):
        field_type = field_type.replace("ArrayMap<", "Map<")
        field['type'] = field_type

    if field_type.startswith("HashMap<"):
        field_type = field_type.replace("HashMap<", "Map<")
        field['type'] = field_type

    if field_type.startswith("List<"):
        return resolve_list_type(
            field,
            model_map,
            decoder_map_dir,
            decoder_map,
            parent_message_type
        )

    if field_type.startswith("Map<"):
        return resolve_map_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type)

    # External class
    return resolve_external_type(
        field,
        decoder_map_dir,
        field_position,
        annotation,
        parent_message_type
    )


def resolve_list_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type):
    inner_type = field['type'][5:-1]
    resolved_inner, nested_messages = resolve_field(
        {"type": inner_type, "name": field['name'], "annotation": field.get('annotation', None)},
        model_map, decoder_map_dir, decoder_map, parent_message_type,
    )

    if resolved_inner:
        return {
            "type": f"repeated {resolved_inner['type']}",
            "name": field['name'],
            "annotation": resolved_inner["annotation"],
            "position": resolved_inner["position"],
        }, nested_messages
    return None


def resolve_map_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type):
    inner_types = field['type'][4:-1].split(",")
    if len(inner_types) != 2:
        logging.warning(f"Invalid map type format: {field['type']}")
        return None

    key_type, value_type = map(str.strip, inner_types)
    resolved_key, nested_messages_key = resolve_field(
        {"type": key_type, "name": field['name'], "annotation": None},
        model_map, decoder_map_dir, decoder_map, parent_message_type
    )

    resolved_value, nested_messages_value = resolve_field(
        {"type": value_type, "name": field['name'], "annotation": field.get('annotation', None)},
        model_map, decoder_map_dir, decoder_map, parent_message_type,
    )

    if resolved_key and resolved_value:
        return {
            "type": f"map<{resolved_key['type']}, {resolved_value['type']}>",
            "name": field['name'],
            "annotation": field.get('annotation', None),
            "position": decoder_map[field['name']]['field'],
        }, nested_messages_key + nested_messages_value
    return None


def resolve_external_type(field, decoder_map_dir, field_position, annotation, parent_message_type=None):
    # First try to resolve the decoder as a standalone separate field

    field_to_return = {
        "type": field['type'],
        "name": field['name'],
        "annotation": annotation,
        "position": field_position,
    }

    try:
        resolve_decoder(
            message_type=field['type'],
            parent_message_type=None,
            decoder_map_dir=decoder_map_dir,
        )
        logging.info(f'Found external decoder for field: {field["name"]}')
        return field_to_return, []
    except FileNotFoundError:
        pass

    # If that fails, try it as a subfield of the parent message
    try:
        resolve_decoder(
            message_type=field['type'],
            parent_message_type=parent_message_type,
            decoder_map_dir=decoder_map_dir,
        )
        logging.error(f'Found external decoder for field: {field["name"]}')
        return field_to_return, []
    except FileNotFoundError:
        logging.warning(f"External type not found for child of {parent_message_type}: {json.dumps(field, indent=4)}")
        return None



