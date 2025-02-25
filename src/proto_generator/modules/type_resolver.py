from pathlib import Path

BASIC_TYPE_MAP = {
    "int": "int32",
    "Integer": "int32",
    "long": "int64",
    "Long": "int64",
    "float": "float",
    "Float": "float",
    "double": "double",
    "Double": "double",
    "boolean": "bool",
    "Boolean": "bool",
    "String": "string",
    "byte[]": "bytes",
    "List": "repeated",
    "Map": "map",
}


def complex_type_resolver(
        java_type
):
    """
    Maps a Java type to its corresponding Protocol Buffers type.

    Args:
    java_type (str): A string representing the Java type.

    Returns:
    str: A string representing the corresponding Protocol Buffers type.
    """

    # Mapping dictionary
    type_map = {
        "List": "repeated",  # Typically used as 'repeated T' where T is the item type
        "Map": "map"  # Typically used as 'map<K, V>' where K and V are the key and value types
    }

    # Handle special cases for generic types like List and Map
    if "List<" in java_type:
        item_type = java_type[java_type.find("<") + 1:-1]
        proto_item_type = type_map.get(item_type, None)
        if proto_item_type is None:
            return f"repeated {item_type}"
        return f"repeated {proto_item_type}"

    if "Map<" in java_type:
        kv_types = java_type[java_type.find("<") + 1:-1].split(", ")
        key_type = type_map.get(kv_types[0], "Unknown")
        value_type = type_map.get(kv_types[1], "Unknown")
        return f"map<{key_type}, {value_type}>"

    # Return the protobuf type or 'Unknown' if not found
    return type_map[java_type]
