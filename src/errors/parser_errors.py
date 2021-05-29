from src.errors.error import *


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
