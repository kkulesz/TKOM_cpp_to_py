from enum import Enum, auto, unique
from src.lexer.token import TokenType




@unique
class Types(Enum):
    INT = auto()
    STRING = auto()
    BOOLEAN = auto()


class Dictionaries:
    token_to_ast_types_dict = {
        TokenType.INT_KW: Types.INT,
        TokenType.STRING_KW: Types.STRING,
        TokenType.BOOL_KW: Types.BOOLEAN
    }

    default_values = {
        Types.INT: 0,
        Types.STRING: '',
        Types.BOOLEAN: False
    }


@unique
class ArithmeticOperatorTypes(Enum):
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    dictionary = {
        TokenType.PLUS: PLUS,
        TokenType.MINUS: MINUS,
        TokenType.STAR: MULTIPLY,
        TokenType.FORWARD_SLASH: DIVIDE
    }


@unique
class BooleanOperatorTypes(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    dictionary = {
        TokenType.EQUAL: EQUAL,
        TokenType.NOT_EQUAL: NOT_EQUAL,
        TokenType.GREATER: GREATER,
        TokenType.GREATER_EQUAL: GREATER_EQUAL,
        TokenType.LESS: LESS,
        TokenType.LESS_EQUAL: LESS_EQUAL
    }


@unique
class LogicalOperatorTypes(Enum):
    NOT = auto()
    OR = auto()
    AND = auto()

    dictionary = {
        TokenType.NOT: NOT,
        TokenType.OR: OR,
        TokenType.AND: AND
    }
