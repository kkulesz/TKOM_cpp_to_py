from src.errors import ParserSyntaxError, ParserError
from src.lexer.token import TokenType
from src.parser.ast.complex import *
from src.parser.ast.semi_complex import *
from src.parser.ast.primitives import *
from src.parser.parser_utils import ParserUtils


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__current_token = None
        self.__is_consumed = False

    def parse(self):
        program = []
        self.__get_next_token()
        while self.__get_current_token().get_type() != TokenType.EOF:
            new_ins = self.__parse_instruction()
            print(new_ins)
            program.append(new_ins)
            if self.__is_consumed:
                self.__get_next_token()

        return program

    def __parse_instruction(self):
        # instead of if-else everywhere
        maybe_instruction = self.__parse_declaration() or \
                            self.__parse_id_starting() or \
                            self.__parse_print() or \
                            self.__parse_return() or \
                            self.__parse_while() or \
                            self.__parse_if()

        if not maybe_instruction:
            ParserError(self.__get_position(), "unknown instruction!").fatal()
        return maybe_instruction

    def __parse_declaration(self):
        maybe_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not maybe_type_token:
            return None

        id_token = self.__demand_next_token(TokenType.IDENTIFIER)
        self.__get_next_token()

        maybe_function_declaration = self.__parse_function_declaration(maybe_type_token, id_token)
        if maybe_function_declaration:
            return maybe_function_declaration

        maybe_variable_declaration = self.__parse_variable_declaration(maybe_type_token, id_token)
        if maybe_variable_declaration:
            return maybe_variable_declaration

        self.__demand_current_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token)

    def __parse_additive_factor(self):
        additive_factor = None
        maybe_literal = self.__check_if_one_of_tokens(ParserUtils.literal_tokens)
        if maybe_literal:
            additive_factor = Literal(maybe_literal)

        maybe_id = self.__check_current_token(TokenType.IDENTIFIER)
        if maybe_id:
            additive_factor = Id(maybe_id)

        if self.__check_current_token(TokenType.OP_BRACKET):
            self.__get_next_token()
            # TODO: zastanowic sie co z nawiasami, czy trzeba jakos explicite to zapisywac czy bedzie wynikalo z
            #  kontekstu
            additive_factor = self.__parse_arithmetic_expression()
            self.__demand_current_token(TokenType.CL_BRACKET)

        if additive_factor:
            self.__get_next_token()
        return additive_factor

    def __parse_multiplicative_factor(self):
        multiplicative_factor = self.__parse_additive_factor()
        if multiplicative_factor:
            while self.__check_if_one_of_tokens(ParserUtils.multiplicative_operator_tokens):
                multiplicative_token = self.__get_current_token()
                self.__get_next_token()
                multiplicative_factor = ArithmeticExpression(multiplicative_factor,
                                                             ArithmeticOperator(multiplicative_token),
                                                             self.__parse_additive_factor())

        return multiplicative_factor

    def __parse_arithmetic_expression(self):
        result = self.__parse_multiplicative_factor()

        if result:
            while self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens):
                additive_token = self.__get_current_token()
                self.__get_next_token()
                result = ArithmeticExpression(result, ArithmeticOperator(additive_token),
                                              self.__parse_additive_factor())

        return result

    # def __parse_single_condition(self):
    #     left = self.__parse_arithmetic_expression()
    #     maybe_comparison_operator = None
    #     maybe_right = None
    #     if left:
    #         maybe_comparison_operator = self.__check_if_one_of_tokens(ParserUtils.comparison_tokens)
    #         self.__get_next_token()
    #         if maybe_comparison_operator:
    #             maybe_right = self.__parse_arithmetic_expression()
    #             if not maybe_right:
    #                 ParserError(self.__get_position(), "expected literal, id or math expression!").fatal()
    #     return SingleCondition(left, maybe_comparison_operator, maybe_right)
    #
    # def __parse_condition(self):
    #     return self.__parse_single_condition()

    def __parse_r_value(self):
        return self.__parse_arithmetic_expression()

    def __parse_condition(self):
        return self.__parse_arithmetic_expression()

    def __parse_function_declaration_arguments(self):
        maybe_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not maybe_type_token:
            return []

        id_token = self.__demand_next_token(TokenType.IDENTIFIER)
        arguments_fo_far = [FunctionArgument(maybe_type_token, id_token)]
        while self.__check_next_token(TokenType.COMA):
            self.__get_next_token()
            type_token = self.__demand_one_of_tokens(ParserUtils.type_tokens, "type token")
            id_token = self.__demand_next_token(TokenType.IDENTIFIER)
            arguments_fo_far.append(FunctionArgument(type_token, id_token))

        return arguments_fo_far

    def __parse_function_declaration(self, type_token, id_token):
        if not self.__check_current_token(TokenType.OP_BRACKET):
            return None

        self.__get_next_token()
        arguments = self.__parse_function_declaration_arguments()
        self.__demand_current_token(TokenType.CL_BRACKET)
        self.__demand_next_token(TokenType.OP_CURLY_BRACKET)
        instructions = []
        while not self.__check_next_token(TokenType.CL_CURLY_BRACKET):
            instructions.append(self.__parse_instruction())

        return FunctionDeclaration(type_token, id_token, arguments, instructions)

    def __parse_variable_declaration(self, maybe_type_token, id_token):
        if not self.__check_current_token(TokenType.ASSIGN):
            return None
        self.__get_next_token()
        value = self.__parse_r_value()
        self.__demand_current_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token, value)

    def __parse_id_starting(self):
        maybe_id_token = self.__check_current_token(TokenType.IDENTIFIER)
        if not maybe_id_token:
            return None

        maybe_assignment = self.__parse_assignment(maybe_id_token)
        if maybe_assignment:
            return maybe_assignment

        maybe_function_invocation = self.__parse_function_invocation(maybe_id_token)
        if maybe_function_invocation:
            return maybe_function_invocation

        ParserError(self.__get_position(), f"invalid token({self.__get_current_token()}) after id!").fatal()

    def __parse_assignment(self, id_token):
        if not self.__check_next_token(TokenType.ASSIGN):
            return None

        self.__get_next_token()
        value = self.__parse_r_value()
        self.__demand_current_token(TokenType.SEMICOLON)

        return VariableAssignment(id_token, value)

    def __get_literal_or_id(self):
        maybe_id_token = self.__check_current_token(TokenType.IDENTIFIER)
        if maybe_id_token:
            return Id(maybe_id_token)

        maybe_literal_token = self.__check_if_one_of_tokens(ParserUtils.literal_tokens)
        if maybe_literal_token:
            return Literal(maybe_literal_token)

        ParserError(self.__get_position(), "invalid function argument token!").fatal()

    def __parse_function_invocation_arguments(self):
        maybe_id_token = self.__check_if_one_of_tokens(ParserUtils.function_invocation_tokens)
        if not maybe_id_token:
            return []

        arguments_so_far = [Id(maybe_id_token)]
        while self.__check_next_token(TokenType.COMA):
            self.__get_next_token()
            arguments_so_far.append(self.__get_literal_or_id())

        return arguments_so_far

    def __parse_function_invocation(self, id_token):
        if not self.__check_current_token(TokenType.OP_BRACKET):
            return None

        self.__get_next_token()
        arguments = self.__parse_function_invocation_arguments()
        self.__demand_current_token(TokenType.CL_BRACKET)
        self.__demand_next_token(TokenType.SEMICOLON)

        return FunctionInvocation(id_token, arguments)

    def __parse_return(self):
        if not self.__check_current_token(TokenType.RETURN_KW):
            return None

        self.__get_next_token()
        maybe_return_value = self.__parse_r_value()
        self.__demand_current_token(TokenType.SEMICOLON)

        return ReturnExpression(maybe_return_value)

    def __parse_if(self):
        if not self.__check_current_token(TokenType.IF_KW):
            return None

        self.__demand_next_token(TokenType.OP_BRACKET)
        self.__get_next_token()
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), "condition is a must in if statement!").fatal()
        self.__demand_current_token(TokenType.CL_BRACKET)
        self.__demand_next_token(TokenType.OP_CURLY_BRACKET)
        if_instructions = self.__parse_scope()

        else_instruction = None
        if self.__check_next_token(TokenType.ELSE_KW):
            self.__demand_next_token(TokenType.OP_CURLY_BRACKET)
            else_instruction = self.__parse_scope()

        return IfStatement(condition, if_instructions, else_instruction)

    def __parse_while(self):
        if not self.__check_current_token(TokenType.WHILE_KW):
            return None

        self.__demand_next_token(TokenType.OP_BRACKET)
        self.__get_next_token()
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), "condition is a must in while statement!").fatal()
        self.__demand_current_token(TokenType.CL_BRACKET)
        self.__demand_next_token(TokenType.OP_CURLY_BRACKET)
        instructions = self.__parse_scope()
        return WhileStatement(condition, instructions)

    def __parse_print(self):
        if not self.__check_current_token(TokenType.COUT_KW):
            return None
        self.__demand_next_token(TokenType.STREAM_OPERATOR)
        self.__get_next_token()
        statement_to_print = self.__parse_r_value()
        self.__demand_current_token(TokenType.STREAM_OPERATOR)
        self.__demand_next_token(TokenType.ENDL_KW)  # TODO: make this optional and set flag in statement
        self.__demand_next_token(TokenType.SEMICOLON)
        return PrintStatement(statement_to_print)

    def __parse_scope(self):
        scope = []
        self.__get_next_token()
        while not self.__check_current_token(TokenType.CL_CURLY_BRACKET):
            new_instruction = self.__parse_instruction()
            scope.append(new_instruction)
            if self.__is_consumed:
                self.__get_next_token()
        return scope

    # demand functions
    def __demand_one_of_tokens(self, list_of_tokens_types, expected_message):
        maybe_token = self.__check_if_one_of_tokens(list_of_tokens_types)
        if maybe_token:
            return maybe_token

        ParserSyntaxError(self.__current_token.get_position(),
                          self.__current_token.get_type(),
                          expected_message).fatal()

    def __demand_next_token(self, expected_token_type):
        self.__get_next_token()
        return self.__demand_current_token(expected_token_type)

    def __demand_current_token(self, expected_token_type):
        if self.__check_current_token(expected_token_type):
            return self.__current_token

        ParserSyntaxError(self.__current_token.get_position(),
                          expected_token_type,
                          self.__current_token.get_type()
                          ).fatal()

    # check functions
    def __check_current_token(self, expected_token_type):
        if self.__current_token.get_type() == expected_token_type and not self.__is_consumed:
            self.__is_consumed = True
            return self.__current_token
        return None

    def __check_next_token(self, expected_token_type):
        self.__get_next_token()
        return self.__check_current_token(expected_token_type)

    def __check_if_one_of_tokens(self, list_of_tokens_types):
        for token_type in list_of_tokens_types:
            if self.__check_current_token(token_type):
                return self.__current_token
        return None

    # get functions
    def __get_current_token(self):
        return self.__current_token

    def __get_next_token(self):
        self.__is_consumed = False
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token

    def __get_position(self):
        return self.__current_token.get_position()
