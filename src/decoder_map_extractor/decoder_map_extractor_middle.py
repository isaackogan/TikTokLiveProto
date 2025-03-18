import json
from pathlib import Path

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from antlr.generated.Java8Lexer import Java8Lexer
from antlr.generated.Java8Parser import Java8Parser
from modules.utilities import FieldMap
from modules.while_parser import WhileLoopListener


def parse_java_file(file_path: Path) -> FieldMap:
    """
    Extract the field map from a Java file.

    :param file_path: The path to the Java file.
    :return: The field map.

    """

    input_stream: FileStream = FileStream(str(file_path), encoding="utf-8")
    file_lines = file_path.read_text().split("\n")

    # Tokenize input
    lexer = Java8Lexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = Java8Parser(token_stream)
    tree = parser.compilationUnit()
    walker = ParseTreeWalker()
    listener = WhileLoopListener(
        class_name=file_path.stem,
        file_lines=file_lines
    )
    walker.walk(listener, tree)
    return listener.field_map


decoders: Path = Path(__file__).parent.parent.parent / './resources/decoders'
decoder_maps: Path = Path(__file__).parent.parent.parent / './resources/decoder_maps'

decoder_files = [file for file in decoders.iterdir() if file.suffix == '.java']

for idx, file in enumerate((decoder_files[:len(decoder_files) // 2])):
    decoder_map = decoder_maps / f"{file.stem}.json"

    if decoder_map.exists() and 'BattleBonusConfig' not in file.stem:
        # print(f"Skipping {file.stem} as it already exists")
        continue
    else:
        print(f'Parsing Decoder {idx + 1}/{len(decoder_files)}: {file.stem}')

    field_map = parse_java_file(file)
    with open(decoder_map, 'w') as f:
        f.write(json.dumps(field_map, indent=4))
