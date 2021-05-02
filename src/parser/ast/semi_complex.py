# semi_complex - they cannot contain complex nodes
from src.parser.ast.ast_node import AstNode


class VariableDeclaration(AstNode):
    # int a = 0
    # int a ;
    pass


class VariableAssignment(AstNode):
    # a = 0;
    pass


class Condition(AstNode):
    pass


class ArithmeticOperation(AstNode):
    pass


class PrintStatement(AstNode):
    pass
