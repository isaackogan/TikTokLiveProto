import json
import os
import re
from pathlib import Path


def find_matching_java_file(directory):
    pattern = re.compile(r'\s*CHAT\("WebcastChatMessage"\s*')  # <-- We know the file will have

    for root, _, files in os.walk(directory.resolve()):
        for idx, file in enumerate(files):

            if idx % 100 == 0:
                print(f'Checking file {idx}/{len(files)}')

            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if pattern.search(content):
                        return Path(f"{file_path}")

    return None  #


# Example usage:
sources: Path = Path(__file__).parent.parent.parent / './resources/sources'
matching_file = find_matching_java_file(sources) if not os.getenv('TESTING') else Path(__file__).parent / 'TestEnum.java'

if not matching_file:
    raise FileNotFoundError('No matching file found')

# Open the file
file_text = matching_file.read_text()

ENUM_VALUE_MAP = {}

for line in file_text.split("\n"):
    if '("Webcast' not in line:
        continue

    enum_entry_name = line.split('("')[0].strip()
    enum_entry_value = line.split('"')[1].strip()

    ENUM_VALUE_MAP[enum_entry_name] = enum_entry_value

enum_map: Path = Path(__file__).parent.parent.parent / './resources/enum_maps/event_map.json'
with open(enum_map, 'w') as f:
    f.write(json.dumps(ENUM_VALUE_MAP, indent=4))
