from src.errors.error import *


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


class SemanticNoSuchFunctionError(SemanticError):
    def __init__(self, fun_name):
        self.message = f"no function named {fun_name}"
        super(SemanticNoSuchFunctionError, self).__init__(self.message)


class SemanticInvalidNumberOfArgsError(SemanticError):
    def __init__(self, got, expected):
        self.message = f"invalid number of args: expected {got}, but got {expected}"
        super(SemanticInvalidNumberOfArgsError, self).__init__(self.message)


class SemanticTypesOfArgsInFunInvocationError(SemanticError):
    def __init__(self, fun_name, got, expected):
        self.message = f"invalid types of args in function({fun_name}) arguments:\n\t expected {got}, but got {expected}"
        super(SemanticTypesOfArgsInFunInvocationError, self).__init__(self.message)


class SemanticAnalyzerDevelopmentError(SemanticError):
    def __init__(self, message):
        self.message = f"SEMANTIC ANALYZER DEVELOPMENT ERROR: {message}"
        super(SemanticAnalyzerDevelopmentError, self).__init__(self.message)
