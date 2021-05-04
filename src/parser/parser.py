from src.errors import ParserSyntaxError
from src.lexer.token import TokenType
from src.parser.ast.complex import *
from src.parser.ast.semi_complex import *
from src.parser.ast.primitives import *
from src.parser.parser_utils import ParserUtils


# TODO: następnie:
#   __parse_function_declaration
#       __parse scope
#   __parse_id_starting
#       __variable assignment
#       __function_invocation


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__current_token = None

    def parse(self):
        program = []
        self.__get_next_token()
        while self.__get_current_token().get_type() != TokenType.EOF:
            new_ins = self.__parse_instruction()
            if new_ins is None:
                pass  # error no instruction
            print(new_ins)
            program.append(new_ins)
            self.__get_next_token()

        return program

    def __parse_instruction(self):
        # instead of if-else everywhere
        return self.__parse_declaration() or \
               self.__parse_if() or \
               self.__parse_print() or \
               self.__parse_while() or \
               self.__parse_id_starting

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

        self.__get_next_token()
        return additive_factor

    def __parse_multiplicative_factor(self):
        multiplicative_factor = self.__parse_additive_factor()
        if multiplicative_factor:
            while self.__check_if_one_of_tokens(ParserUtils.multiplicative_operator_tokens):
                multiplicative_token = self.__demand_one_of_tokens(ParserUtils.multiplicative_operator_tokens,
                                                                   "multiplicative operator")
                self.__get_next_token()
                multiplicative_factor = ArithmeticExpression(multiplicative_factor,
                                                             ArithmeticOperator(multiplicative_token),
                                                             self.__parse_additive_factor())

        return multiplicative_factor

    def __parse_arithmetic_expression(self):
        result = self.__parse_multiplicative_factor()

        if result:
            while self.__check_if_one_of_tokens(ParserUtils.additive_operator_tokens):
                additive_token = self.__demand_one_of_tokens(ParserUtils.additive_operator_tokens, "additive operator")
                self.__get_next_token()
                result = ArithmeticExpression(result, ArithmeticOperator(additive_token),
                                              self.__parse_additive_factor())

        return result

    def __parse_r_value(self):
        return self.__parse_arithmetic_expression()

    def __parse_function_declaration_arguments(self):
        maybe_id_token = self.__check_next_token(TokenType.IDENTIFIER)
        if not maybe_id_token:
            return None

        arguments_fo_far = [Id(maybe_id_token)]
        while self.__check_next_token(TokenType.COMA):
            arguments_fo_far.append(Id(self.__demand_next_token(TokenType.IDENTIFIER)))

        return arguments_fo_far

    def __parse_function_declaration(self, type_token, id_token):
        if not self.__check_current_token(TokenType.OP_BRACKET):
            return None
        arguments = self.__parse_function_declaration_arguments()
        self.__demand_current_token(TokenType.CL_BRACKET)
        self.__demand_next_token(TokenType.OP_CURLY_BRACKET)
        instructions = []
        # TODO: DEMAND SCOPE( instructions.append while return)
        self.__demand_next_token(TokenType.CL_CURLY_BRACKET)
        return FunctionDeclaration(type_token, id_token, arguments, instructions)

    def __parse_variable_declaration(self, maybe_type_token, id_token):
        if not self.__check_current_token(TokenType.ASSIGN):
            return None
        self.__get_next_token()
        value = self.__parse_r_value()
        self.__demand_current_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token, value)

    def __parse_id_starting(self):
        id_token = self.__check_current_token(TokenType.IDENTIFIER)
        if not id_token:
            return None
        pass

    def __parse_assignment(self):
        # __demand(id)
        # =
        # __parse_r_value ;
        pass

    def __parse_function_invocation(self):
        # __demand id (
        # parse_arguments
        # ) ;
        pass

    def __parse_if(self):
        # if ( <condition> ) {
        # __parse_statement
        # }
        # self.__parse_else()
        pass

    def __parse_else(self):
        # else {
        # __parse_statement
        # }
        pass

    def __parse_while(self):
        # while (
        # __parse_condition
        # ) {
        # __parse_statement
        # }
        pass

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
        if self.__current_token.get_type() == expected_token_type:
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
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token

    def __get_position(self):
        return self.__current_token.get_position()
