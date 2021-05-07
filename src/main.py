import sys

from src.lexer.code_provider import CodeProvider
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.parser.parser import Parser


def init_all(input_file):
    file = open(input_file, "rt")
    code_provider = CodeProvider(file)
    lexer = Lexer(code_provider)
    parser = Parser(lexer)

    # token = lexer.build_and_get_token()
    # while token.get_type() != TokenType.EOF:
    #     print(token)
    #     token = lexer.build_and_get_token()

    parser.parse_program()


def main():
    if len(sys.argv) < 2:
        print("Nie podano nazwy pliku wejściowego!")
        return

    init_all(sys.argv[1])


if __name__ == "__main__":
    main()
