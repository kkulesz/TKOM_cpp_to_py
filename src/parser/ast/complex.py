# complex meaning it can contain other complex. They simply introduce new scope
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import Dictionaries
from src.parser.ast.primitives import *


class FunctionDeclaration(AstNode):
    def __init__(self, type_token, id_token, arguments, instructions):
        """
        TODO: return maybe?
        """
        self.type = Type(type_token)
        self.name = Id(id_token)
        self.arguments = arguments
        self.instructions = instructions

    def __repr__(self):
        return f"FunctionDeclaration: {self.type} {self.name} ({self.arguments})  {self.instructions}"


class IfStatement(AstNode):
    pass


class WhileStatement(AstNode):
    pass
