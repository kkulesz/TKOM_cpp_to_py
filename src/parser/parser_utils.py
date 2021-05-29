from src.lexer.token import TokenType


class ParserUtils:
    type_tokens = \
        [TokenType.INT_KW, TokenType.BOOL_KW, TokenType.STRING_KW]

    literal_tokens = \
        [TokenType.INT_LITERAL, TokenType.STRING_LITERAL, TokenType.TRUE_KW, TokenType.FALSE_KW]

    function_invocation_tokens = \
        literal_tokens + [TokenType.IDENTIFIER]

    multiplicative_operator_tokens = \
        [TokenType.STAR, TokenType.FORWARD_SLASH]

    additive_operator_tokens = \
        [TokenType.PLUS, TokenType.MINUS]

    comparison_tokens = \
        [TokenType.EQUAL,
         TokenType.NOT_EQUAL,
         TokenType.GREATER_EQUAL,
         TokenType.GREATER,
         TokenType.LESS_EQUAL,
         TokenType.LESS]

    boolean_tokens = \
        [TokenType.AND, TokenType.OR]
