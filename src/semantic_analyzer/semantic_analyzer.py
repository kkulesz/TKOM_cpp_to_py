class SemanticAnalyzer:
    def __init__(self):
        pass

    def analyze_scope(self, list_of_instructions, var_symbols={}, fun_symbols={}):
        pass

    def check_fun_declaration(self, fun_decl, var_symbols, fun_symbols):
        pass

    def check_var_declaration(self, var_decl, var_symbols, fun_symbols):
        pass

    def check_var_assignment(self, var_assignment, var_symbols, fun_symbols):
        pass

    def check_math_expression(self, math_expression, var_symbols, fun_symbols):
        pass

    def check_if_stmt(self, if_stmt, var_symbols, fun_symbols):
        pass

    def check_while_stmt(self, while_stmt, var_symbols, fun_symbols):
        pass
