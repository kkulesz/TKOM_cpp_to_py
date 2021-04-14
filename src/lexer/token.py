from enum import Enum, auto, unique


@unique
class TokenType(Enum):
    #
    EOF = auto()
    ID = auto()
    SEMICOLON = auto()
    SINGLE_LINE_COMMENT = auto()
    MULTI_LINE_COMMENT = auto()
    PRINT_START = auto()
    PRINT_NEW_LINE = auto()

    # brackets
    OP_SQUARE_BRACKET = auto()
    CL_SQUARE_BRACKET = auto()
    OP_BRACKET = auto()
    CL_BRACKET = auto()
    OP_CURLY_BRACKET = auto()
    CL_CURLY_BRACKET = auto()

    # arithmetic operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FOR_SLASH = auto()

    # logical operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # bool operators
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    ASSIGN = auto

    DOT = auto()
    COMA = auto()

    RETURN = auto()

    # literals
    INT_LITERAL = auto
    STRING_LITERAL = auto
    BOOL_LITERAL = auto
    FLOAT_LITERAL = auto

    # types ids
    INT_TYPE = auto
    STRING_TYPE = auto
    BOOL_TYPE = auto
    FLOAT_TYPE = auto


class Token:
    def __init__(self, token_type: TokenType, line: int, column: int, value=None):
        self.type = token_type
        self.line = line
        self.column = column
        self.value = value

    def get_position(self):
        return self.line, self.column

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    # for debug
    def __repr__(self):
        # INT(6): 1,15
        return f'{self.type.name}({self.value}): pos({self.line}, {self.column})'
