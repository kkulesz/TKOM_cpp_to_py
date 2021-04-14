class Lexer:
    def __init__(self, code_provider):
        self.code_provider = code_provider
        self.token = None

    def get_token(self):
        pass

    def build_token(self):
        self.ignore_whites()
        line, col = self.code_provider.get_position()

    def ignore_whites(self):
        curr_char = self.code_provider.get_char()
        while curr_char in [' ', '\t', '\n']:
            curr_char = self.code_provider.move_and_get_char()

    def try_match(self):
        # instead of ifelse everywhere
        return self.try_id_or_keyword() or \
               self.try_number() or \
               self.try_string() or \
               self.try_operators_or_comments()

    # try methods
    def try_id_or_keyword(self):
        # identyfikatory
        # slowa kluczowe
        pass

    def try_number(self):
        # 0[^.] -> INT o wartosci 0
        # xxxx$ -> INT o danej wartości
        # xx.xx -> FLOAT o danej wartosci
        pass

    def try_string(self):
        # w cudzysłowach bez znaku nowej linii
        pass

    def try_operators_or_comments(self):
        # double char
        # == && || >= <= !=

        # single char
        # + - / !

        # comments
        # // /*
        pass


