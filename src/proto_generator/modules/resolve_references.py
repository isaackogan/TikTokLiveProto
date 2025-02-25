import json
import logging
from pathlib import Path
from model_map_extractor.utilities import ModelMap
from proto_generator.modules.decoder_resolver import resolve_decoder
from proto_generator.modules.type_resolver import BASIC_TYPE_MAP

type MessageField = {
    "type": str,
    "name": str,
    "annotation": str | None,
    "position": int,
    "message": dict | None,
}

type MessageStruct = {
    "name": str,
    "fields": list[MessageField],
    "nested_messages": list[MessageStruct],
}

def resolve_references(model_map: ModelMap, decoder_map_dir: Path, parent_message_type: str = None) -> MessageStruct:
    """
    Resolves references recursively for a given model map, handling lists and maps.
    """
    base_struct = {
        "name": model_map.get('event_name', model_map['class_name']),
        "fields": [],
        "nested_messages": [],
    }

    decoder_map = resolve_decoder(
        message_type=model_map['class_name'],
        parent_message_type=parent_message_type,
        decoder_map_dir=decoder_map_dir,
    )

    for field in model_map['fields']:
        if field['name'] not in decoder_map:
            logging.debug(f"Field {field['name']} not found in decoder map")
            continue

        resolved_field = resolve_field(field, model_map, decoder_map_dir, decoder_map, parent_message_type)
        if resolved_field:
            base_struct['fields'].append(resolved_field)
            if resolved_field['type'] == "message" and resolved_field['message']:
                base_struct['nested_messages'].append(resolved_field['message'])

    return base_struct

def resolve_map_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type):
    """
    Resolves a map field type recursively (e.g., Map<K, V>).
    """
    inner_types = field['type'][4:-1].split(",")  # Extract K, V from Map<K, V>
    if len(inner_types) != 2:
        logging.warning(f"Invalid map type format: {field['type']}")
        return None

    key_type, value_type = inner_types
    key_type = key_type.strip()
    value_type = value_type.strip()

    resolved_key = resolve_field(
        {"type": key_type, "name": field['name'], "annotation": None},
        model_map, decoder_map_dir, decoder_map, parent_message_type
    )

    resolved_value = resolve_field(
        {"type": value_type, "name": field['name'], "annotation": field.get('annotation', None)},
        model_map, decoder_map_dir, decoder_map, parent_message_type
    )

    if resolved_key and resolved_value:
        return {
            "type": f"map<{resolved_key['type']}, {resolved_value['type']}>",
            "name": field['name'],
            "message": None,  # Map itself is not a message, but its values might be
            "annotation": field.get('annotation', None),
            "position": decoder_map[field['name']]['field'],
        }
    return None


def resolve_field(field, model_map, decoder_map_dir, decoder_map, parent_message_type):
    """
    Resolves a single field, determining if it is a basic, nested, list, or external type.
    """
    field_type = field['type']
    field_position = decoder_map[field['name']]['field']
    annotation = field.get('annotation', None)

    if field_type in BASIC_TYPE_MAP:
        return {
            "type": BASIC_TYPE_MAP[field_type],
            "name": field['name'],
            "message": None,
            "annotation": annotation,
            "position": field_position,
        }

    if field_type in model_map['nested_classes']:
        nested_struct = resolve_references(
            model_map=model_map['nested_classes'][field_type],
            decoder_map_dir=decoder_map_dir,
            parent_message_type=(parent_message_type or "") + f"_{model_map['class_name']}",
        )
        return {
            "type": "message",
            "name": field['name'],
            "message": nested_struct,
            "annotation": annotation,
            "position": field_position,
        }

    if field_type.startswith("List<"):
        return resolve_list_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type)

    if field_type.startswith("Map<"):
        return resolve_map_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type)

    return resolve_external_type(field, decoder_map_dir, field_position, annotation)


def resolve_list_type(field, model_map, decoder_map_dir, decoder_map, parent_message_type):
    """
    Resolves a list field type recursively (e.g., List<List<type>>).
    """
    inner_type = field['type'][5:-1]  # Extract inner type from List<inner_type>
    resolved_inner = resolve_field(
        {"type": inner_type, "name": field['name'], "annotation": field.get('annotation', None)},
        model_map, decoder_map_dir, decoder_map, parent_message_type
    )

    if resolved_inner:
        return {
            "type": f"repeated {resolved_inner['type']}",
            "name": field['name'],
            "message": resolved_inner["message"],
            "annotation": resolved_inner["annotation"],
            "position": resolved_inner["position"],
        }
    return None


def resolve_external_type(field, decoder_map_dir, field_position, annotation):
    """
    Attempts to resolve an external type (not in BASIC_TYPE_MAP or nested_classes) by checking decoder maps.
    """
    try:
        decoder_map = resolve_decoder(
            message_type=field['type'],
            parent_message_type=None,
            decoder_map_dir=decoder_map_dir,
        )
        logging.info(f'Found external decoder for field: {field["name"]}')
        return {
            "type": field['type'],
            "name": field['name'],
            "message": None,
            "annotation": annotation,
            "position": field_position,
        }
    except FileNotFoundError:
        logging.warning(f"External type not found: {json.dumps(field, indent=4)}")
        return None


if __name__ == '__main__':
    user_model_map = Path(__file__).parent.parent.parent.parent / './resources/model_maps/Gift.json'
    user_model_map = json.loads(user_model_map.read_text())
    _decoder_map_dir = Path(__file__).parent.parent.parent.parent / './resources/decoder_maps'

    if not _decoder_map_dir.is_dir():
        raise FileNotFoundError(f"Decoder maps directory not found at {_decoder_map_dir}")

    resolve_references(user_model_map, _decoder_map_dir)
