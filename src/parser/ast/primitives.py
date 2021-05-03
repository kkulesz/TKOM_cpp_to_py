# primitives - leaves of AST, they do not contain other nodes
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *
from src.lexer.token import TokenType
from src.errors import ParserDevelopmentError


# TODO: GET RID OF DEVELOPMENT ERRORS WHEN

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
            return Types.INT, value
        elif literal_type == TokenType.STRING_LITERAL and isinstance(value, str):
            return Types.STRING, value
        elif literal_type == TokenType.TRUE_KW or literal_type == TokenType.FALSE_KW:
            return Types.BOOLEAN, literal_type == TokenType.TRUE_KW
        else:
            ParserDevelopmentError(literal_token.get_position(), "bad token in literal!").fatal()


class ArithmeticOperator(AstNode):
    def __init__(self, token_operator):
        self.type = ArithmeticOperator.get_type_from_token(token_operator)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_arithmetic_operator:
            return Dictionaries.token_to_arithmetic_operator[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in arithmetic operation!").fatal()

    def __repr__(self):
        return Dictionaries.operator_to_string[self.type]


class BooleanOperator(AstNode):
    def __init__(self, token):
        self.type = BooleanOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_boolean_operator:
            return Dictionaries.token_to_boolean_operator[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in boolean operation!").fatal()


class LogicalOperator(AstNode):
    def __init__(self, token):
        self.type = LogicalOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in Dictionaries.token_to_logical_operator:
            return Dictionaries.token_to_logical_operator[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in logical operation!").fatal()


class Variable(AstNode):
    def __init__(self, id_token):
        if TokenType.IDENTIFIER != id_token.get_type():
            ParserDevelopmentError(id_token.get_position(), "bad token in arithmetic operation!").fatal()
        self.name = id_token.get_value()

    def __repr__(self):
        return f"(Variable={self.name})"
