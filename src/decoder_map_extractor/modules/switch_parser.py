import logging

from antlr.generated.Java8Parser import Java8Parser
from antlr.generated.Java8ParserListener import Java8ParserListener
from .utilities import extract_proto_decoder, FieldMap


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


class SwitchCaseListener(Java8ParserListener):

    def __init__(self, field_map: FieldMap, file_lines: list[str], class_name: str):
        super().__init__()
        self._field_map: FieldMap = field_map
        self._file_lines: list[str] = file_lines
        self._class_name = class_name

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
                field_name_partial = block_statements_text.split(".")[1]
            except IndexError:
                logging.error(
                    f"Could not find field name for {case_label_expression_text} in class {self._class_name}, got {block_statements_text}"
                )
                continue

            if '=' in field_name_partial:
                field_name = field_name_partial.split("=")[0]
            else:
                field_name = field_name_partial

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
