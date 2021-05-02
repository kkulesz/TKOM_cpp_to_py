from src.errors import ParserSyntaxError
from src.lexer.token import TokenType


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__current_token = None

    def parse(self):
        program = []

        while self.__get_current_token().get_type() == TokenType.EOF:
            new_ins = self.__parse_instruction()
            if new_ins is None:
                pass  # error no instruction
            program.append(new_ins)

        return program

    def __parse_instruction(self):
        # instead of if-else everywhere
        return self.__parse_declaration() or \
               self.__parse_if() or \
               self.__parse_print() or \
               self.__parse_while() or \
               self.__parse_id_starting

    def __parse_declaration(self):
        # __demand type
        # __demand id
        # return parse_function_declaration or parse_variable_declaration
        pass

    def __parse_function_declaration(self):
        # __demand type
        # __demand(id)
        # (
        # __parse_function_arguments
        # )
        # {
        # __parse_statement
        # jezeli return
        #   to demand __parse_r_value
        #   ;
        # }
        pass

    def __parse_variable_declaration(self):
        # __demand type
        # __demand(id)
        # =
        # __parse_r_value
        pass

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
        current_token_type = self.__get_next_token().get_type()
        for token_type in list_of_tokens_types:
            if self.__check_token(token_type):
                return
        ParserSyntaxError(self.__current_token.get_position(), current_token_type, expected_message).fatal()

    def __demand_token(self, expected_token_type):
        current_token_type = self.__get_next_token().get_type()
        if self.__check_token(expected_token_type):
            return
        ParserSyntaxError(self.__current_token.get_position(), current_token_type, expected_token_type).fatal()

    def __check_token(self, expected_token_type):
        return self.__current_token.get_type() == expected_token_type

    def __get_current_token(self):
        return self.__current_token

    def __get_next_token(self):
        self.__current_token = self.__lexer.build_and_get_token()
        return self.__current_token
