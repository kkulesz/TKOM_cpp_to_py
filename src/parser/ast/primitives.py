# primitives - leaves of AST, they do not contain other nodes
from src.parser.ast.ast_node import AstNode
from src.parser.ast.ast_utils import *
from src.lexer.token import TokenType, Token
from src.errors import ParserDevelopmentError


# TODO: GET RID OF DEVELOPMENT ERRORS WHEN


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
        return Dictionaries.primitive_to_string[self.type]


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


class Id(AstNode):
    def __init__(self, id_token):
        if TokenType.IDENTIFIER != id_token.get_type():
            ParserDevelopmentError(id_token.get_position(), "bad token in arithmetic operation!").fatal()
        self.name = id_token.get_value()

    def __repr__(self):
        return f"(id={self.name})"


class Type(AstNode):
    def __init__(self, type_token):
        if type_token.get_type() not in Dictionaries.token_to_types:
            ParserDevelopmentError(type_token.get_position(), "not a type token!").fatal()
        self.type = Dictionaries.token_to_types[type_token.get_type()]

    def __repr__(self):
        return Dictionaries.primitive_to_string[self.type]
