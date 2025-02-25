import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

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
template = environment.get_template("proto_template.jinja2")

context = {
    "imports": [],
    "root_messages": [
        {
            "name": "Person",
            "fields": [
                {"type": "string", "name": "name"},
                {"type": "int32", "name": "age", "annotation": "Test"},
                {
                    "type": "message",
                    "name": "address",
                    "message": {
                        "name": "Address",
                        "fields": [
                            {"type": "string", "name": "street"},
                            {"type": "string", "name": "city"}
                        ]
                    }
                }
            ]
        }
    ]
}

output = template.render(context)

proto_output = Path(__file__).parent.parent.parent / './resources/proto_output'

if not proto_output.is_dir():
    proto_output.mkdir()

with open(proto_output / 'webcast.proto', 'w') as f:
    f.write(output)
