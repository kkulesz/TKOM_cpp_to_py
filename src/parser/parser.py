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
        self.__get_next_token()

    def parse_program(self):
        program = []
        while self.__get_current_token().get_type() != TokenType.EOF:
            new_ins = self.__parse_instruction()
            print(new_ins)
            program.append(new_ins)

        return program

    def __parse_instruction(self):
        # instead of if-else everywhere
        maybe_instruction = self.__parse_declaration() or \
                            self.__parse_id_starting() or \
                            self.__parse_print() or \
                            self.__parse_return() or \
                            self.__parse_while() or \
                            self.__parse_comments() or \
                            self.__parse_if()

        if not maybe_instruction:
            ParserError(self.__get_position(), "unknown instruction!").warning()
        return maybe_instruction

    def __parse_declaration(self):
        maybe_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not maybe_type_token:
            return None

        id_token = self.__demand_token(TokenType.IDENTIFIER)

        maybe_function_declaration = self.__parse_function_declaration(maybe_type_token, id_token)
        if maybe_function_declaration:
            return maybe_function_declaration

        maybe_variable_declaration = self.__parse_variable_declaration(maybe_type_token, id_token)
        if maybe_variable_declaration:
            return maybe_variable_declaration

        self.__demand_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token)

    def __parse_function_declaration(self, type_token, id_token):
        if not self.__check_token(TokenType.OP_BRACKET):
            return None

        arguments = self.__parse_function_declaration_arguments()
        self.__demand_token(TokenType.CL_BRACKET)
        self.__demand_token(TokenType.OP_CURLY_BRACKET)
        instructions = []
        while not self.__check_token(TokenType.CL_CURLY_BRACKET):
            instructions.append(self.__parse_instruction())

        return FunctionDeclaration(type_token, id_token, arguments, instructions)

    def __parse_function_declaration_arguments(self):
        maybe_type_token = self.__check_if_one_of_tokens(ParserUtils.type_tokens)
        if not maybe_type_token:
            return []

        id_token = self.__demand_token(TokenType.IDENTIFIER)
        arguments_fo_far = [FunctionArgument(maybe_type_token, id_token)]
        while self.__check_token(TokenType.COMA):
            type_token = self.__demand_one_of_tokens(ParserUtils.type_tokens, "type token")
            id_token = self.__demand_token(TokenType.IDENTIFIER)
            arguments_fo_far.append(FunctionArgument(type_token, id_token))

        return arguments_fo_far

    def __parse_variable_declaration(self, maybe_type_token, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        value = self.__parse_r_value()
        self.__demand_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token, value)

    def __parse_id_starting(self):
        maybe_id_token = self.__check_token(TokenType.IDENTIFIER)
        if not maybe_id_token:
            return None

        maybe_assignment = self.__parse_assignment(maybe_id_token)
        if maybe_assignment:
            return maybe_assignment

        maybe_function_invocation = self.__parse_function_invocation(maybe_id_token)
        if maybe_function_invocation:
            return maybe_function_invocation

        ParserError(self.__get_position(),
                    f"invalid token after id: {self.__get_current_token()}!"
                    ).fatal()

    def __parse_assignment(self, id_token):
        if not self.__check_token(TokenType.ASSIGN):
            return None

        value = self.__parse_r_value()
        self.__demand_token(TokenType.SEMICOLON)

        return VariableAssignment(id_token, value)

    def __parse_r_value(self):
        return self.__parse_arithmetic_expression()  # TODO: maybe condition later

    def __parse_arithmetic_expression(self):
        result = self.__parse_multiplicative_factor()

        if result:
            additive_token = self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens)
            while additive_token:
                result = ArithmeticExpression(result,
                                              ArithmeticOperator(additive_token),
                                              self.__parse_multiplicative_factor())
                additive_token = self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens)

        return result

    def __parse_multiplicative_factor(self):
        multiplicative_factor = self.__parse_additive_factor()

        if multiplicative_factor:
            maybe_multiplicative_token = self.__check_if_one_of_tokens(ParserUtils.multiplicative_operator_tokens)
            while maybe_multiplicative_token:
                multiplicative_factor = ArithmeticExpression(multiplicative_factor,
                                                             ArithmeticOperator(maybe_multiplicative_token),
                                                             self.__parse_additive_factor())
                maybe_multiplicative_token = self.__check_if_one_of_tokens(
                    ParserUtils.multiplicative_operator_tokens)

        return multiplicative_factor

    def __parse_additive_factor(self):
        additive_factor = self.__parse_id_or_literal()

        if not additive_factor and self.__check_token(TokenType.OP_BRACKET):
            additive_factor = self.__parse_arithmetic_expression()
            self.__demand_token(TokenType.CL_BRACKET)

        return additive_factor

    def __parse_condition(self):
        maybe_left_id_or_literal = self.__parse_id_or_literal()
        if not maybe_left_id_or_literal:
            return None

        maybe_comparison_token = self.__check_if_one_of_tokens(ParserUtils.comparison_tokens)
        if maybe_comparison_token:
            maybe_right_id_or_literal = self.__parse_id_or_literal()
            if not maybe_right_id_or_literal:
                ParserError(self.__get_position(),
                            f"expected literal or id, but got {self.__get_current_token()}"
                            ).fatal()
            return SingleCondition(maybe_left_id_or_literal, maybe_comparison_token, maybe_right_id_or_literal)
        return maybe_left_id_or_literal

    def __parse_function_invocation(self, id_token):
        if not self.__check_token(TokenType.OP_BRACKET):
            return None

        arguments = self.__parse_function_invocation_arguments()
        self.__demand_token(TokenType.CL_BRACKET)
        self.__demand_token(TokenType.SEMICOLON)

        return FunctionInvocation(id_token, arguments)

    def __parse_function_invocation_arguments(self):
        maybe_argument = self.__parse_arithmetic_expression()
        if not maybe_argument:
            return []

        arguments_so_far = [maybe_argument]
        while self.__check_token(TokenType.COMA):
            arguments_so_far.append(self.__parse_arithmetic_expression())

        return arguments_so_far

    def __parse_id_or_literal(self):
        maybe_literal = self.__check_if_one_of_tokens(ParserUtils.literal_tokens)
        if maybe_literal:
            return Literal(maybe_literal)

        maybe_id = self.__check_token(TokenType.IDENTIFIER)
        if maybe_id:
            return Id(maybe_id)

        return None

    def __parse_return(self):
        if not self.__check_token(TokenType.RETURN_KW):
            return None

        maybe_return_value = self.__parse_r_value()
        self.__demand_token(TokenType.SEMICOLON)

        return ReturnExpression(maybe_return_value)

    def __parse_if(self):
        if not self.__check_token(TokenType.IF_KW):
            return None

        self.__demand_token(TokenType.OP_BRACKET)
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), "condition is required in 'if statement'!").fatal()
        self.__demand_token(TokenType.CL_BRACKET)
        self.__demand_token(TokenType.OP_CURLY_BRACKET)
        if_instructions = self.__parse_scope()

        else_instruction = [] # TODO: make it none
        if self.__check_token(TokenType.ELSE_KW):
            self.__demand_token(TokenType.OP_CURLY_BRACKET)
            else_instruction = self.__parse_scope()

        return IfStatement(condition, if_instructions, else_instruction)

    def __parse_while(self):
        if not self.__check_token(TokenType.WHILE_KW):
            return None

        self.__demand_token(TokenType.OP_BRACKET)
        condition = self.__parse_condition()
        if condition is None:
            ParserError(self.__get_position(), "condition is required in 'while statement'!").fatal()
        self.__demand_token(TokenType.CL_BRACKET)
        self.__demand_token(TokenType.OP_CURLY_BRACKET)
        instructions = self.__parse_scope()
        return WhileStatement(condition, instructions)

    def __parse_scope(self):
        scope = []
        while not self.__check_token(TokenType.CL_CURLY_BRACKET):
            new_instruction = self.__parse_instruction()
            scope.append(new_instruction)

        return scope

    def __parse_print(self):
        if not self.__check_token(TokenType.COUT_KW):
            return None
        self.__demand_token(TokenType.STREAM_OPERATOR)
        statement_to_print = self.__parse_r_value()
        self.__demand_token(TokenType.STREAM_OPERATOR)
        self.__demand_token(TokenType.ENDL_KW)  # TODO: make this optional and set flag in statement
        self.__demand_token(TokenType.SEMICOLON)
        return PrintStatement(statement_to_print)

    def __parse_comments(self):
        maybe_single_line = self.__check_token(TokenType.SINGLE_LINE_COMMENT)
        if maybe_single_line:
            return SingleLineComment(maybe_single_line)

        maybe_multi_line = self.__check_token(TokenType.MULTI_LINE_COMMENT)
        if maybe_multi_line:
            return MultiLineComment(maybe_multi_line)

        return None

    #################################
    # UTILS
    def __demand_token(self, expected_token_type):
        token = self.__check_token(expected_token_type)
        if token:
            return token

        ParserSyntaxError(self.__current_token.get_position(),
                          expected_token_type,
                          self.__current_token.get_type()
                          ).fatal()

    def __check_token(self, expected_token_type):
        if self.__current_token.get_type() == expected_token_type:
            token = self.__current_token
            self.__get_next_token()
            return token
        return None

    def __check_if_one_of_tokens(self, list_of_tokens_types):
        for token_type in list_of_tokens_types:
            maybe_token = self.__check_token(token_type)
            if maybe_token:
                return maybe_token
        return None

    def __demand_one_of_tokens(self, list_of_tokens_types, expected_message):
        maybe_token = self.__check_if_one_of_tokens(list_of_tokens_types)
        if maybe_token:
            return maybe_token

        ParserSyntaxError(self.__current_token.get_position(),
                          self.__current_token.get_type(),
                          expected_message).fatal()

    # get functions
    def __get_current_token(self):
        return self.__current_token

    def __get_next_token(self):
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token

    def __get_position(self):
        return self.__current_token.get_position()
