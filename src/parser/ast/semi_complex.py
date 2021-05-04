# semi_complex - they consists of primitives and other semi_complex, but do not introduce new scope
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *
from src.parser.ast.primitives import  *


class VariableDeclaration(AstNode):
    def __init__(self, type_token, id_token, value=None):
        # self.type = Dictionaries.token_to_types[type_token.get_type()]
        self.type = Type(type_token)
        self.name = Id(id_token)
        if value is None:
            self.value = Dictionaries.default_values[self.type]
        else:
            self.value = value

    def __repr__(self):
        return f"VariableDeclaration: {self.type} {self.name} = {self.value}; "


class VariableAssignment(AstNode):
    def __init__(self, id_token, value):
        self.name = Id(id_token)
        self.value = value


class Condition(AstNode):
    pass


class ArithmeticExpression(AstNode):
    def __init__(self, left_operand, operator, right_operand):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def __repr__(self):
        return f"ArithmeticExpr: ({self.left_operand}{self.operator}{self.right_operand})"


class PrintStatement(AstNode):
    pass
