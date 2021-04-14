from io import StringIO


class CodeProvider:
    def __init__(self, input_stream):
        self.line = 1
        self.column = 0
        self.stream = input_stream
        self.curr_char = self.get_next_char()

    '''
    trzeba pomyslec jak zrobic z get_char i get_next_char
    '''



    def get_position(self):
        return self.line, self.column
