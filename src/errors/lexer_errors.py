from src.errors.error import *


class LexerError(GenericError):
    def __init__(self, position, message):
        line, col = position
        self.message = f"Lexer error! line:{line} column:{col} -- {message}!"
        super().__init__(self.message)


class LexerNoEndOfStringProvidedError(LexerError):
    def __init__(self, position):
        self.message = "no end of string provided"
        super().__init__(position, self.message)


class LexerNoEndOfMultilineCommentProvidedError(LexerError):
    def __init__(self, position):
        self.message = "no end of multi-line comment"
        super().__init__(position, self.message)


class LexerUndefinedTokenError(LexerError):
    def __init__(self, position):
        self.message = "undefined token"
        super().__init__(position, self.message)


class LexerInvalidStdTokenError(LexerError):
    def __init__(self, position):
        self.message = "invalid std token"
        super().__init__(position, self.message)


class LexerOverwrittenPythonKeywordError(LexerError):
    def __init__(self, position, keyword):
        self.message = f"overwritten Python keyword-{keyword}"
        super().__init__(position, self.message)


class LexerOverwrittenCppKeywordError(LexerError):
    def __init__(self, position, keyword):
        self.message = f"overwritten C++ keyword-{keyword}, input code cannot be executed"
        super().__init__(position, self.message)
