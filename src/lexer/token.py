from enum import Enum, auto, unique


@unique
class TokenType(Enum):

    UNDEFINED = auto()

    EOF = auto()
    IDENTIFIER = auto()
    SEMICOLON = auto()
    START_SINGLE_LINE_COMMENT = auto()
    START_MULTI_LINE_COMMENT = auto()
    END_MULTI_LINE_COMMENT = auto()
    NEW_LINE = auto()

    # brackets
    OP_BRACKET = auto()
    CL_BRACKET = auto()
    OP_CURLY_BRACKET = auto()
    CL_CURLY_BRACKET = auto()

    # arithmetic operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FORWARD_SLASH = auto()

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

    ASSIGN = auto()

    NAMESPACE_OPERATOR = auto()  # '::'
    STREAM_OPERATOR = auto()  # '<<'

    # literals
    INT_LITERAL = auto()
    STRING_LITERAL = auto()
    TRUE_LITERAL = auto()
    FALSE_LITERAL = auto()
    # types ids
    INT_TYPE = auto()
    STRING_TYPE = auto()
    BOOL_TYPE = auto()

    # statements keywords
    RETURN_KW = auto()
    FOR_KW = auto()
    WHILE = auto()
    IF_KW = auto()
    ELSE_KW = auto()
    STD_KW = auto()
    COUT_KW = auto()
    ENDL_KW = auto()



class Token:
    def __init__(self, token_type: TokenType, value=None, line: int = 0, column: int = 0):
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
        # INT(6): 1,15 --example
        return f'{self.type.name} \t {self.value} \t pos({self.line}, {self.column})'


class TokenDicts:
    bool_operators = {

    }

    acceptable_keywords = {
        'return': TokenType.RETURN_KW,
        'for': TokenType.FOR_KW,
        'while': TokenType.WHILE,
        'if': TokenType.IF_KW,
        'else': TokenType.ELSE_KW,
        'std': TokenType.STD_KW,
        'cout': TokenType.COUT_KW,
        'endl': TokenType.ENDL_KW,

        'int': TokenType.INT_TYPE,
        'bool': TokenType.BOOL_TYPE,
        'std::string': TokenType.STRING_TYPE
    }

    double_char_tokens = {
        '::': TokenType.NAMESPACE_OPERATOR,
        '<<': TokenType.STREAM_OPERATOR,
        '<=': TokenType.GREATER_EQUAL,
        '>=': TokenType.LESS_EQUAL,
        '==': TokenType.EQUAL,
        '!=': TokenType.NOT_EQUAL,
        '//': TokenType.START_SINGLE_LINE_COMMENT,
        '/*': TokenType.START_MULTI_LINE_COMMENT,
        '*/': TokenType.END_MULTI_LINE_COMMENT,
        '&&': TokenType.AND,
        '||': TokenType.OR,
    }

    single_char_tokens = {
        '=': TokenType.ASSIGN,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.STAR,
        '/': TokenType.FORWARD_SLASH,
        '!': TokenType.NOT,
        '(': TokenType.OP_BRACKET,
        ')': TokenType.CL_BRACKET,
        '{': TokenType.OP_CURLY_BRACKET,
        '}': TokenType.CL_CURLY_BRACKET,
    }
