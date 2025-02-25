import json
from pathlib import Path


def resolve_decoder(
        message_type: str,
        decoder_map_dir: Path,
        parent_message_type: str = None,
) -> dict:
    decoder_map = decoder_map_dir / f"{parent_message_type or ''}_{message_type}_ProtoDecoder.json"

    if not decoder_map.is_file():
        raise FileNotFoundError(f"Decoder map for {message_type} not found at {decoder_map}")

    return json.loads(decoder_map.read_text())
