from enum import Enum, auto, unique
from src.lexer.token import TokenType


@unique
class Types(Enum):
    INT = auto()
    STRING = auto()
    BOOLEAN = auto()


@unique
class ArithmeticOperatorTypes(Enum):
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()


@unique
class BooleanOperatorTypes(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()


@unique
class LogicalOperatorTypes(Enum):
    NOT = auto()
    OR = auto()
    AND = auto()


class Dictionaries:
    default_values = {
        Types.INT: 0,
        Types.STRING: '',
        Types.BOOLEAN: False
    }

    token_to_types = {
        TokenType.INT_KW: Types.INT,
        TokenType.STRING_KW: Types.STRING,
        TokenType.BOOL_KW: Types.BOOLEAN
    }

    token_to_arithmetic_operator = {
        TokenType.PLUS: ArithmeticOperatorTypes.PLUS,
        TokenType.MINUS: ArithmeticOperatorTypes.MINUS,
        TokenType.STAR: ArithmeticOperatorTypes.MULTIPLY,
        TokenType.FORWARD_SLASH: ArithmeticOperatorTypes.DIVIDE
    }

    token_to_boolean_operator = {
        TokenType.EQUAL: BooleanOperatorTypes.EQUAL,
        TokenType.NOT_EQUAL: BooleanOperatorTypes.NOT_EQUAL,
        TokenType.GREATER: BooleanOperatorTypes.GREATER,
        TokenType.GREATER_EQUAL: BooleanOperatorTypes.GREATER_EQUAL,
        TokenType.LESS: BooleanOperatorTypes.LESS,
        TokenType.LESS_EQUAL: BooleanOperatorTypes.LESS_EQUAL
    }

    token_to_logical_operator = {
        TokenType.NOT: LogicalOperatorTypes.NOT,
        TokenType.OR: LogicalOperatorTypes.OR,
        TokenType.AND: LogicalOperatorTypes.AND
    }

    operator_to_string = {
        ArithmeticOperatorTypes.PLUS: '+',
        ArithmeticOperatorTypes.MINUS: '-',
        ArithmeticOperatorTypes.DIVIDE: '/',
        ArithmeticOperatorTypes.MULTIPLY: '*',

        BooleanOperatorTypes.EQUAL: '==',
        BooleanOperatorTypes.NOT_EQUAL: '!=',
        BooleanOperatorTypes.GREATER: '>',
        BooleanOperatorTypes.GREATER_EQUAL: '>=',
        BooleanOperatorTypes.LESS: '<',
        BooleanOperatorTypes.LESS_EQUAL: '<=',

        LogicalOperatorTypes.NOT: 'not',
        LogicalOperatorTypes.OR: 'or',
        LogicalOperatorTypes.AND: 'and'
    }
