from antlr4 import ParseTreeWalker

from antlr.generated.Java8Parser import Java8Parser
from antlr.generated.Java8ParserListener import Java8ParserListener
from .switch_parser import SwitchCaseListener
from .utilities import FieldMap, extract_proto_decoder, count_while_parents


class IfElseListener(Java8ParserListener):

    def __init__(self, class_name: str, field_map: FieldMap, file_lines: list[str]):
        super().__init__()
        self._class_name: str = class_name
        self._field_map: FieldMap = field_map
        self._file_lines: list[str] = file_lines

        object_name_raw = class_name.split("_")[-2]
        # CapitalCase
        self._model_name = object_name_raw[0].upper() + object_name_raw[1:]
        self._object_instance: str = object_name_raw[0].lower() + object_name_raw[1:]  # camelCase

    def enterIfThenElseStatement(self, ctx: Java8Parser.IfThenElseStatementContext):

        if count_while_parents(ctx) > 1:
            # This is inside of a SECOND while loop, ignore it, it's a map
            # Since this listener works recursively, we know another parent if statement will capture the context
            return

        condition = ctx.expression()
        comparison_text = condition.getText()

        assert condition.getChildCount() == 1, "The condition should have only 1 child."
        assert "!=" in comparison_text, "The condition should have a != operator."

        operand = comparison_text.split("!=")[1]
        try:
            field_number: int = int(operand)
        except ValueError:

            # If null, it's because it's for a map. Ignore, a more parent if statement will handle this
            if operand == "null":
                return

            raise ValueError(f"Could not extract field number from {comparison_text}")

        # Ignore field number -1 as it is the null case
        if field_number == -1:

            # If we have a switch statement at -1, this is a switch-parsed class
            field_text = ctx.statementNoShortIf().getText()
            if 'switch' in field_text:
                walker = ParseTreeWalker()
                walker.walk(SwitchCaseListener(
                    field_map=self._field_map, file_lines=self._file_lines,
                    class_name=self._class_name
                ), ctx)

            # Never handle -1 field numbers
            return

        # The block can be 1 of 2 cases
        # either it is (A) an assignment expression, such as followInfo.followStatus=c140922mme.LJIIJJI()
        # or (B) a switch case

        # Check if the block contains an assignment expression
        block = ctx.statement()

        # (A) Check if the block contains an assignment expression
        assert block.getChildCount() == 1, "The block should have only 1 child."
        statement_text = block.getText()

        # e.g. {followInfo.followingCount=c140922mme.LJIIJJI();}
        try:
            assert (
                    statement_text.count(";") == 1
                    # Special case: A nested definition (e.g. ExampleMessage.Data = new ExampleMessage.Data())
                    or f"new{self._model_name}." in statement_text
            ), f"The block should have only 1 line, got {statement_text}"

            try:
                field_name_raw = statement_text.split(self._object_instance + ".")[1]
            except IndexError:
                raise IndexError(f"Got an unexpected statement text (Instance is {self._object_instance}): " + statement_text)

            # Try to split by =, if not, split by .
            if '=' in field_name_raw:
                field_name = field_name_raw.split("=")[0]
            else:
                field_name = field_name_raw.split(".")[0]

        except AssertionError:
            # Special case: Map
            if '.put(' in statement_text:
                field_name = statement_text.split('.put(')[0].split(".")[-1]
            else:
                raise AssertionError(f"Unexpected block text: {statement_text}")

        print(f"Assigned {field_name} to field number {field_number}")
        self._field_map[field_name] = {
            "field": field_number,
            "proto_decoder": extract_proto_decoder(statement_text),
            "field_enum": None
        }
