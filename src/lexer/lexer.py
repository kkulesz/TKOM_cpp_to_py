from src.lexer.token import TokenType, TokenDicts, Token


class Lexer:
    def __init__(self, code_provider):
        self.code_provider = code_provider
        self.token = None
        self.curr_pos = None

    def get_token(self):
        return self.token

    def build_and_get_token(self):
        self.ignore_whites()
        line, col = self.code_provider.get_position()
        token = self.try_match()
        token.column = col
        token.line = line

        self.token = token
        return self.token

    def ignore_whites(self):
        curr_char = self.code_provider.get_char()
        while curr_char in [' ', '\t', '\n']:
            curr_char = self.code_provider.move_and_get_char()

    def try_match(self):
        self.curr_pos = self.code_provider.get_position()
        # instead of 'if else' everywhere
        return self.try_eof() or \
               self.try_id_or_keyword() or \
               self.try_number() or \
               self.try_string() or \
               self.try_operators_or_comments() or \
               self.get_undefined_and_move()

    # try methods
    def try_eof(self):
        if self.code_provider.get_char() == '':
            return Token(TokenType.EOF)
        return None

    def try_id_or_keyword(self):
        candidate = self.read_word()
        if candidate in TokenDicts.acceptable_keywords:
            token_type = TokenDicts.acceptable_keywords[candidate]
            return Token(token_type, candidate)
        elif candidate != "":
            return Token(TokenType.IDENTIFIER, candidate)

        return None

    def try_number(self):
        value_so_far = 0
        digit_candidate = self.code_provider.get_char()
        if digit_candidate.isdigit():
            if digit_candidate == '0':
                self.move_pointer()
                return Token(TokenType.INT_LITERAL, value_so_far)

            value_so_far = ord(digit_candidate) - ord('0')
            digit_candidate = self.code_provider.move_and_get_char()
            while digit_candidate.isdigit():
                value_so_far *= 10
                value_so_far += ord(digit_candidate) - ord('0')
                digit_candidate = self.code_provider.move_and_get_char()
            return Token(TokenType.INT_LITERAL, value_so_far)

        return None

    def try_string(self):
        character = self.code_provider.get_char()
        if character == '"':
            string = ''
            character = self.code_provider.move_and_get_char()
            while character != '"':
                string += character

            self.move_pointer()  # move so next char will not be quote
            return Token(TokenType.STRING_LITERAL, string)
        return None

    def get_characters_to_new_line(self):
        pass

    def get_characters_to_enf_of_multiline(self):
        pass

    def try_operators_or_comments(self):
        # double char
        # == && || >= <= !=

        # comments
        # // /*

        # single char
        # + - / !
        return None

    def get_undefined_and_move(self):
        char = self.code_provider.get_char()
        self.move_pointer()  # move so we can continue after undefined
        return Token(TokenType.UNDEFINED, char)

    def read_word(self):
        word_so_far = ""
        new_char = self.code_provider.get_char()
        if new_char.isalpha():
            while new_char.isalpha() or new_char.isdigit():
                word_so_far += new_char
                new_char = self.code_provider.move_and_get_char()
        return word_so_far

    def move_pointer(self):
        _ = self.code_provider.move_and_get_char()
