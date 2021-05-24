class GenericError(Exception):
    def __init__(self, message):
        self.message = message
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
    def __init__(self):
        pass


class SemanticAnalyzerDevelopmentError(GenericError):
    def __init__(self, message):
        self.message = f"SEMANTIC ANALUZER DEVELOPMENT ERROR: {message}"
        super(SemanticAnalyzerDevelopmentError, self).__init__(self.message)
