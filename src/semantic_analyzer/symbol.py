from abc import ABC


class Symbol(ABC):
    pass


class VariableSymbol(Symbol):
    def __init__(self, var_type, var_id):
        self.type = var_type
        self.id = var_id


class FunctionSymbol(Symbol):
    def __init__(self, fun_type, fun_id, fun_args):
        self.type = fun_type
        self.id = fun_id
        self.args = fun_args
