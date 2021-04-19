from src.errors import LexerError
from src.lexer.token import TokenType, TokenDicts, Token


class Lexer:
    def __init__(self, code_provider):
        self.code_provider = code_provider
        self.token = None
        self.curr_pos = None

    def get_token(self):
        return self.token

    def build_and_get_token(self):
        self.__ignore_whites()
        line, col = self.code_provider.get_position()
        token = self.__try_match()
        token.column = col
        token.line = line

        self.token = token
        return self.token

    def __ignore_whites(self):
        curr_char = self.code_provider.get_char()
        while curr_char in [' ', '\t', '\n']:
            curr_char = self.code_provider.move_and_get_char()

    def __try_match(self):
        self.curr_pos = self.code_provider.get_position()
        # instead of 'if else' everywhere
        return self.__try_eof() or \
               self.__try_id_or_keyword() or \
               self.__try_number() or \
               self.__try_string() or \
               self.__try_operators_or_comments() or \
               self.__get_undefined_and_move()

    # try methods
    def __try_eof(self):
        if self.code_provider.get_char() == '':
            return Token(TokenType.EOF)
        return None

    def __try_id_or_keyword(self):
        candidate = self.__read_word()
        if candidate in TokenDicts.acceptable_keywords:
            token_type = TokenDicts.acceptable_keywords[candidate]
            return Token(token_type)
        elif candidate != "":
            return Token(TokenType.IDENTIFIER, candidate)

        return None

    def __try_number(self):
        value_so_far = 0
        digit_candidate = self.code_provider.get_char()
        if digit_candidate.isdigit():
            if digit_candidate == '0':
                self.__move_pointer()
                return Token(TokenType.INT_LITERAL, value_so_far)

            value_so_far = ord(digit_candidate) - ord('0')
            digit_candidate = self.code_provider.move_and_get_char()
            while digit_candidate.isdigit():
                value_so_far *= 10
                value_so_far += ord(digit_candidate) - ord('0')
                digit_candidate = self.code_provider.move_and_get_char()
            return Token(TokenType.INT_LITERAL, value_so_far)

        return None

    def __try_string(self):
        character = self.code_provider.get_char()
        if character == '"':
            string = ''
            character = self.code_provider.move_and_get_char()
            while character != '"':
                string += character
                character = self.code_provider.move_and_get_char()

            self.__move_pointer()  # move so next char will not be quote
            return Token(TokenType.STRING_LITERAL, string)
        return None

    def __try_operators_or_comments(self):
        tmp_token = None
        candidate = self.code_provider.get_char()
        if candidate in TokenDicts.single_char_tokens:
            tmp_token_type = TokenDicts.single_char_tokens[candidate]
            tmp_token = Token(tmp_token_type)

        candidate += self.code_provider.move_and_get_char()
        if candidate in TokenDicts.double_char_tokens:
            tmp_token_type = TokenDicts.double_char_tokens[candidate]

            if tmp_token_type == TokenType.START_SINGLE_LINE_COMMENT:
                comment_value = self.__get_characters_to_new_line()
                tmp_token = Token(TokenType.SINGLE_LINE_COMMENT, comment_value)

            elif tmp_token_type == TokenType.START_MULTI_LINE_COMMENT:
                comment_value = self.__get_characters_to_end_of_multiline()
                tmp_token = Token(TokenType.MULTI_LINE_COMMENT, comment_value)

            else:
                tmp_token = Token(tmp_token_type)

            self.__move_pointer()
        return tmp_token

    def __get_undefined_and_move(self):
        char = self.code_provider.get_char()
        self.__move_pointer()  # move so we can continue after undefined
        LexerError(self.code_provider.get_position(), "unidentified token").warning()
        return Token(TokenType.UNDEFINED, char)

    def __read_word(self):
        word_so_far = ""
        new_char = self.code_provider.get_char()
        if new_char.isalpha():
            while new_char.isalpha() or new_char.isdigit():
                word_so_far += new_char
                new_char = self.code_provider.move_and_get_char()
        return word_so_far

    def __get_characters_to_new_line(self):
        string_of_chars = ""
        character = self.code_provider.move_and_get_char()
        while character != '\n' and character != '':
            string_of_chars += character
            character = self.code_provider.move_and_get_char()
        return string_of_chars

    def __get_characters_to_end_of_multiline(self):
        string_of_chars = ""
        character = self.code_provider.move_and_get_char()
        next_character = self.code_provider.move_and_get_char()
        maybe_end_of_comment = character + next_character
        while maybe_end_of_comment != '*/':
            if maybe_end_of_comment == "":
                LexerError(self.code_provider.get_position(), "no end of multi-line comment").warning()
                return string_of_chars
            string_of_chars += character
            character = next_character
            next_character = self.code_provider.move_and_get_char()
            maybe_end_of_comment = character + next_character
        return string_of_chars #[:-1]

    def __move_pointer(self):
        _ = self.code_provider.move_and_get_char()
