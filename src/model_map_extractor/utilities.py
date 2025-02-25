type ModelMapField = {
    "name": str,
    "annotation": str,
    "type": str
}

type ModelMap = {
    "class_name": str,
    "fields": list[ModelMapField],
    "type": str,
    "nested_classes": dict[str, ModelMap]
}
