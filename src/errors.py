class GenericError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def fatal(self):
        print(self.message)
        exit()

    def warning(self):
        print(self.message)


class LexerError(GenericError):
    def __init__(self, position, message):
        line, col = position
        self.message = f"Lexer error! line:{line} column:{col} -- {message}"
        super().__init__(self.message)


class ParserError(GenericError):
    pass
