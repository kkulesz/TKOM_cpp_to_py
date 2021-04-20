class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer

    def __parse_statement(self):
        # dopoki nie koniec pliku
        #       sprobuj wszystko co moze istniec same sobie
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

    def __parse_assignment(self):
        # __demand(id)
        # =
        # __parse_r_value ;
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

    def __demand_token(self, token_type):
        return self.__get_current_token() == token_type

    def __get_current_token(self):
        return self.__lexer.get_token()

    def __get_next_token(self):
        return self.__lexer.build_and_get_token()
