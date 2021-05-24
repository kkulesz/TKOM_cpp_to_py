class GenericError(Exception):
    def __init__(self, message):
        self.message = f"{message}!"
        super().__init__(self.message)

    def fatal(self):
        print(self.message)
        exit(-1)

    def warning(self):
        print(self.message)


class LexerError(GenericError):
    def __init__(self, position, message):
        line, col = position
        self.message = f"Lexer error! line:{line} column:{col} -- {message}"
        super().__init__(self.message)


class ParserError(GenericError):
    def __init__(self, position, message):
        line, col = position
        self.message = f"Parser error! line:{line} column:{col} -- {message}"
        super().__init__(self.message)


class ParserSyntaxError(ParserError):
    def __init__(self, position, expected_token, got_token):
        self.message = f"Expected: {expected_token}, but got: {got_token}"
        super(ParserSyntaxError, self).__init__(position, self.message)


class ParserDevelopmentError(ParserError):  # for debug
    def __init__(self, position, message):
        self.message = f"PARSER DEVELOPMENT ERROR: {message}"
        super(ParserDevelopmentError, self).__init__(position, self.message)


class SemanticError(GenericError):
    def __init__(self, message):
        self.message = f"Semantic error! -- {message}"
        super(SemanticError, self).__init__(self.message)


class SemanticVariableRedeclarationError(SemanticError):
    def __init__(self, var_id):
        self.message = f"redeclaration of variable: {var_id}"
        super(SemanticVariableRedeclarationError, self).__init__(self.message)


class SemanticInvalidTypeError(SemanticError):
    def __init__(self, expected_type, gotten_type):
        self.message = f"invalid type, expected: {expected_type}, but got {gotten_type}"
        super(SemanticInvalidTypeError, self).__init__(self.message)


class SemanticUnknownSymbolError(SemanticError):
    def __init__(self, gotten_id):
        self.message = f"unknown symbol: {gotten_id}"
        super(SemanticUnknownSymbolError, self).__init__(self.message)


class SemanticNotNumberInArithmeticExprError(SemanticError):
    def __init__(self, gotten_type):
        self.message = f"arithmetic expressions are designed for integers only, not for: {gotten_type}s"
        super(SemanticNotNumberInArithmeticExprError, self).__init__(self.message)


class SemanticReturnNotInsideFunctionBodyError(SemanticError):
    def __init__(self):
        self.message = f"return statement not inside function body"
        super(SemanticReturnNotInsideFunctionBodyError, self).__init__(self.message)


class SemanticAnalyzerDevelopmentError(SemanticError):
    def __init__(self, message):
        self.message = f"SEMANTIC ANALYZER DEVELOPMENT ERROR: {message}"
        super(SemanticAnalyzerDevelopmentError, self).__init__(self.message)
