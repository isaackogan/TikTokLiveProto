from antlr4 import ParseTreeWalker

from antlr.generated.Java8ParserListener import Java8ParserListener
from .if_parser import IfElseListener
from .utilities import FieldMap


class WhileLoopListener(Java8ParserListener):
    def __init__(self, class_name: str, file_lines: list[str]):
        super().__init__()
        self._class_name: str = class_name
        self._field_map: FieldMap = {}
        self._file_lines: list[str] = file_lines
        self._while_depth: int = 0  # Depth counter for while loops

    @property
    def field_map(self):
        return self._field_map

    def enterWhileStatement(self, ctx):
        """Triggered when a while statement is encountered."""
        self._while_depth += 1  # Increment depth as we enter a while statement

        if self._while_depth == 1:  # Process only the outermost while loop
            block_statement = ctx.statement()
            if_else_listener = IfElseListener(
                class_name=self._class_name,
                field_map=self._field_map,
                file_lines=self._file_lines)
            walker = ParseTreeWalker()
            walker.walk(if_else_listener, block_statement)

    def exitWhileStatement(self, ctx):
        """Triggered when exiting a while statement."""
        self._while_depth -= 1  # Decrement depth as we exit a while statement
