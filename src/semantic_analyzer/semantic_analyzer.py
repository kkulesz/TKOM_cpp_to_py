from src.parser.ast.primitives import *
from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *

from src.errors import SemanticAnalyzerDevelopmentError


class SemanticAnalyzer:
    def __init__(self):
        pass

    def start_analysis(self, program):
        return self.__analyze_scope(program, {}, {}, False)

    def __check_fun_declaration(self, fun_decl, var_symbols, fun_symbols):
        pass

    def __check_var_declaration(self, var_decl, var_symbols, fun_symbols):
        pass

    def __check_var_assignment(self, var_assignment, var_symbols, fun_symbols):
        pass

    def __check_if_stmt(self, if_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_while_stmt(self, while_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_return_expr(self, return_expr, var_symbols, fun_symbols, is_inside_fun, return_type):
        pass

    def __check_arithmetic_expr(self, arithmetic_expr, var_symbols, fun_symbols):
        pass

    def __check_fun_invocation(self, fun_invocation, var_symbols, fun_symbols):
        pass

    def __check_print_stmt(self, print_stmt, var_symbols, fun_symbols):
        pass

    def __check_condition(self, condition, var_symbols, fun_symbols):
        pass

    def __analyze_scope(self, list_of_instructions, var_symbols, fun_symbols, is_inside_fun, return_type):
        for ins in list_of_instructions:
            if isinstance(ins, FunctionDeclaration):
                self.__check_fun_declaration(ins, var_symbols, fun_symbols)
            elif isinstance(ins, VariableDeclaration):
                self.__check_var_declaration(ins, var_symbols, fun_symbols)
            elif isinstance(ins, VariableAssignment):
                self.__check_var_assignment(ins, var_symbols, fun_symbols)
            elif isinstance(ins, IfStatement):
                self.__check_if_stmt(ins, var_symbols, fun_symbols, is_inside_fun, return_type)
            elif isinstance(ins, WhileStatement):
                self.__check_while_stmt(ins, var_symbols, fun_symbols, is_inside_fun, return_type)
            elif isinstance(ins, ReturnExpression):
                self.__check_return_expr(ins, var_symbols, fun_symbols, is_inside_fun, return_type)
            else:
                SemanticAnalyzerDevelopmentError("unknown instruction in scope!").fatal()

        return list_of_instructions  # if everything is correct then function is 'transparent'
