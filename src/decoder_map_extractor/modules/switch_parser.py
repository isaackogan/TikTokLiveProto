from antlr.generated.Java8Parser import Java8Parser
from antlr.generated.Java8ParserListener import Java8ParserListener

if __name__ == '__main__':
    from decoder_map_extractor.modules.utilities import FieldMap, extract_proto_decoder
else:
    from .utilities import FieldMap, extract_proto_decoder


def extract_original_line(label, file_lines) -> str:
    for file_line in file_lines:
        if label.replace(" ", "") in file_line.replace(" ", ""):
            return file_line
    raise ValueError(f"Could not find line for {label}")


def extract_field_number_from_comment(label, file_lines) -> int:
    original_line = extract_original_line(label, file_lines)
    return int(original_line.split("/*")[1].split("*/")[0].strip())


MANUAL_MAPPINGS = {
    # Dynamic from a class final value, can't be inferred by jadx
    # Technically we could infer from 48, ____, 50, but it's not worth risking it
    "C53831LAl.LJIIJ": 49  # <-- Changes between app versions
}


def extract_model_name(class_name: str) -> str:
    """
    >>> extract_model_name("_GalleryData_TitleData_ProtoDecoder")
    'TitleData'

    >>> extract_model_name("_GalleryData_ProtoDecoder")
    'GalleryData'

    """

    return class_name.split("_")[-2]


def extract_field_name(model_name: str, switch_statement_text: str) -> str:
    """
    Given a model name, extract the field name from the switch statement text.

    >>> extract_field_name("BattleBonusConfig", "battleBonusConfig.previewStartTime = c140922mme.LJIIJJI();")
    'previewStartTime'

    >>> extract_field_name("BattleBonusConfig", "battleBonusConfig.extra.put(48, c140922mme.LJIIJJI());")
    'extra'

    >>> extract_field_name("BattleBonusConfig", "battleBonusConfig.previewPeriodConfig.add(_PreviewPeriod_ProtoDecoder.LIZIZ(c140922mme));")
    'previewPeriodConfig'

    """

    model_name_instance: str = model_name[0].lower() + model_name[1:]

    statement_start = switch_statement_text[switch_statement_text.index(model_name_instance) + len(model_name_instance) + 1:]

    # End at the first index of a non-alphanumeric character that isn't an underscore
    for idx, char in enumerate(statement_start):
        if not char.isalnum() and char != "_":
            return statement_start[:idx]

    raise ValueError(f"Could not extract field name from {switch_statement_text}")


class SwitchCaseListener(Java8ParserListener):

    def __init__(self, field_map: FieldMap, file_lines: list[str], class_name: str):
        super().__init__()
        self._field_map: FieldMap = field_map
        self._file_lines: list[str] = file_lines
        self._class_name = class_name
        self._model_name = extract_model_name(class_name)

    def enterSwitchStatement(self, ctx: Java8Parser.SwitchStatementContext):

        # Iterate through switch blocks (cases)
        switch_block = ctx.switchBlock()
        for rule in switch_block.switchBlockStatementGroup():

            # Extract case number
            case_label = rule.switchLabels().switchLabel(0)
            case_label_text = case_label.getText()

            # Skip null condition
            if 'default' in case_label_text:
                continue

            assert case_label_text.startswith("case"), "Expected a case label."
            case_label_expression_text = case_label.constantExpression().getText()

            # Extract statement in the case
            block_statements = rule.blockStatements()
            assert block_statements, "The case block should have statements."

            block_statements_text = block_statements.getText()

            try:
                field_name = extract_field_name(self._model_name, block_statements_text)
            except ValueError:

                if self._model_name not in block_statements_text:
                    print('Skipping empty block')
                    continue

                print("Failed with", block_statements_text, "in", self._class_name, "named", self._model_name)
                raise

                # Try to convert the case label to an integer
            try:
                case_number = int(case_label_expression_text)
                field_enum = None
            except ValueError:
                # Find the line number of the case label
                try:
                    case_number = extract_field_number_from_comment(case_label_expression_text, self._file_lines)
                except IndexError:

                    # Check for manual mappings
                    if case_label_expression_text in MANUAL_MAPPINGS:
                        case_number = MANUAL_MAPPINGS[case_label_expression_text]
                    else:
                        raise IndexError(f"Could not find field number for {case_label_expression_text} in class {self._class_name}")
                field_enum = case_label_expression_text

            print(f"Assigned {field_name} to field number {case_number} with decoder {extract_proto_decoder(block_statements_text)}")
            self._field_map[field_name] = {
                "field": case_number,
                "proto_decoder": extract_proto_decoder(block_statements_text),
                "field_enum": field_enum
            }
