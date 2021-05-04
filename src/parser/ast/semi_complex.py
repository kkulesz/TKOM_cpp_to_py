# semi_complex - they consists of primitives and other semi_complex, but do not introduce new scope
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *
from src.parser.ast.primitives import *


class Literal(AstNode):
    def __init__(self, literal_token):
        self.type, self.value = Literal.init_literal(literal_token)

    def __repr__(self):
        return f"(Literal={self.value})"

    @staticmethod
    def init_literal(literal_token):
        literal_type = literal_token.get_type()
        value = literal_token.get_value()
        if literal_type == TokenType.INT_LITERAL and isinstance(value, int):
            return Type(Token(TokenType.INT_KW)), value
        elif literal_type == TokenType.STRING_LITERAL and isinstance(value, str):
            return Type(Token(TokenType.STRING_KW)), value
        elif literal_type == TokenType.TRUE_KW or literal_type == TokenType.FALSE_KW:
            return Type(Token(TokenType.BOOL_KW)), literal_type == TokenType.TRUE_KW
        else:
            ParserDevelopmentError(literal_token.get_position(), "bad token in literal!").fatal()


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
        return f"VariableDeclaration: {self.type} {self.name} = {self.value};"


class VariableAssignment(AstNode):
    def __init__(self, id_token, value):
        self.name = Id(id_token)
        self.value = value

    def __repr__(self):
        return f"VariableAssignment: {self.name} = {self.value};"


class FunctionArgument(AstNode):
    def __init__(self, type_token, id_token):
        self.type = Type(type_token)
        self.name = Id(id_token)

    def __repr__(self):
        return f"FunArg:{self.type}-{self.name}"


class FunctionInvocation(AstNode):
    def __init__(self, id_token, arguments):
        self.name = Id(id_token)
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionInvocation {self.name} {self.arguments}"


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
    def __init__(self, to_print):
        self.to_print = to_print

    def __repr__(self):
        return f"PrintStatement: {self.to_print};"
