import sys

from src.lexer.code_provider import CodeProvider
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType


def init_all(input_file):
    file = open(input_file, "rt")
    code_provider = CodeProvider(file)
    lexer = Lexer(code_provider)

    token = lexer.build_and_get_token()
    while token.get_type() != TokenType.EOF:
        print(token)
        token = lexer.build_and_get_token()


def main():
    if len(sys.argv) < 2:
        print("Nie podano nazwy pliku wejściowego!")
        return

    program = init_all(sys.argv[1])


if __name__ == "__main__":
    main()
