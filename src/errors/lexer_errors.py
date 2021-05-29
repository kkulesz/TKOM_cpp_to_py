from src.errors.error import *


class LexerError(GenericError):
    def __init__(self, position, message):
        line, col = position
        self.message = f"Lexer error! line:{line} column:{col} -- {message}"
        super().__init__(self.message)