# semi_complex - they consists of primitives and other semi_complex, but do not introduce new scope
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *


class VariableDeclaration(AstNode):
    def __init__(self, variable_type_token, id_token, value=None):
        self.type = Dictionaries.token_to_types[variable_type_token.get_type()]
        self.name = id_token.get_value()
        if value is None:
            self.value = Dictionaries.default_values[self.type]
        else:
            self.value = value

    def __repr__(self):
        return f"VariableDeclaration: {self.type.name} {self.name} = {self.value}; "


class VariableAssignment(AstNode):
    def __init__(self, name, value):
        self.name = name
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
