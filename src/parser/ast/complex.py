# complex meaning it can contain other nodes other than primitives
from src.parser.ast.ast_node import AstNode


class ArithmeticExpression(AstNode):
    def __init__(self, left_operand, operator, right_operand):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand


class FunctionDeclaration(AstNode):
    # int fun(<arg_list>){ return; }
    pass


class IfStatement(AstNode):
    pass


class WhileStatement(AstNode):
    pass
