from src.errors import ParserSyntaxError
from src.lexer.token import TokenType
from src.parser.ast.semi_complex import *
from src.parser.ast.primitives import *
from src.parser.utils import Utils


# TODO: zastanowic się:
#   czy nie klasyfikować std::string i std::cout<< i <<std::endl
#   ALBO
#   używać using namespace std;


# TODO: __parse_r_value
# TODO: __parse_arguments


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
        maybe_type_token = self.__get_current_token()
        if not self.__check_if_one_of_tokens(Utils.types_token):
            return None

        id_token = self.__demand_next_token(TokenType.IDENTIFIER)

        maybe_function_declaration = self.__parse_function_declaration(maybe_type_token, id_token)
        if maybe_function_declaration:
            return maybe_function_declaration

        maybe_variable_declaration = self.__parse_variable_declaration(maybe_type_token, id_token)
        if maybe_variable_declaration:
            return maybe_variable_declaration

        self.__demand_current_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token)

    def __parse_r_value(self):
        maybe_literal = self.__check_if_one_of_tokens([TokenType.INT_LITERAL, TokenType.STRING_LITERAL, TokenType.TRUE_KW, TokenType.FALSE_KW])
        if maybe_literal:
            return Literal(maybe_literal)

        # TODO:maybe_arithmetic_expression = self.__parse_arithmetic_expression
        #  maybe_variable
        #  ParserError expected right_value but got token

    def __parse_function_declaration(self, maybe_type_token, id_token):
        if not self.__check_current_token(TokenType.OP_BRACKET):
            return None

        # __parse_function_arguments
        # demand )
        # demand{
        # instructions = []
        # while
        # jezeli return
        #   to demand __parse_r_value
        #   ;
        # }
        pass

    def __parse_variable_declaration(self, maybe_type_token, id_token):
        self.__get_next_token()
        if not self.__check_current_token(TokenType.ASSIGN):
            return None
        self.__get_next_token()
        value = self.__parse_r_value()
        self.__demand_next_token(TokenType.SEMICOLON)
        return VariableDeclaration(maybe_type_token, id_token, value)

    def __parse_id_starting(self):
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
        # std :: cout <<
        # __parse_print_argument
        # << std :: endl ;
        pass

    # utils functions
    def __demand_one_of_tokens(self, list_of_tokens_types, expected_message):
        if self.__check_if_one_of_tokens(list_of_tokens_types):
            return
        current_token_type = self.__current_token.get_type()
        ParserSyntaxError(self.__current_token.get_position(), current_token_type, expected_message).fatal()

    def __demand_next_token(self, expected_token_type):
        self.__get_next_token()
        return self.__demand_current_token(expected_token_type)

    def __demand_current_token(self, expected_token_type):
        if self.__check_current_token(expected_token_type):
            return self.__current_token
        ParserSyntaxError(self.__current_token.get_position(), self.__current_token.get_type(), expected_token_type).fatal()

    def __check_current_token(self, expected_token_type):
        return self.__current_token.get_type() == expected_token_type

    def __check_if_one_of_tokens(self,list_of_tokens_types):
        for token_type in list_of_tokens_types:
            if self.__check_current_token(token_type):
                return self.__current_token
        return None

    def __get_current_token(self):
        return self.__current_token

    def __get_next_token(self):
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token

    def __get_position(self):
        return self.__current_token.get_position()
