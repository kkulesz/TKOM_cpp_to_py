# primitives - leaves of AST, they cannot contain other nodes
from src.parser.ast.ast_node import AstNode
from src.parser.ast.utils import Types, ArithmeticOperatorTypes, BooleanOperatorTypes, LogicalOperatorTypes
from src.lexer.token import TokenType
from src.errors import ParserDevelopmentError


class Literal(AstNode):
    def __init__(self, literal_token, value=None):
        self.type, self.value = Literal.init_literal(literal_token, value)

    @staticmethod
    def init_literal(literal_token, value):
        literal_type = literal_token.get_type()
        if literal_type == TokenType.INT_LITERAL and isinstance(value, int):
            return Types.INT, value
        elif literal_type == TokenType.STRING_LITERAL and isinstance(value, str):
            return Types.STRING
        elif literal_type == TokenType.TRUE_KW or literal_type == TokenType.FALSE_KW:
            return Types.BOOLEAN, literal_type == TokenType.TRUE_KW
        else:
            ParserDevelopmentError(literal_token.get_position(), "bad token in literal!")
            # TODO: change it later to non development error


class ArithmeticOperator(AstNode):
    def __init__(self, token_operator):
        self.type = ArithmeticOperator.get_type_from_token(token_operator)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in ArithmeticOperatorTypes.dictionary:
            return ArithmeticOperatorTypes.dictionary[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in arithmetic operation!")


class BooleanOperator(AstNode):
    def __init__(self, token):
        self.type = BooleanOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in BooleanOperatorTypes.dictionary:
            return BooleanOperatorTypes.dictionary[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in boolean operation!")


class LogicalOperator(AstNode):
    def __init__(self, token):
        self.type = LogicalOperator.get_type_from_token(token)

    @staticmethod
    def get_type_from_token(token_operator):
        token_type = token_operator.get_type()
        if token_type in LogicalOperatorTypes.dictionary:
            return LogicalOperatorTypes[token_type]
        else:
            ParserDevelopmentError(token_operator.get_position(), "bad token in logical operation!")