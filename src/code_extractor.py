"""
code_extractor.py

This file extracts all Protobuf models & decoders from the sources directory of
a decompiled TikTok APK. These can then be used as inputs in the protobuf extractors.

"""

import os
from pathlib import Path

sources: Path = Path(__file__).parent.parent / './resources/sources'
decoders: Path = Path(__file__).parent.parent / './resources/decoders'
models: Path = Path(__file__).parent.parent / './resources/models'

if not sources.is_dir():
    raise FileNotFoundError(f"Sources directory not found at {sources}")

decoder_files = []
model_files = []

# Walk through the directory
for root, dirs, files in os.walk(sources):
    # Check each file in the current directory
    for file in files:
        # Check if the file ends with '_ProtoDecoder.java'
        if file.endswith('_ProtoDecoder.java'):

            # Append the full path of the file to the list
            decoder_files.append(os.path.join(root, file))
            print('Found', file)
            model_name = file[1:-len('_ProtoDecoder.java')]

            # If it has _ it is an _Data or _Extra, etc. Decoder
            # Skip it because these decoders are a class WITHIN a parent model
            # As such they HAVE no 'Model' file, they are within their parent's model file
            if '_' in model_name:
                continue

            model_files.append(os.path.join(root, f'{model_name}.java'))

print(f'Found {len(decoder_files)} decoder files')
print(f'Found {len(model_files)} model files')

for decoder_file in decoder_files:
    decoder_output = decoders / Path(decoder_file).name

    with open(decoder_file, 'r') as f:
        with open(decoder_output, 'w') as out:
            out.write(f.read())

for model_file in model_files:
    # Copy model file
    model_output = models / Path(model_file).name
    with open(model_file, 'r') as f:
        with open(model_output, 'w') as out:
            out.write(f.read())
