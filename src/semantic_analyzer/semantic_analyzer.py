from src.parser.ast.primitives import *
from src.parser.ast.semi_complex import *
from src.parser.ast.complex import *

from src.semantic_analyzer.symbol import *

from src.errors import *

# for arithmetic expressions
INT_TYPE = Type(Token(TokenType.INT_KW))


class SemanticAnalyzer:
    def __init__(self):
        pass

    def start_analysis(self, program):
        return self.__analyze_scope(program, {}, {}, False, None)

    def __check_fun_declaration(self, fun_decl, var_symbols, fun_symbols):
        pass

    def __check_var_declaration(self, var_decl, var_symbols, fun_symbols):
        var_name = var_decl.id.name
        if var_name in var_symbols:
            SemanticVariableRedeclarationError(var_name).fatal()
        self.__check_r_value(var_decl.value, var_symbols, fun_symbols, var_decl.type)

        new_var_symbol = VariableSymbol(var_decl.type, var_name)
        var_symbols[var_name] = new_var_symbol

    def __check_var_assignment(self, var_assignment, var_symbols, fun_symbols):
        var_name = var_assignment.id.name
        if var_name not in var_symbols:
            SemanticUnknownSymbolError(var_name).fatal()
            # TODO: moze warning, bo w pythonie przypsianie nie rozni sie od deklaracji

        var_type = var_symbols[var_name].get_type()
        self.__check_r_value(var_assignment.value, var_symbols, fun_symbols, var_type)

    def __check_if_stmt(self, if_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        condition = if_stmt.condition
        self.__check_condition(condition, var_symbols, fun_symbols)
        if_instructions = if_stmt.if_instructions
        else_instructions = if_stmt.else_instructions
        self.__analyze_scope(if_instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)
        self.__analyze_scope(else_instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

    def __check_while_stmt(self, while_stmt, var_symbols, fun_symbols, is_inside_fun, return_type):
        condition = while_stmt.condition
        self.__check_condition(condition, var_symbols, fun_symbols)
        instructions = while_stmt.instructions
        self.__analyze_scope(instructions, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)

    def __check_return_expr(self, return_expr, var_symbols, fun_symbols, is_inside_fun, return_type):
        if not is_inside_fun:
            pass  # TODO: blad o nie byciu w fynkcji

        self.__check_r_value(return_expr.value, var_symbols, fun_symbols, return_type)

    def __check_arithmetic_expr(self, arithmetic_expr, var_symbols, fun_symbols):
        left = arithmetic_expr.left_operand
        right = arithmetic_expr.right_operand
        self.__check_r_value(left, var_symbols, fun_symbols, INT_TYPE)
        self.__check_r_value(right, var_symbols, fun_symbols, INT_TYPE)

    def __check_fun_invocation(self, fun_invocation, var_symbols, fun_symbols):
        pass

    def __check_print_stmt(self, print_stmt, var_symbols, fun_symbols):
        self.__check_r_value(print_stmt.to_print, var_symbols, fun_symbols, expected_type=None)

    def __check_condition(self, condition, var_symbols, fun_symbols):
        if isinstance(condition, Literal):
            pass
        elif isinstance(condition, Id):
            pass
        elif isinstance(condition, SingleCondition):
            pass
        else:
            pass  # TODO: development error

    def __check_r_value(self, r_value, var_symbols, fun_symbols, expected_type):
        if isinstance(r_value, Literal):
            self.__check_literal(r_value, expected_type)
        elif isinstance(r_value, Id):
            self.__check_var_id(r_value, var_symbols, expected_type)
        elif isinstance(r_value, ArithmeticExpression):
            if expected_type == INT_TYPE:
                self.__check_arithmetic_expr(r_value, var_symbols, fun_symbols)
            else:
                SemanticNotNumberInArithmeticExprError(expected_type).fatal()
        else:
            SemanticAnalyzerDevelopmentError(f"unknown right value! - {r_value}").fatal()

    def __check_var_id(self, var_id, var_symbols, expected_type):
        var_name = var_id.name
        if var_name not in var_symbols:
            SemanticUnknownSymbolError(var_name).fatal()
        if expected_type is not None and expected_type != var_symbols[var_name].type:
            SemanticInvalidTypeError(expected_type, var_symbols[var_name].type).fatal()

    def __check_literal(self, literal, expected_type):
        if expected_type is not None and literal.type != expected_type:
            SemanticInvalidTypeError(expected_type, literal.type).fatal()

    def __analyze_scope(self, list_of_instructions, var_symbols, fun_symbols, is_inside_fun, return_type):
        for ins in list_of_instructions:
            if isinstance(ins, FunctionDeclaration):
                self.__check_fun_declaration(ins, var_symbols.copy(), fun_symbols.copy())
            elif isinstance(ins, VariableDeclaration):
                self.__check_var_declaration(ins, var_symbols, fun_symbols)
            elif isinstance(ins, VariableAssignment):
                self.__check_var_assignment(ins, var_symbols, fun_symbols)
            elif isinstance(ins, IfStatement):
                self.__check_if_stmt(ins, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)
            elif isinstance(ins, WhileStatement):
                self.__check_while_stmt(ins, var_symbols.copy(), fun_symbols.copy(), is_inside_fun, return_type)
            elif isinstance(ins, FunctionInvocation):
                self.__check_fun_invocation(ins, var_symbols, fun_symbols)
            elif isinstance(ins, ReturnExpression):
                self.__check_return_expr(ins, var_symbols, fun_symbols, is_inside_fun, return_type)
            elif isinstance(ins, PrintStatement):
                self.__check_print_stmt(ins, var_symbols, fun_symbols)
            else:
                SemanticAnalyzerDevelopmentError(f"unknown instruction in scope: {ins}!").fatal()
        # print(var_symbols)
        return list_of_instructions  # if everything is correct then function is 'transparent'
