class Utils:
    python_forbidden_keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
                                 'expect', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in',
                                 'is', 'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
                                 'try', 'while', 'with', 'yield']
    cpp_forbidden_keywords = ['auto', 'bool', 'break', 'case', 'catch', 'char', 'class', 'const', 'continue',
                              'default', 'do', 'double', 'else', 'enum', 'false', 'float', 'for', 'goto',
                              'if', 'int', 'long', 'namespace', 'new', 'not', 'nullptr', 'or', 'private', 'public',
                              'return', 'short', 'signed', 'sizeof', 'static', 'switch', 'this', 'throw', 'true',
                              'try', 'typedef', 'union', 'unsigned', 'using', 'void', 'while']

    forbidden_ids = python_forbidden_keywords + cpp_forbidden_keywords
